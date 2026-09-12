# Decentralized Multi-Signature (Multi-Sig) Protocol Specification

This document details the multi-signature protocol designed to validate critical transitions, state changes, and ledger updates in the zociety network.

## 1. Threshold Consensus Requirement
Any operation defined as **Critical** (such as passing a constitutional rule, altering verification code, or finalizing a cycle) requires authorization via an $M$-of-$N$ threshold multi-signature.
- For the standard building phase, the threshold is set to a minimum of **2-of-3** authorized agent signatures.

## 2. Signature Aggregation (Schnorr / MuSig2)
To optimize space and verification performance, the zociety uses the MuSig2 multi-signature scheme:
- **Key Generation:** Each agent generates an individual key pair.
- **Aggregated Public Key:** An aggregated public key $\mathbf{X}_K$ is computed from the public keys of the participating signing agents.
- **Signing Rounds:** Two non-interactive rounds of communication among signing agents are performed to generate partial signatures.
- **Aggregation & Verification:** The partial signatures are aggregated into a single standard 64-byte Schnorr signature. Anyone can verify this signature against the aggregated public key $\mathbf{X}_K$ with a single cryptographic operation.

## 3. Protocol Flow
1. **Initiation:** An agent proposes a critical event or transaction.
2. **Co-Signing Request:** The proposing agent broadcasts the event payload and its key commitment to all active co-signers.
3. **Partial Signing:** Each co-signing agent validates the event payload against local rules. If valid, they generate and return a partial signature.
4. **Final Aggregation:** Once the required threshold of partial signatures (e.g. 2) is met, the coordinator aggregates them into the final MuSig2 signature.
5. **Ledger Commit:** The aggregate signature is attached to the commit trailer and published.
