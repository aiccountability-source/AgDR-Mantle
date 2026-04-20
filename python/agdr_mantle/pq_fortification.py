"""
Post-Quantum Fortification for AgDR-Mantle.

Implements ML-DSA-65 (FIPS 204, NIST Security Level 3) quantum-resistant
signatures as an envelope around AgDR-Phoenix AKI output.

This module runs downstream of AgDR-Phoenix. It does not modify the
Phoenix hot path and therefore does not affect AKI latency.

Envelope format:
    [seal_len : 4 bytes, big-endian][classical_seal : N bytes]
    [MAGIC : 6 bytes]                   = b"AGPQ65"
    [pubkey_len : 2 bytes][pubkey : 1,952 bytes]
    [sig_len : 2 bytes][signature : ~3,309 bytes]
"""
import struct
from typing import Optional, Tuple

try:
    from pqcrypto.sign.ml_dsa_65 import generate_keypair, sign, verify
    PQCRYPTO_AVAILABLE = True
except ImportError:
    PQCRYPTO_AVAILABLE = False
    generate_keypair = sign = verify = None

PQ_MAGIC = b"AGPQ65"
ML_DSA_65_PUBKEY_SIZE = 1952
ML_DSA_65_PRIVKEY_SIZE = 4032
ML_DSA_65_SIG_SIZE = 3309


class PQFortification:
    """ML-DSA-65 post-quantum fortification wrapper.

    Wraps a classical AKI seal (produced by AgDR-Phoenix) with a quantum-resistant
    signature envelope. The signature covers the classical seal bytes, producing
    evidentiary attestation that resists known quantum attacks under FIPS 204.

    Usage:
        fortification = PQFortification()                        # ephemeral keypair
        fortification = PQFortification(keypair=(pub, priv))     # load existing

        envelope = fortification.wrap(aki_seal_bytes)
        assert fortification.verify(envelope)

        classical_seal = PQFortification.extract_aki_seal(envelope)
    """

    def __init__(self, keypair: Optional[Tuple[bytes, bytes]] = None):
        """Initialize the fortification wrapper.

        Args:
            keypair: Optional (public_key, private_key) tuple.
                     If None, an ephemeral ML-DSA-65 keypair is generated.
        """
        if not PQCRYPTO_AVAILABLE:
            raise ImportError(
                "pqcrypto package not installed. "
                "Install with: pip install pqcrypto>=0.4.0"
            )
        if keypair is None:
            self.public_key, self.private_key = generate_keypair()
        else:
            self.public_key, self.private_key = keypair

    def wrap(self, aki_seal: bytes) -> bytes:
        """Wrap an AKI seal with an ML-DSA-65 fortification envelope.

        Args:
            aki_seal: The classical AKI seal bytes from AgDR-Phoenix.

        Returns:
            Envelope bytes containing the original seal, magic marker,
            public key, and ML-DSA-65 signature.
        """
        signature = sign(self.private_key, aki_seal)
        envelope = (
            struct.pack(">I", len(aki_seal))
            + aki_seal
            + PQ_MAGIC
            + struct.pack(">H", len(self.public_key))
            + self.public_key
            + struct.pack(">H", len(signature))
            + signature
        )
        return envelope

    def verify(self, envelope: bytes) -> bool:
        """Verify an ML-DSA-65 fortification envelope.

        Returns:
            True if the signature is valid, False if tampered or malformed.
        """
        try:
            aki_seal, pubkey, signature = self._unpack(envelope)
            return verify(pubkey, aki_seal, signature)
        except Exception:
            return False

    @staticmethod
    def _unpack(envelope: bytes) -> Tuple[bytes, bytes, bytes]:
        """Parse envelope into (aki_seal, pubkey, signature)."""
        offset = 0
        seal_len = struct.unpack(">I", envelope[offset:offset + 4])[0]
        offset += 4
        aki_seal = envelope[offset:offset + seal_len]
        offset += seal_len

        magic = envelope[offset:offset + len(PQ_MAGIC)]
        if magic != PQ_MAGIC:
            raise ValueError(f"Invalid AgDR-Mantle envelope magic: {magic!r}")
        offset += len(PQ_MAGIC)

        pk_len = struct.unpack(">H", envelope[offset:offset + 2])[0]
        offset += 2
        pubkey = envelope[offset:offset + pk_len]
        offset += pk_len

        sig_len = struct.unpack(">H", envelope[offset:offset + 2])[0]
        offset += 2
        signature = envelope[offset:offset + sig_len]
        return aki_seal, pubkey, signature

    @staticmethod
    def extract_aki_seal(envelope: bytes) -> bytes:
        """Strip the fortification envelope and return the inner AKI seal.

        Useful for downstream processors that need the classical seal without
        the post-quantum wrapper (for example, Phoenix-aware verifiers).
        """
        seal, _, _ = PQFortification._unpack(envelope)
        return seal
