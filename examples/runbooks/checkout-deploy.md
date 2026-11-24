# Checkout deployment

## Rollback trigger
Roll back a checkout deployment if the checkout error rate exceeds 2% for five consecutive minutes. Compare against the production checkout dashboard.

## Rollback procedure
To roll back checkout, redeploy the last healthy image and confirm checkout success with a smoke test. Keep the failed release ID in the incident timeline.
