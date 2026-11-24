# Payments webhook rotation

## Rotate a webhook signing secret
Payments webhook signing secret rotation: add the new secret to the receiver before changing the sender. The receiver accepts both signing secrets for 24 hours. After that window, remove the old secret.

## Check delivery
After switching the sender, verify webhook delivery with the sandbox test event. A valid signature and an HTTP 2xx response are both required to close the change.
