# AgDR-Mantle v1.1.5

**Sovereign post-quantum fortification for AgDR records.**

## What it does
AgDR-Mantle adds an optional **post-quantum security layer** to AgDR-Phoenix [2]. It wraps each sealed record with an **ML-DSA-65 signature** (NIST FIPS 204), **Self-Learning/Evolving** a **sparse Merkle tree witness**, and **Brotli compression** [2].

You do not need to change your existing AgDR-Phoenix setup; Mantle runs after the fact [2]. The "hot path" for **Atomic Kernel Inferences** (AKI) remains at **0.62 microseconds** [2, 4].

## Changes from v1.1.1 to v1.1.5
**v1.1.5 (May 2026):** Multi-architecture infrastructure synchronization [1, 2].

*   **Updated:** Standardized multi-architecture pre-built wheels for **Linux** (x86_64, aarch64), **Windows** (x64), and **macOS** (Intel, Apple Silicon) [1, 5, 6].
*   **Added:** Official support for **Python 3.13 and 3.14**.
*   **Refinement:** Synchronized versioning across `Cargo.toml`, `pyproject.toml`, and the `bump-version.ps1` automation suite.
*   **Maintenance:** No changes were made to the Rust core or Python bindings—these updates focus on distribution and infrastructure stability.

## Install
```bash
pip install agdr-mantle
With post-quantum enabled: pip install agdr-mantle[post-quantum]
With all features: pip install agdr-mantle[post-quantum,self-learning,sovereign]
Quick example
from agdr_mantle import AgDRMantle

engine = AgDRMantle(fo_i="Accountability (Toronto)")
ppp = {"provenance": "...", "place": "Toronto", "purpose": "Test"}
record = engine.seal(ppp)
Performance
These numbers come from a build container, not production hardware
.
ML-DSA-65 key generation: 0.3 ms
Sign and wrap: 1 ms
Verify: 0.2 ms
Platform Support
Pre-built wheels available for:
Linux: x86_64, aarch64 (ARM64)
Windows: x64
macOS: x86_64 (Intel), aarch64 (Apple Silicon)
Python 3.9 through 3.14 are supported via the abi3 stable binary interface
.
License
You can use this under either CC0 1.0 or Apache 2.0. Pick the one that works for you
.
About
AgDR-Mantle is maintained by the Genesis Glass Foundation, a federally incorporated Canadian not-for-profit
. The standard is open, with no vendor lock-in and no royalties
. It represents a three-tier lineage (Core, Implementation, Fortification) published for sovereign data integrity

# AgDR-Mantle v1.1.1

Sovereign post-quantum fortification for AgDR records.

## What it does

AgDR-Mantle adds an optional post-quantum security layer to AgDR-Phoenix.
It wraps each sealed record with an ML-DSA-65 signature, a sparse Merkle
tree witness, and Brotli compression.

You do not need to change your existing AgDR-Phoenix setup. Mantle runs
after the fact. The hot path stays at 0.62 microseconds.

## Changes from v1.0.8 to v1.1.1

v1.1.1 (May 2026): Multi-architecture wheels and expanded Python support.

- Added: Multi-architecture pre-built wheels for Linux (x86_64, aarch64), Windows (x64), and macOS (Intel, Apple Silicon)
- Added: Official Python 3.13 and 3.14 support
- Added: Automated GitHub Actions CI/CD for wheel building and publishing
- Changed: PyO3 ABI target updated to abi3-py39 for forward Python compatibility
- Changed: requires-python expanded from >=3.9,<3.13 to >=3.9,<3.15

Note: No Rust core or Python binding changes--purely distribution and infrastructure improvements.

## Install

pip install agdr-mantle

With post-quantum enabled:
pip install agdr-mantle[post-quantum]

With all features:
pip install agdr-mantle[post-quantum,self-learning,sovereign]

## Quick example

from agdr_mantle import AgDRMantle

engine = AgDRMantle(fo_i="Accountability (Toronto)")
ppp = {"provenance": "...", "place": "Toronto", "purpose": "Test"}
record = engine.seal(ppp)

## Performance

These numbers come from a build container, not production hardware.

ML-DSA-65 key generation: 0.3 ms
Sign and wrap: 1 ms
Verify: 0.2 ms

## Platform Support

Pre-built wheels available for:
- Linux: x86_64, aarch64 (ARM64)
- Windows: x64
- macOS: x86_64 (Intel), aarch64 (Apple Silicon)

Python 3.9 through 3.14 supported via abi3.

## License

You can use this under either CC0 1.0 or Apache 2.0. Pick the one that
works for you.

## About

AgDR-Mantle is maintained by the Genesis Glass Foundation, a federally
incorporated Canadian not-for-profit. The standard is open. No vendor
lock-in. No royalties. Chartered Donee: Council of
Canadians with Disabilities (CCD) https://www.ccdonline.ca/en/
