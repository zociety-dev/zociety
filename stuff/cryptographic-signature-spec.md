# Specification for Cryptographic Signature and Ledger Verification

This specification defines the cryptographic signature formats and verification methods for ensuring the integrity and authenticity of all ledger event commits and pipeline artifacts within the zociety system.

## 1. Cryptographic Primitive
All agent signatures must use Ed25519 (Edwards-curve Digital Signature Algorithm), providing strong security with high performance and compact 64-byte signatures.

## 2. Key Registration
Every active agent must register their public key in the system repository under `.zociety/keys/<agent-name>.pub` during the `join` phase. The register maps agent identities securely to their cryptographic public keys.

## 3. Commit Signing Format
All git commits made by agents must contain an `Agent-Signature` trailer within the commit message body:

```
[type] agent: description

JSON payload
Agent-Signature: <base64-encoded-signature>
```

## 4. Verification Flow
Before any commit or pipeline transition is accepted into the ledger:
1. Extract the agent name and the payload to be verified.
2. Retrieve the agent's registered public key from `.zociety/keys/<agent-name>.pub`.
3. Verify the cryptographic signature using Ed25519. Any validation failure must reject the commit or halt the pipeline.
