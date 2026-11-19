# AgDR-Mantle v1.1.5

AgDR-Mantle provides post-quantum cryptographic fortification and witness tooling for Atomic Genesis Decision Record (AgDR) payloads. It forms the third tier of the lineage (Core, Implementation, Fortification) alongside [AgDR-Phoenix (`agdr-aki`)](https://github.com/aiccountability-source/AgDR-Phoenix).

Canonical source and verification reference: [https://accountability.ai](https://accountability.ai)

For post-quantum architecture and governance details, see [README-PQC.md](README-PQC.md).

## Overview

AgDR-Mantle adds an optional post-quantum security layer on top of sealed AgDR-Phoenix records:

- **Signatures:** Optional ML-DSA-65 (NIST FIPS 204) signing and verification.
- **Witnesses:** Sparse Merkle tree witness handling and Brotli compression.
- **Hot-path isolation:** Runs after record sealing, leaving the AgDR-Phoenix capture hot path at 0.62 microseconds.

## Installation

### Python (`pip`)

```bash
pip install agdr-mantle
```

Optional feature sets:

```bash
pip install agdr-mantle[post-quantum]
pip install agdr-mantle[post-quantum,self-learning,sovereign]
```

- `post-quantum`: Enables ML-DSA-65 signing and verification support.
- `self-learning`: Enables sparse Merkle witness update support.
- `sovereign`: Enables sovereign harness, blueprint, and telemetry helpers.

### Rust (`cargo`)

```bash
cargo add agdr-mantle
```

## Quick Example

```python
from agdr_mantle import AgDRMantle

engine = AgDRMantle(fo_i="Accountability (Toronto)")
ppp = {"provenance": "...", "place": "Toronto", "purpose": "Test"}
record = engine.seal(ppp)
```

## Harnesses, Wrappers, and Schemas

- `agdr_sovereign_v1_0_fixed.py`: Standalone reference harness containing `CommonwealthEternalWitness` (`capture_medical`, `nemoclaw_mode`), a BLAKE3 256-bit `SparseMerkleTree`, and `SparseMerkleCUDA` (a drop-in wrapper interface intended for a future `pybind11` and CUDA implementation).
- `agdr_medical_swarm.py`: Reference multi-agent clinical telemetry and coordination harness.
- `agdr_spine.py`: Sovereign governance orchestration harness.
- `nemo_claw_blueprint.yaml`: Agentic deployment blueprint configuration.
- `src_provenance-packet.proto`: Protocol Buffers schema for provenance packets.

## Repository Layout

- `src/`: Rust crate source (`Cargo.toml`)
- `python/agdr_mantle/`: Python package and `abi3` bindings (`pyproject.toml`)
- `agdr_sovereign_v1_0_fixed.py`: Sovereign Commonwealth Eternal Witness and `SparseMerkleCUDA` wrapper
- `agdr_medical_swarm.py`: Medical swarm multi-agent telemetry harness
- `agdr_spine.py`: Sovereign governance spine orchestration
- `nemo_claw_blueprint.yaml`: NemoClaw agentic deployment blueprint
- `src_provenance-packet.proto`: Protocol Buffers schema for provenance packets
- `README-PQC.md`: Post-quantum cryptography and governance notes
- `bump-version.ps1`: Version synchronization script
- `tests/`: Test suite

## Benchmarks

These numbers come from a build container rather than production hardware. Actual timings vary by CPU or GPU architecture, payload size, active feature flags, and native versus wrapper execution paths:

- **ML-DSA-65 key generation:** 0.3 ms
- **Sign and wrap:** 1 ms
- **Verify:** 0.2 ms

## Platform Support

Pre-built `cp39-abi3` wheels support Python 3.9 through 3.14:

- **Linux (PyPI):** `x86_64`, `aarch64`
- **ARM Linux (piwheels):** `linux_armv6l`, `linux_armv7l` (`piwheels.org/project/agdr-mantle`)
- **Windows (PyPI):** `x64`
- **macOS (PyPI):** `x86_64`, `aarch64`

## Changelog

### v1.1.5 (May 2026)
- Synchronized release metadata across `Cargo.toml`, `pyproject.toml`, and `bump-version.ps1` with OIDC trusted publishing.
- Standardized multi-architecture pre-built wheels across PyPI and piwheels for Python 3.9 through 3.14.
- Documented root reference harnesses, wrappers, and schemas (`agdr_sovereign_v1_0_fixed.py`, `agdr_medical_swarm.py`, `agdr_spine.py`, `nemo_claw_blueprint.yaml`, `src_provenance-packet.proto`) alongside `README-PQC.md`.

### v1.1.1 (May 2026)
- Added multi-architecture pre-built wheels for Linux (`x86_64`, `aarch64`), Windows (`x64`), and macOS (`x86_64`, `aarch64`).
- Added official Python 3.13 and 3.14 support (`requires-python` `>=3.9,<3.15`) using `abi3-py39` and automated GitHub Actions wheel workflows.

## License

Dual-licensed under CC0 1.0 or Apache 2.0. Choose whichever fits your project.

## Governance and Links

AgDR-Mantle is maintained by the Genesis Glass Foundation (Fondation Genèse Cristal), a federally incorporated Canadian not-for-profit operating without vendor lock-in or code royalties.

- **AgDR Specification:** [https://github.com/aiccountability-source/AgDR](https://github.com/aiccountability-source/AgDR)
- **AgDR-Phoenix:** [https://github.com/aiccountability-source/AgDR-Phoenix](https://github.com/aiccountability-source/AgDR-Phoenix)
- **Chartered Donee:** [Council of Canadians with Disabilities (CCD)](https://www.ccdonline.ca/en/)
