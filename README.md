 HEAD
# AgDR-Mantle v1.0.6

# AgDR-Mantle
 a7be03a (docs: add Python 3.13/3.14 to supported versions)

Post-quantum fortification for AgDR records.

## What it does

AgDR-Mantle adds an optional post-quantum security layer to AgDR-Phoenix.
It wraps each sealed record with an ML-DSA-65 signature, a sparse Merkle
tree witness, and Brotli compression.

You do not need to change your existing AgDR-Phoenix setup. Mantle runs
after the fact. The hot path stays at 0.62 microseconds.

## Changes from v1.0.1 to v1.0.5

v1.0.2: Fixed license syntax. Corrected the spec URL. Set Python to less
        than 3.13.

v1.0.3: Fixed PyO3 compatibility. Added native Windows wheels.

v1.0.4: Added Brotli compression. Published to PyPI.

v1.0.5: Cleaned up documentation.

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

## License

You can use this under either CC0 1.0 or Apache 2.0. Pick the one that
works for you.

## About

AgDR-Mantle is maintained by the Genesis Glass Foundation, a federally
incorporated Canadian not-for-profit. The standard is open. No vendor
lock-in. No royalties.