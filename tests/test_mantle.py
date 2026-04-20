"""Tests for AgDR-Mantle v1.0.1."""
import pytest
from agdr_mantle import CommonwealthEternalWitness
from agdr_mantle.brotli_compress import (
    compress_forensic_bundle,
    decompress_forensic_bundle,
)

try:
    from agdr_mantle.pq_fortification import (
        PQFortification,
        PQCRYPTO_AVAILABLE,
        PQ_MAGIC,
        ML_DSA_65_PUBKEY_SIZE,
    )
except ImportError:
    PQCRYPTO_AVAILABLE = False

try:
    from agdr_mantle import AgDRMantle
    AGDR_CORE_AVAILABLE = True
except ImportError:
    AGDR_CORE_AVAILABLE = False


# ----- Fortification layer tests (pure Python, no Rust required) -----

def test_brotli_roundtrip():
    """Brotli compression round-trips AgDR forensic data."""
    original = b"AgDR-Mantle forensic data " * 100
    compressed = compress_forensic_bundle(original)
    decompressed = decompress_forensic_bundle(compressed)
    assert decompressed == original
    assert len(compressed) < len(original)


def test_sovereign_witness_basic():
    """Sovereign witness produces 32-byte SMT root for captured records."""
    witness = CommonwealthEternalWitness(nemoclaw_mode=False)
    rec = witness.capture_medical("agent_doctor_1", "patient_001", "Clinical reasoning trace")
    assert rec["adr_id"] == "adr_med_0"
    assert len(bytes.fromhex(rec["smt_root"])) == 32
    assert rec["compression_ratio"] < 1.0


@pytest.mark.skipif(not PQCRYPTO_AVAILABLE, reason="pqcrypto not installed")
def test_pq_fortification_sizes():
    """ML-DSA-65 keypair matches FIPS 204 specification sizes."""
    fortification = PQFortification()
    assert len(fortification.public_key) == ML_DSA_65_PUBKEY_SIZE


@pytest.mark.skipif(not PQCRYPTO_AVAILABLE, reason="pqcrypto not installed")
def test_pq_fortification_wrap_and_verify():
    """ML-DSA-65 envelope wraps, verifies, and extracts correctly."""
    fortification = PQFortification()
    aki_seal = b"ATOMIC_KERNEL_INFERENCE_SEAL_PLACEHOLDER"
    envelope = fortification.wrap(aki_seal)

    assert PQ_MAGIC in envelope
    assert fortification.verify(envelope) is True

    extracted = PQFortification.extract_aki_seal(envelope)
    assert extracted == aki_seal


@pytest.mark.skipif(not PQCRYPTO_AVAILABLE, reason="pqcrypto not installed")
def test_pq_fortification_tamper_detection():
    """Tampered envelopes fail verification."""
    fortification = PQFortification()
    aki_seal = b"original_seal_bytes"
    envelope = bytearray(fortification.wrap(aki_seal))

    envelope[-10] ^= 0xFF
    assert fortification.verify(bytes(envelope)) is False


# ----- Full engine tests (require Rust _core extension) -----

@pytest.mark.skipif(not AGDR_CORE_AVAILABLE, reason="Rust _core extension not built")
def test_mantle_engine_classical_only():
    """AgDRMantle engine with fortification disabled."""
    engine = AgDRMantle(enable_pq=False, enable_self_learning=False, enable_sovereign=False)
    result = engine.seal({"provenance": "test", "place": "Toronto", "purpose": "test"})
    assert "aki_seal" in result
    assert result["pq_applied"] is False
    assert result["tier_breakdown"]["core_aki"] == "captured"
    assert result["tier_breakdown"]["implementation_phoenix"] == "sealed"
    assert result["tier_breakdown"]["fortification_mantle"] == "not_applied"


@pytest.mark.skipif(
    not (AGDR_CORE_AVAILABLE and PQCRYPTO_AVAILABLE),
    reason="Rust _core and pqcrypto both required",
)
def test_mantle_engine_with_fortification():
    """End-to-end: AgDRMantle with full fortification enabled."""
    engine = AgDRMantle(enable_pq=True, enable_sovereign=True)
    result = engine.seal({"provenance": "agent", "place": "Toronto", "purpose": "test"})
    assert result["pq_applied"] is True
    assert result["pq_algorithm"] == "ML-DSA-65"
    assert result["tier_breakdown"]["fortification_mantle"] == "applied"

    envelope = bytes.fromhex(result["aki_seal"])
    assert engine.pq.verify(envelope) is True
