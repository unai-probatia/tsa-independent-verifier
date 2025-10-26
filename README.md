# Independent TSA Timestamp Verifier

🔐 **Verify timestamp tokens independently - No trust required!**

This tool allows anyone to cryptographically verify RFC 3161 timestamp tokens without relying on the original timestamping service. Perfect for auditors, compliance officers, and anyone who needs to verify document timestamps.

## Quick Start

### Installation
```bash
git clone https://github.com/unai-probatia/tsa-independent-verifier.git
cd tsa-independent-verifier
pip install -r requirements.txt
```

### Basic Usage (You have: .tsr file + hash + provider)

This is the most common scenario. You received:
- A `.tsr` file (timestamp token)
- The document hash (SHA-256)
- The provider name (e.g., "SSL", "FreeTSA")
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL
```

**Output:**
```
================================================================================
                    INDEPENDENT TIMESTAMP VERIFICATION RESULT
================================================================================

✓✓✓ STATUS: VERIFIED AND AUTHENTIC ✓✓✓

  Timestamp:        2025-09-13 05:02:15
  TSA Authority:    DigiCert SHA512 RSA4096
  Serial Number:    169790533997128162934813285611086882
  Provider:         SSL

────────────────────────────────────────────────────────────────────────────────
  VERIFICATION RESULT:
  ✓ This timestamp has been independently verified
  ✓ The document existed at the stated time
  ✓ The document has not been altered since timestamping
  ✓ The cryptographic signature is valid
────────────────────────────────────────────────────────────────────────────────
================================================================================
```

## Command Reference

### Show all supported providers
```bash
python verify_timestamp.py --list-providers
```

### Verbose output (detailed information)
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash abc123... \
  --provider SSL \
  --verbose
```

### Compare with original system
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash abc123... \
  --provider SSL \
  --compare true
```

### Verify from JSON file
```bash
python verify_timestamp.py --json verification_data.json
```

### Quiet mode (scripts/automation)
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash abc123... \
  --provider SSL \
  --quiet
# Outputs: ✓ VALID or ✗ INVALID
```

## What You Need to Verify

### Required Files/Data:

1. **Timestamp Token File (.tsr)**
   - Binary file containing the RFC 3161 timestamp token
   - Usually provided by the timestamping service
   - File extension: `.tsr` or `.timestamp`

2. **Document Hash**
   - SHA-256 hash of the original document
   - 64-character hexadecimal string
   - Example: `2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656`

3. **Provider Name**
   - Name of the TSA that created the timestamp
   - Examples: SSL, FreeTSA, Sectigo, GlobalSign, Apple, Microsoft
   - See all providers: `python verify_timestamp.py --list-providers`

## Supported TSA Providers

| Priority | Provider       | URL                                          |
|----------|----------------|----------------------------------------------|
| 1        | FreeTSA        | https://freetsa.org/tsr                      |
| 2        | SafeCreative    | https://tsa.safecreative.org                 |
| 3        | OpenTimestamps  | https://alice.btc.calendar.opentimestamps.org |
| 4        | Sectigo        | http://timestamp.sectigo.com/qualified       |
| 5        | SSL            | http://timestamp.digicert.com                |
| 6        | GlobalSign     | http://timestamp.globalsign.com/tsa/v3       |
| 7        | Apple          | http://timestamp.apple.com/ts01              |
| 8        | Microsoft      | http://timestamp.microsoft.com/scripts/timstamp.dll |
| 9        | CEV            | https://tsa.cev.be/tsawebservice             |
| 10       | Intesi         | http://tsa.time4mind.com/timestamp           |
| 11       | TrueTimestamp  | https://truetimestamp.org/timestamp          |
| 12       | Sigstore       | https://timestamp.sigstore.dev/timestamp     |
| 13       | Identrust      | http://timestamp.identrust.com               |

## Python Library Usage
```python
from tsa_verifier import IndependentTSAVerifier

# Initialize
verifier = IndependentTSAVerifier()

# Verify from .tsr file (most common)
result = verifier.verify_from_tsr_file(
    tsr_file_path="document.tsr",
    original_hash="2f94444c1fe84c7f...",
    provider_name="SSL"
)

# Check result
if result['valid']:
    print(f"✓ Verified! Timestamp: {result['timestamp']}")
    print(f"  TSA: {result['tsa_authority']}")
else:
    print(f"✗ Failed: {result['error']}")

# Compare with original system
comparison = verifier.compare_with_original_verification(
    verification_data=result,
    original_verified=True  # From original system
)
print(f"Results match: {comparison['results_match']}")
```

## Exit Codes

- `0` - Verification successful
- `1` - Verification failed
- `130` - Cancelled by user

Useful for scripts:
```bash
if python verify_timestamp.py --tsr doc.tsr --hash abc123... --provider SSL --quiet; then
    echo "Timestamp is valid"
else
    echo "Timestamp is invalid"
fi
```

## Real-World Example

Imagine you received a contract with a timestamp. To verify independently:

1. **Get the .tsr file**: `contract_timestamp.tsr`
2. **Calculate document hash**:
```bash
   sha256sum contract.pdf
   # Output: 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656
```
3. **Know the provider**: SSL (DigiCert)
4. **Verify**:
```bash
   python verify_timestamp.py \
     --tsr contract_timestamp.tsr \
     --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
     --provider SSL
```

✓ Result: You now have cryptographic proof the contract existed on the stated date!

## Why Independent Verification Matters

### Trust Through Transparency
- ✓ You don't need to trust the original service
- ✓ Anyone can verify using open-source code
- ✓ Based on RFC 3161 cryptographic standards
- ✓ Results are reproducible by anyone

### Use Cases
- Legal contracts and agreements
- Intellectual property protection
- Regulatory compliance
- Digital forensics
- Audit trails
- Document integrity verification

## FAQ

**Q: Why is the .tsr file needed?**  
A: The .tsr file contains the cryptographic proof (RFC 3161 timestamp token) that can be independently verified.

**Q: What if I don't have the .tsr file?**  
A: You need it for verification. Ask the party who timestamped the document to provide it.

**Q: Can I verify timestamps from any TSA?**  
A: Yes! This tool works with any RFC 3161 compliant TSA, not just the ones listed.

**Q: How do I know this verifier isn't manipulated?**  
A: The code is open source. Audit it yourself or have a security expert review it.

**Q: What if verification fails?**  
A: Possible reasons:
- Incorrect hash (wrong document)
- Corrupted .tsr file
- Wrong provider name
- Timestamp token is invalid/tampered

**Q: Does this tool connect to the internet?**  
A: No! All verification is done locally using cryptography.

## Support

- 📖 Documentation: [https://docs.probatia.com](https://docs.yourcompany.com)
- 🐛 Report Issues: [GitHub Issues](https://github.com/unai-probatia/tsa-independent-verifier/issues)

## License

MIT License - See LICENSE file

---

**Made with ❤️ for transparency in digital timestamping**