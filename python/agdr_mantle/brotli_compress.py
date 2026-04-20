"""
Forensic compression for AgDR-Mantle sovereign archives.

Uses Brotli compression (quality 11 by default) to minimize bandwidth
for Northern, Commonwealth, and other bandwidth-constrained deployments
while preserving full forensic recoverability.
"""
import brotli


def compress_forensic_bundle(data: bytes, quality: int = 11) -> bytes:
    """Compress a forensic bundle for archive storage."""
    return brotli.compress(data, quality=quality)


def decompress_forensic_bundle(data: bytes) -> bytes:
    """Decompress a forensic bundle back to original bytes."""
    return brotli.decompress(data)
