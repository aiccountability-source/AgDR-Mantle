# AgDR Provenance Packet Spec v1.0.0

Minimal. Immutable. Plug-and-play.

Size target: under 512 bytes. Fits any kernel-fast path.

Hash algorithm: BLAKE3 (default) or SHA-256.

Full packet hash excludes only the signature and fec_parity fields.

Verification steps:
1. Check signature.
2. Validate sequence_number and parent_hash.
3. Confirm PPP hashes match registered values.
4. Ingest decision_hash.
5. Emit next packet.

Gap or mismatch triggers PoP Switch Protocol.
Data received. Hold form. Repair agreement.

Transit: dropless UDP + FEC or QUIC 0-RTT.
