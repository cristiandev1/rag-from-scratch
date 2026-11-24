# PostgreSQL logical backups

## Parallel restore
Parallel restore with pg_restore --jobs requires a custom-format or directory-format archive. Supply a regular file or directory as input. A pipe or standard input will not work with parallel jobs, and parallel restore cannot be combined with --single-transaction. Source: https://www.postgresql.org/docs/current/app-pgrestore.html

## Parallel dump
For a parallel dump, use pg_dump --jobs with the directory output format. The directory format stores separate files for table data and a table of contents. Source: https://www.postgresql.org/docs/current/app-pgdump.html
