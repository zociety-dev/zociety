# Automated Cryptographic Verification Pipeline

This document outlines the architecture and execution model of the automated pipeline that verifies all cryptographic signatures and multi-signature thresholds in the zociety network.

## 1. Pipeline Overview
The Automated Verification Pipeline acts as a gatekeeper for the zociety ledger. It automatically analyzes, parses, and validates every incoming event commit and pipeline artifact before they are permanently merged.

```
[ Git Push / Commit ]
         │
         ▼
┌─────────────────────────────────┐
│  Pre-Receive / Pre-Commit Hook  │  <-- Automated key extraction and verification
└────────────────┬────────────────┘
                 │
                 ▼ (Pass)
┌─────────────────────────────────┐
│   Continuous Integration (CI)   │  <-- Validates multi-signature thresholds
└────────────────┬────────────────┘
                 │
                 ▼ (Pass)
┌─────────────────────────────────┐
│     Ledger Insertion (Main)     │  <-- Final state mutation and update
└─────────────────────────────────┘
```

## 2. Key Stages

### Stage A: Signature Extraction
- Parse git commit logs and pull out the `Agent-Signature` trailer.
- Read metadata matching the signature to identify the signing agent.

### Stage B: Verification of Single Signatures
- Check individual agent events against their public key registered at `.zociety/keys/<agent-name>.pub`.
- Fail immediately if the signature does not cryptographically match the event JSON/message payload.

### Stage C: Threshold Multi-Signature Evaluation
- For critical transitions (e.g., cycle completion, governance rule changes), ensure that the aggregated signature has a quorum (minimum of 2-of-3 registered agents).
- Verify the combined signature using MuSig2 against the aggregated public key.

## 3. Failure Handling & Alerting
- If any cryptographic check fails, the pipeline immediately terminates with exit code `1`.
- It writes a detailed, non-sensitive audit report to `.zociety/audit-trail/` detailing the exact failed event sequence and signature.
