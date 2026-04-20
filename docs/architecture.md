# AgDR-Mantle Architecture

## Three-Tier Lineage

AgDR-Mantle operates within a three-tier architecture that separates principle from implementation from protection:

```
+-------------------------------------------------------+
|  TIER 3: FORTIFICATION                                |
|  AgDR-Mantle v1.0.1                                   |
|  - ML-DSA-65 (FIPS 204) post-quantum envelope         |
|  - Sovereign Sparse Merkle Tree (256-bit, BLAKE3)     |
|  - Brotli forensic archive (Commonwealth-ready)       |
|  - Self-learning coherence weighting (EMA)            |
+-------------------------------------------------------+
                          ^
                          | wraps output of
                          |
+-------------------------------------------------------+
|  TIER 2: IMPLEMENTATION                               |
|  AgDR-Phoenix v1.8                                    |
|  - Rust AKI engine (sub-microsecond latency)          |
|  - Byzantine fault tolerance, critic pre-filter       |
|  - PPP triplet capture, kernel monotonic timestamps   |
+-------------------------------------------------------+
                          ^
                          | realizes
                          |
+-------------------------------------------------------+
|  TIER 1: CORE                                         |
|  AKI (Atomic Kernel Inference)                        |
|  - Architectural invariant                            |
|  - Defined in the AgDR specification                  |
|  - Captured at the moment of decision                 |
|  - Carries the PPP triplet: Provenance, Place,        |
|    Purpose                                            |
+-------------------------------------------------------+
```

## Tier Responsibilities

**AKI (Core).** The principle. Defined in the AgDR specification. Captured at the moment of decision. AKI is not a product and not a codebase. AKI is what every Implementation must realize and what every Fortification must preserve.

**AgDR-Phoenix (Implementation).** The first reference implementation of the AKI Core. Written in Rust. Targets sub-microsecond hot-path latency. Captures the PPP triplet, stamps kernel monotonic timestamps, and produces a classical Ed25519 seal. Phoenix is not AKI. Phoenix is how AKI gets captured in running code. Other Implementations may follow in other languages, and all must preserve the same AKI invariants.

**AgDR-Mantle (Fortification).** This package. Wraps AgDR-Phoenix output with optional sovereign protection layers. Does not modify the Phoenix hot path. Operates entirely downstream of AKI capture. Adds quantum-resistant signatures, sparse Merkle inclusion proofs, and Brotli-compressed forensic archives.

## Why Fortification Runs Downstream

ML-DSA-65 signing completes in approximately 1 millisecond on commodity CPUs. AKI targets sub-microsecond latency. Placing fortification inside the hot path would destroy the AKI latency budget.

Placing it downstream preserves the AKI property. The Phoenix implementation seals classically at full speed. The Mantle fortification then wraps that seal with post-quantum and sovereign layers for adopters who require them.

## Why the Fortification Tier Matters Now

The AKI Core itself is quantum-resistant conceptually: it is a record, not a secret. What needs quantum-resistance is the signature that authenticates the record. At the Core level that signature is defined abstractly. At the Implementation level (Phoenix v1.8) it is currently Ed25519 (classical), with ML-DSA-65 scheduled as a future Phoenix upgrade. At the Fortification level (Mantle v1.0.1) ML-DSA-65 is available today as an optional envelope.

This lets adopters opt into quantum-resistant evidentiary signatures immediately without waiting for the Phoenix kernel upgrade cycle. The Foundation's layered architecture is designed exactly for this kind of staged cryptographic migration.

## Envelope Format

Mantle post-quantum envelopes follow this format:

```
[seal_len : 4 bytes big-endian]
[classical_aki_seal : N bytes]
[MAGIC : 6 bytes]             = b"AGPQ65"
[pubkey_len : 2 bytes][ML-DSA-65 public key : 1952 bytes]
[sig_len : 2 bytes][ML-DSA-65 signature : ~3309 bytes]
```

Total envelope overhead is approximately 5,275 bytes plus the inner classical seal length.

## Performance Envelope

Measured on commodity hardware:

| Tier | Operation | Latency |
|---|---|---|
| Implementation (Phoenix) | AKI capture | below 1 microsecond |
| Fortification (Mantle) | ML-DSA-65 keygen | around 0.3 ms |
| Fortification (Mantle) | ML-DSA-65 sign and wrap | around 1 ms |
| Fortification (Mantle) | ML-DSA-65 verify | around 0.2 ms |

The Phoenix hot path latency is unaffected by Mantle operations.

## License

CC0 1.0 Universal OR Apache License 2.0.
