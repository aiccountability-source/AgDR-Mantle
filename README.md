# AgDR-Mantle v1.0.6

Sovereign post-quantum fortification for AgDR records.

## Architecture

AgDR-Mantle is the Fortification tier of the AgDR standard. It operates within a three-tier lineage:

- **AKI** is the Core. Atomic Kernel Inference is the architectural principle defined in the AgDR specification. It is captured at the moment of decision and carries the PPP triplet (Provenance, Place, Purpose).
- **AgDR-Phoenix** is the Implementation. The reference Rust engine that realizes the AKI Core in running code at sub-microsecond latency, with kernel monotonic timestamps, Byzantine fault tolerance, and the critic pre-filter.
- **AgDR-Mantle** is the Fortification. It wraps AgDR-Phoenix output with an optional ML-DSA-65 post-quantum envelope, a sovereign sparse Merkle tree witness, and Brotli-compressed forensic archives for Commonwealth and bandwidth-constrained deployments.

```
+---------------------------------------------------+
|  AgDR-Mantle : FORTIFICATION                      |
|  - ML-DSA-65 (FIPS 204) post-quantum envelope     |
|  - Sovereign Sparse Merkle Tree witness           |
|  - Brotli-compressed forensic archive             |
+---------------------------------------------------+
|  AgDR-Phoenix : IMPLEMENTATION                    |
|  - Rust AKI engine, sub-microsecond latency       |
|  - BFT, critic, PPP capture, kernel timestamps    |
+---------------------------------------------------+
|  AKI : CORE                                       |
|  The architectural invariant. Defined in the      |
|  AgDR specification. Captured at decision time.   |
+---------------------------------------------------+
```

The Phoenix hot path remains classical Ed25519 and is not modified by Mantle. Mantle runs after Phoenix completes. Its operations therefore do not affect AKI latency.

## Features

- Optional ML-DSA-65 (FIPS 204) quantum-resistant signature envelope via the pqcrypto library. Opt-in, disabled by default.
- Sovereign forensic archive using a 256-bit sparse Merkle tree with Brotli compression.
- Self-learning coherence weighting via exponential moving average (feature-gated).
- Designed for Commonwealth, Northern, and other bandwidth-constrained jurisdictions requiring quantum-resistant evidentiary signatures today.

## Install

~~~bash
pip install agdr-mantle

# With the post-quantum fortification enabled
pip install agdr-mantle[post-quantum]

# With all optional features
pip install agdr-mantle[post-quantum,self-learning,sovereign]
~~~

## Quick Start

~~~python
from agdr_mantle import AgDRMantle

# Classical AKI only (fastest configuration)
engine = AgDRMantle(fo_i="Accountability (Toronto)")

# With ML-DSA-65 post-quantum fortification enabled
engine = AgDRMantle(
    fo_i="Accountability (Toronto)",
    enable_pq=True,
    enable_self_learning=True,
    enable_sovereign=True,
)

ppp = {"provenance": "...", "place": "Toronto, ON", "purpose": "Accountability review"}
sealed_record = engine.seal(ppp)

# Verify the post-quantum fortification envelope
if sealed_record["pq_applied"]:
    envelope = bytes.fromhex(sealed_record["aki_seal"])
    assert engine.pq.verify(envelope)
~~~

## Post-Quantum Fortification Notes

- Algorithm: ML-DSA-65 (NIST FIPS 204, Security Level 3, 192-bit classical equivalent strength).
- Signature size: 3,309 bytes per envelope.
- Public key size: 1,952 bytes. Private key size: 4,032 bytes.
- Library: pqcrypto v0.4.0 or later. The pqcrypto package wraps the pqclean reference C implementations and ships pre-compiled wheels for common platforms.
- Envelope format: `[seal_length][classical_seal][MAGIC][pubkey_length][pubkey][sig_length][signature]`.
- Keys: ephemeral per-instance by default. Production deployments should inject long-term keys through the `pq_keypair` constructor parameter.

## Performance

Measured on commodity hardware:

| Operation | Latency |
|---|---|
| ML-DSA-65 keygen | around 0.3 ms |
| Sign and wrap | around 1 ms |
| Verify | around 0.2 ms |

The fortification layer runs downstream of AgDR-Phoenix. The Phoenix hot path latency is unaffected.

## Related Artifacts

- AgDR Specification
- AgDR-Phoenix (the AKI Implementation)
- Eternal Witness v3.0 (forensic permanence layer)

## License

Dual-licensed under your choice of:

- Creative Commons Zero v1.0 Universal (CC0 1.0)
- Apache License 2.0

See the LICENSE file for full terms.

## About

AgDR-Mantle is published by the Genesis Glass Foundation (Fondation Genese Cristal), a federally incorporated Canadian not-for-profit stewarding the AgDR open standard through accountability.ai.
