"""
AgDR-Mantle v1.0.1

Sovereign post-quantum fortification for AgDR records.

Three-tier architecture:
    AKI           - the Core (principle, defined in the AgDR specification)
    AgDR-Phoenix  - the Implementation (Rust reference AKI engine)
    AgDR-Mantle   - the Fortification (this package)

Published by the Genesis Glass Foundation (Fondation Genese Cristal).
Licensed under CC0 1.0 OR Apache 2.0.
"""
from .mantle_engine import AgDRMantle
from .pq_fortification import PQFortification
from .sovereign_witness import CommonwealthEternalWitness

__version__ = "1.0.1"
__all__ = [
    "AgDRMantle",
    "PQFortification",
    "CommonwealthEternalWitness",
]
