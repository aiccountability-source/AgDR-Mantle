# AgDR-Mantle: Sovereign Commonwealth Eternal Witness and Post-Quantum Fortification

This document outlines the cryptographic governance and post-quantum fortification design for capturing Atomic Kernel Inferences (AKI) and Atomic Genesis Decision Records (AgDR) in high-stakes domains, including healthcare and regulated enterprise workloads.

Canonical source and verification reference: [https://accountability.ai](https://accountability.ai)

For legal, healthcare, privacy, and regulatory mappings, see [REGULATORY-ALIGNMENT.md](https://github.com/aiccountability-source/AgDR-Phoenix/blob/main/REGULATORY-ALIGNMENT.md).

Built to serve Beauty, Truth, and Wisdom under the spirit of the Commonwealth Charter and in honour of the King of the Commonwealth.

AgDR turns AI agentic and inference events into verifiable records built for high-stakes accountability.

## Core Capabilities and Spine Architecture

- **PPP Triplet:** Captures Provenance, Place, and Purpose for every record.
- **Sparse Merkle Forest and Witnessing:** Hierarchical Merkle tree structure and `SparseMerkleTree` / `SparseMerkleCUDA` wrapper hooks in `agdr_sovereign_v1_0_fixed.py`.
- **Human Delta Chain:** Explicit human oversight and override tracking (`human_delta`).
- **Medical and Clinical Extensions:** Pseudonymized patient identifiers, consent versioning, clinical risk tiers, and health-privacy alignment (`agdr_medical_swarm.py`, `agdr_sovereign_v1_0_fixed.py`).
- **NemoClaw and Spine Integration:** Native event emission and policy blueprint integration (`agdr_spine.py`, `nemo_claw_blueprint.yaml`).
- **Optional Post-Quantum Fortification:** `ML-DSA-65` (NIST FIPS 204) signing and verification layered alongside baseline `BLAKE3`, `Ed25519`, and Brotli compression.
- **Privacy by Design:** Pseudonymization and zero-knowledge proof hooks for reasoning traces.
- **Wire Schema:** `src_provenance-packet.proto` for structured provenance packet serialization.

## Operational Notes and Trade-Offs

- **Hot-path isolation:** Post-quantum signing and tree witnessing run downstream of record sealing so capture latency in `AgDR-Phoenix` stays isolated.
- **Signature size and placement:** `ML-DSA-65` keys and signatures are larger than classical elliptic-curve counterparts. Place signing and verification at record boundaries, batch checkpoints, or archival steps rather than inner loops.
- **Wrapper maturity:** `SparseMerkleCUDA` in `agdr_sovereign_v1_0_fixed.py` provides a wrapper interface rather than a completed GPU kernel. Verify implementation maturity before production use.

## Quick Start

```bash
pip install agdr-mantle
```

For post-quantum and sovereign extras:

```bash
pip install agdr-mantle[post-quantum,self-learning,sovereign]
```

## Repository Root Files Referenced

- `agdr_sovereign_v1_0_fixed.py`: Sovereign Commonwealth Eternal Witness (`CommonwealthEternalWitness`, `SparseMerkleTree`, and `SparseMerkleCUDA` wrapper).
- `agdr_medical_swarm.py`: Medical swarm multi-agent telemetry harness.
- `agdr_spine.py`: Sovereign governance spine orchestration.
- `nemo_claw_blueprint.yaml`: NemoClaw agentic deployment blueprint.
- `src_provenance-packet.proto`: Protocol Buffers schema for provenance packets.
- `README.md`: Main package overview, installation, and wheel matrix.
- `LICENSE`: Dual-license text.

## License and Governance

Dual-licensed under CC0 1.0 or Apache 2.0. Maintained by the Genesis Glass Foundation (Fondation Genèse Cristal), a federally incorporated Canadian not-for-profit operating without vendor lock-in or code royalties.
