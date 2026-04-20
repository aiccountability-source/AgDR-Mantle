"""
AgDR-Mantle engine: Fortification tier orchestration.

Wraps AgDR-Phoenix (the AKI Implementation) output with optional
post-quantum fortification, sovereign sparse Merkle witness,
and self-learning coherence weighting.
"""
import time
from typing import Dict, Any, Optional, Tuple

try:
    from ._core import AKIEngine
except ImportError:
    AKIEngine = None

from .pq_fortification import PQFortification, PQCRYPTO_AVAILABLE
from .self_learning import CoherenceWeightUpdater
from .sovereign_witness import CommonwealthEternalWitness


class AgDRMantle:
    """The AgDR-Mantle Fortification engine.

    Orchestrates AgDR-Phoenix AKI capture and wraps its output with
    optional sovereign fortification layers:

      * Post-quantum envelope (ML-DSA-65, FIPS 204)
      * Sovereign sparse Merkle tree witness with Brotli archive
      * Self-learning coherence weighting

    The Phoenix hot path is not modified. All Mantle operations run
    downstream of AKI capture and therefore do not affect AKI latency.
    """

    def __init__(
        self,
        fo_i: str = "Accountability",
        enable_pq: bool = False,
        enable_self_learning: bool = False,
        enable_sovereign: bool = False,
        nemoclaw_mode: bool = True,
        pq_keypair: Optional[Tuple[bytes, bytes]] = None,
    ):
        """Initialize the Mantle engine.

        Args:
            fo_i: The Field of Inference declaration string.
            enable_pq: Enable ML-DSA-65 post-quantum fortification envelope.
            enable_self_learning: Enable EMA-based coherence weighting.
            enable_sovereign: Enable sovereign sparse Merkle witness.
            nemoclaw_mode: Enable NEMOCLAW diagnostic output for sovereign records.
            pq_keypair: Optional (public_key, private_key) tuple for long-term keys.
                        If None, an ephemeral keypair is generated per instance.
        """
        self.fo_i = fo_i
        self.enable_pq = enable_pq
        self.enable_self_learning = enable_self_learning
        self.enable_sovereign = enable_sovereign

        if AKIEngine is None:
            raise ImportError(
                "AgDR-Phoenix Rust extension (_core) is not built. "
                "Run: maturin develop --release"
            )
        self.phoenix = AKIEngine(fo_i=fo_i)

        if self.enable_pq:
            if not PQCRYPTO_AVAILABLE:
                raise ImportError(
                    "Post-quantum fortification requested but pqcrypto is not installed. "
                    "Install with: pip install agdr-mantle[post-quantum]"
                )
            self.pq = PQFortification(keypair=pq_keypair)
        else:
            self.pq = None

        self.learning = CoherenceWeightUpdater() if self.enable_self_learning else None
        self.witness = (
            CommonwealthEternalWitness(nemoclaw_mode=nemoclaw_mode)
            if self.enable_sovereign
            else None
        )

    def seal(self, ppp: Dict[str, Any]) -> Dict[str, Any]:
        """Seal a PPP record through AKI and optional Mantle fortification.

        Args:
            ppp: Provenance, Place, Purpose triplet as a dict.

        Returns:
            Sealed record including AKI seal (optionally fortified with PQ envelope),
            sovereign witness entry if enabled, and tier latencies.
        """
        t_total_start = time.perf_counter_ns()

        # Tier: AgDR-Phoenix Implementation captures the AKI Core
        t_aki = time.perf_counter_ns()
        aki_seal = self.phoenix.seal_ppp(ppp)
        aki_latency_ns = time.perf_counter_ns() - t_aki

        # Tier: AgDR-Mantle Fortification wraps the AKI seal
        fortification_latency_ns = 0
        if self.pq:
            t_pq = time.perf_counter_ns()
            aki_seal = self.pq.wrap(aki_seal)
            fortification_latency_ns = time.perf_counter_ns() - t_pq

        if self.learning:
            coherence = self._compute_coherence(aki_seal)
            if coherence > 0.92:
                self.learning.update_weights(aki_seal, coherence)

        sovereign_record = None
        if self.witness:
            sovereign_record = self.witness.capture_medical(
                agent_id=ppp.get("provenance", "unknown"),
                patient_pseudo=ppp.get("place", "unknown"),
                reasoning_trace=ppp.get("purpose", ""),
            )

        total_latency_ns = time.perf_counter_ns() - t_total_start

        return {
            "aki_seal": aki_seal.hex() if isinstance(aki_seal, (bytes, bytearray)) else str(aki_seal),
            "pq_applied": self.enable_pq,
            "pq_algorithm": "ML-DSA-65" if self.enable_pq else None,
            "self_learning_applied": self.enable_self_learning,
            "sovereign_witness": sovereign_record,
            "aki_latency_us": aki_latency_ns / 1000,
            "fortification_latency_us": fortification_latency_ns / 1000,
            "total_latency_us": total_latency_ns / 1000,
            "tier_breakdown": {
                "core_aki": "captured",
                "implementation_phoenix": "sealed",
                "fortification_mantle": "applied" if (self.enable_pq or self.enable_sovereign) else "not_applied",
            },
        }

    def _compute_coherence(self, sealed: bytes) -> float:
        """Placeholder for coherence computation. Production integrates with AgDR-FSv2.1."""
        return 0.95
