# Use GRPC for Datastore access

Use the GRPC option for Datastore access.

https://github.com/ONSdigital/eq-survey-runner/tree/use-grpc-for-datastore-access

## Benchmark profile

| Option | Value |
|--------|-------|
| Requests file | test_checkbox.json |
| Run time | 5m |
| User wait time minimum | 0 |
| User wait time maximum | 0 |
| Clients | 1 |
| Hatch rate | 1 |

## Results

Application breaks when authenticating. Error:
```
"app.authentication.jti_claim_storage.JtiTokenUsed: jti claim '063c5e95-f28c-4fa5-9fb2-d5d9ea59b267' has already been used" 
```

## Decision

Discard.

