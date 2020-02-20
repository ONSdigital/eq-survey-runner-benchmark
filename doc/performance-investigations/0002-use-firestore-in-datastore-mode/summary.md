# Investigate Firestore in Datastore Mode

Current databases created via the Python Datastore library are traditional Datastore databases, Firestore offers a Datastore compatibility mode that reduces or removes some of the limitations of native Datatore.

See https://cloud.google.com/datastore/docs/firestore-or-datastore for more details.

## Results

On investigation, it became apparent that all new projects created since changing to eq-terraform-gcp are now created using Firestore in Datastore mode by default. This is caused by the Project no longer being managed by Terraform, which created legacy Datastore applications. This has created a difference between our formal and non-formal environments, as formal environments are still using the legacy Datastore mode. We should bring our formal environments in line with the eq-staging and test environments. It is possible to upgrade the Datastore application to Firestore via the project UI when all entities have been cleared out. An alternative is to recreate formal environment projects.

## Decision

Upgrade formal environments to Firestore in Datastore mode.
