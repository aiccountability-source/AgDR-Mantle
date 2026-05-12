  HEAD
# AgDR-Mantle v1.0.8

# AgDR-Mantle

Post-quantum fortification for AgDR records.

## What it does

AgDR-Mantle adds an optional post-quantum security layer to AgDR-Phoenix.
It wraps each sealed record with an ML-DSA-65 signature, a sparse Merkle
tree witness, and Brotli compression.

You do not need to change your existing AgDR-Phoenix setup. Mantle runs
after the fact. The hot path stays at 0.62 microseconds.

## Release Notes

### Version 1.0.8 (May 10, 2026)

**Multi-architecture wheels and expanded Python support**

#### Added
- Multi-architecture pre-built wheels for Linux (x86_64, aarch64, armv7), Windows (x64, ARM64), and macOS (Intel, Apple Silicon)
- Official Python 3.13 and 3.14 support
- Automated GitHub Actions CI/CD for wheel building and publishing

#### Changed
- PyO3 ABI target updated to `abi3-py39` for forward Python compatibility
- `requires-python` expanded from `>=3.9,<3.13` to `>=3.9,<3.15`

#### Fixed
- Raspberry Pi users can now install pre-built wheels instead of compiling from source

#### Note
No Rust core or Python binding changes—purely distribution and infrastructure improvements.

---

**Version 1.0.7 was an internal development version and is not available on PyPI.**

## Previous Changes (v1.0.1–v1.0.6)

v1.0.2: Fixed license syntax. Corrected the spec URL. Set Python to less
        than 3.13.

v1.0.3: Fixed PyO3 compatibility. Added native Windows wheels.

v1.0.4: Added Brotli compression. Published to PyPI.

v1.0.5: Cleaned up documentation.

v1.0.6: Build infrastructure refinements.

## Install

```bash
pip install agdr-mantle
```

With post-quantum enabled:
```bash
pip install agdr-mantle[post-quantum]
```

With all features:
```bash
pip install agdr-mantle[post-quantum,self-learning,sovereign]
```

## Quick example

```python
from agdr_mantle import AgDRMantle

engine = AgDRMantle(fo_i="Accountability (Toronto)")
ppp = {"provenance": "...", "place": "Toronto", "purpose": "Test"}
record = engine.seal(ppp)
```

## Performance

These numbers come from a build container, not production hardware.

- ML-DSA-65 key generation: 0.3 ms
- Sign and wrap: 1 ms
- Verify: 0.2 ms

## License

You can use this under either CC0 1.0 or Apache 2.0. Pick the one that
works for you.

## About

AgDR-Mantle is maintained by the Genesis Glass Foundation, a federally
incorporated Canadian not-for-profit. The standard is open. No vendor
lock-in. No royalties.
