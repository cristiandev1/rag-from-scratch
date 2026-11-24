import unittest
from pathlib import Path

from rag import Index, build_context, build_messages, load_chunks, split_document

CORPUS = Path(__file__).resolve().parents[1] / "examples/runbooks"
QUESTION = (
    "When should I roll back a checkout deployment, "
    "and how often should I post updates during the rollback?"
)


class RagTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = Index(load_chunks(CORPUS))

    def test_chunking_preserves_overlap_and_line_locations(self):
        chunks = split_document("sample.md", "one two\nthree four\n\nsix", size=3, overlap=1)
        self.assertEqual([chunk.text for chunk in chunks], ["one two three", "three four", "six"])
        self.assertEqual(
            [chunk.location for chunk in chunks],
            ["sample.md:1-2", "sample.md:2-2", "sample.md:4-4"],
        )

    def test_webhook_lookup(self):
        [(score, chunk)] = self.index.search("How long are both webhook signing secrets accepted?", 1)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 1)
        self.assertEqual(chunk.location, "payments-webhooks.md:3-4")
        self.assertIn("24 hours", chunk.text)

    def test_top_k_controls_source_coverage(self):
        small_context = build_context(self.index.search(QUESTION, 2), 2600)
        large_context = build_context(self.index.search(QUESTION, 4), 2600)
        self.assertNotIn("15 minutes", build_messages(QUESTION, small_context)[1]["content"])
        complete_prompt = build_messages(QUESTION, large_context)[1]["content"]
        self.assertIn("five consecutive minutes", complete_prompt)
        self.assertIn("[S3] incident-comms.md:3-4", complete_prompt)
        self.assertIn("15 minutes", complete_prompt)

    def test_no_positive_lexical_match(self):
        self.assertEqual(self.index.search("What is the catering budget?", 4), [])

    def test_budget_packs_whole_blocks_and_contiguous_source_ids(self):
        hits = self.index.search(QUESTION, 4)
        entries = build_context(hits, 70)
        self.assertEqual(len(entries), 1)
        self.assertTrue(entries[0][1].startswith("[S1] "))
        self.assertLessEqual(len(entries[0][1]), 70)
        self.assertEqual(build_context(hits, 1), [])


if __name__ == "__main__":
    unittest.main()
