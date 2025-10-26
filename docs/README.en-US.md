# Independent TSA Timestamp Verifier

🔐 **Verify timestamp tokens independently - No trust required!**

[English](README.en-US.md) | [Español](README.es-ES.md)

This tool allows anyone to cryptographically verify RFC 3161 timestamp tokens without relying on the original timestamping service. Perfect for auditors, compliance officers, and anyone who needs to verify document timestamps.

## Table of Contents

- [Quick Start](#quick-start)
- [What You Need](#what-you-need)
- [Command Reference](#command-reference)
- [Supported Providers](#supported-providers)
- [Python Library](#python-library)
- [Real-World Example](#real-world-example)
- [Why Independent Verification](#why-independent-verification)
- [FAQ](#faq)

## Quick Start

### Installation
```bash
git clone https://github.com/unai-probatia/tsa-independent-verifier.git
cd tsa-independent-verifier
pip install -r requirements.txt
```

### Basic Usage

You received three items:
- A `.tsr` file (timestamp token)
- The document hash (SHA-256)
- The provider name (e.g., "SSL", "FreeTSA")
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL
```

### Expected Output
```
================================================================================
                    INDEPENDENT TIMESTAMP VERIFICATION RESULT
================================================================================

✓✓✓ STATUS: VERIFIED AND AUTHENTIC ✓✓✓

  Timestamp:        2025-09-13 05:02:15 UTC
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

## What You Need

### Required Items for Verification

1. **Timestamp Token File (.tsr)**
   - Binary file containing the RFC 3161 timestamp token
   - Provided by the timestamping service
   - File extension: `.tsr` or `.timestamp`
   - Size: Typically 3-10 KB

2. **Document Hash (SHA-256)**
   - 64-character hexadecimal string
   - Represents the fingerprint of the timestamped document
   - Example: `2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656`
   - To calculate: `sha256sum your_document.pdf`

3. **Provider Name**
   - Name of the TSA (Time Stamping Authority)
   - Examples: SSL, FreeTSA, Sectigo, GlobalSign, Apple, Microsoft
   - Case-sensitive (use exact names from provider list)
   - View all providers: `python verify_timestamp.py --list-providers`

## Command Reference

### List All Supported Providers
```bash
python verify_timestamp.py --list-providers
```

Output shows all known TSA providers with their URLs and priorities.

### Verify with Verbose Output

Get detailed information about the verification process:
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --verbose
```

Verbose mode shows:
- Policy OID
- Timestamp accuracy
- Hash algorithm
- Token size in bytes
- Complete document hash
- Provider details (URL, description)

### Compare with Original System

Verify that independent verification matches the original system:
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --compare true
```

Use `--compare false` if the original system reported the timestamp as invalid.

### Verify from JSON File

If you have verification data in JSON format:
```bash
python verify_timestamp.py --json verification_data.json
```

**JSON Format:**
```json
{
  "hash": "2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656",
  "timestamp_token": {
    "$binary": {
      "base64": "MIIXxgYJKoZIhvcNAQcCoIIX...",
      "subType": "00"
    }
  },
  "provider": "SSL"
}
```

### Quiet Mode (for Scripts)

Minimal output - only shows if valid or invalid:
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --quiet
```

**Output:** `✓ VALID` or `✗ INVALID`

**Usage in scripts:**
```bash
if python verify_timestamp.py --tsr doc.tsr --hash abc123... --provider SSL --quiet; then
    echo "Timestamp is valid - document is authentic"
    # Continue with processing
else
    echo "WARNING: Timestamp is invalid!"
    # Handle verification failure
fi
```

### Enable Debug Mode

For troubleshooting:
```bash
python verify_timestamp.py \
  --tsr document.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --debug
```

## Supported Providers

This tool supports all major RFC 3161 compliant TSA providers:

| Priority | Provider       | URL                                          | Region      |
|----------|----------------|----------------------------------------------|-------------|
| 1        | FreeTSA        | https://freetsa.org/tsr                      | Global      |
| 2        | SafeCreative    | https://tsa.safecreative.org                 | Spain       |
| 3        | OpenTimestamps  | https://alice.btc.calendar.opentimestamps.org | Blockchain  |
| 4        | Sectigo        | http://timestamp.sectigo.com/qualified       | UK          |
| 5        | SSL (DigiCert) | http://timestamp.digicert.com                | USA         |
| 6        | GlobalSign     | http://timestamp.globalsign.com/tsa/v3       | Global      |
| 7        | Apple          | http://timestamp.apple.com/ts01              | USA         |
| 8        | Microsoft      | http://timestamp.microsoft.com/scripts/timstamp.dll | USA |
| 9        | CEV            | https://tsa.cev.be/tsawebservice             | Belgium     |
| 10       | Intesi         | http://tsa.time4mind.com/timestamp           | Italy       |
| 11       | TrueTimestamp  | https://truetimestamp.org/timestamp          | Global      |
| 12       | Sigstore       | https://timestamp.sigstore.dev/timestamp     | Open Source |
| 13       | Identrust      | http://timestamp.identrust.com               | USA         |

**Note:** The tool works with ANY RFC 3161 compliant TSA, not just those listed above.

## Python Library

### Basic Usage
```python
from tsa_verifier import IndependentTSAVerifier

# Initialize verifier
verifier = IndependentTSAVerifier()

# Verify from .tsr file
result = verifier.verify_from_tsr_file(
    tsr_file_path="document.tsr",
    original_hash="2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656",
    provider_name="SSL"
)

# Check result
if result['valid']:
    print(f"✓ Verified!")
    print(f"  Timestamp: {result['timestamp']}")
    print(f"  TSA: {result['tsa_authority']}")
    print(f"  Serial: {result['serial_number']}")
else:
    print(f"✗ Verification failed: {result['error']}")
```

### Verify from Dictionary
```python
data = {
    "hash": "2f94444c1fe84c7f...",
    "timestamp_token": "base64_encoded_token",
    "provider": "SSL"
}

result = verifier.verify_from_dict(data)
```

### Compare with Original System
```python
# Verify independently
result = verifier.verify_from_tsr_file(
    tsr_file_path="document.tsr",
    original_hash="2f94444c1fe84c7f...",
    provider_name="SSL"
)

# Compare with original system's verification
comparison = verifier.compare_with_original_verification(
    verification_data=result,
    original_verified=True  # Status from original system
)

if comparison['results_match']:
    print("✓ Independent verification confirms original system")
    print(f"  Trust Level: {comparison['trust_level']}")
else:
    print("⚠ WARNING: Verification mismatch detected!")
    print(f"  Independent: {comparison['independent_verification']}")
    print(f"  Original: {comparison['original_verification']}")
```

### List Providers Programmatically
```python
verifier = IndependentTSAVerifier()
providers = verifier.list_providers()

for provider in providers:
    print(f"{provider['name']}: {provider['url']}")
```

## Real-World Example

### Scenario: Verify a Timestamped Contract

You received a contract (`contract.pdf`) with a timestamp. The sender provided:
- Timestamp file: `contract_timestamp.tsr`
- Document hash: (you'll calculate this)
- Provider: "SSL" (DigiCert)

**Step 1: Calculate the document hash**
```bash
# On Linux/Mac:
sha256sum contract.pdf

# On Windows (PowerShell):
Get-FileHash contract.pdf -Algorithm SHA256

# Output example:
# 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656  contract.pdf
```

**Step 2: Verify the timestamp**
```bash
python verify_timestamp.py \
  --tsr contract_timestamp.tsr \
  --hash 2f94444c1fe84c7f161159ebfd550e6bab1eaa285dd3a759f3e1e5f841624656 \
  --provider SSL \
  --verbose
```

**Step 3: Interpret the result**

✓ **If verification succeeds:**
- The contract existed on the stated date
- The contract hasn't been modified since
- The timestamp is cryptographically valid
- You have independent proof that doesn't rely on the timestamping service

✗ **If verification fails:**
- The hash doesn't match (wrong document or modified)
- The .tsr file is corrupted
- The provider name is incorrect
- The timestamp token is invalid

## Why Independent Verification Matters

### Trust Through Transparency

Traditional verification requires trusting the timestamping service:
```
User → Sends hash to service → Service says "yes, it's valid" → User trusts service
```

Independent verification eliminates this trust requirement:
```
User → Verifies locally with open-source tool → Cryptographic proof → No trust needed
```

### Key Benefits

✓ **No Trust Required**
- You don't need to trust the original timestamping service
- Verification is done locally on your computer
- Based on open cryptographic standards (RFC 3161)

✓ **Transparent and Auditable**
- All code is open source
- Anyone can review the verification logic
- Results are reproducible by anyone

✓ **Legally Sound**
- Provides independent cryptographic proof
- Suitable for legal proceedings
- Complies with international timestamping standards

✓ **Permanently Valid**
- As long as you have the .tsr file and hash
- Doesn't depend on service availability
- Can be verified decades later

### Use Cases

**Legal and Compliance**
- Contract timestamping
- Intellectual property protection
- Regulatory compliance (GDPR, HIPAA, SOX)
- Legal evidence preservation

**Technical and Security**
- Code signing verification
- Digital forensics
- Audit trail validation
- Document integrity verification

**Business Operations**
- Invoice timestamping
- Order confirmation
- Transaction logging
- Email archiving

## Exit Codes

The tool returns standard exit codes for use in scripts:

- `0` - Verification successful (timestamp is valid)
- `1` - Verification failed (timestamp is invalid or error occurred)
- `130` - Operation cancelled by user (Ctrl+C)

**Example usage in bash:**
```bash
#!/bin/bash

if python verify_timestamp.py --tsr "$TSR_FILE" --hash "$HASH" --provider "$PROVIDER" --quiet; then
    echo "✓ Timestamp verified successfully"
    # Continue with normal processing
    process_document.sh
else
    echo "✗ Timestamp verification failed"
    # Handle verification failure
    log_error.sh "Invalid timestamp detected"
    exit 1
fi
```

## FAQ

### General Questions

**Q: What is a timestamp token?**  
A: A timestamp token (RFC 3161) is a cryptographic proof that a document existed at a specific point in time. It's like a digital notary seal that can be verified independently.

**Q: Why is the .tsr file needed?**  
A: The .tsr file contains the cryptographic proof (timestamp token). Without it, verification is impossible. It's like a signed certificate that proves when something happened.

**Q: What if I don't have the .tsr file?**  
A: You must obtain it from whoever timestamped the document. Without the .tsr file, you cannot verify the timestamp.

**Q: Can I verify timestamps from any TSA provider?**  
A: Yes! This tool works with any RFC 3161 compliant TSA, not just the 13 providers listed. The provider list is for convenience, but any compliant TSA will work.

### Technical Questions

**Q: How does independent verification work?**  
A: The tool:
1. Reads the timestamp token from the .tsr file
2. Extracts the embedded hash from the token
3. Compares it with your document's hash
4. Verifies the TSA's cryptographic signature
5. Validates the timestamp structure (RFC 3161)

**Q: Does this tool connect to the internet?**  
A: No! All verification is done locally using cryptographic algorithms. Your documents never leave your computer.

**Q: What cryptographic algorithms are used?**  
A: The tool supports industry-standard algorithms:
- Hash: SHA-256, SHA-384, SHA-512
- Signature: RSA (2048-4096 bit), ECDSA
- Standard: RFC 3161 (Internet X.509 PKI Time-Stamp Protocol)

**Q: Can the tool be fooled or bypassed?**  
A: No. The verification is based on cryptographic proofs. If someone modifies:
- The document → Hash won't match
- The timestamp → Signature verification fails
- The .tsr file → Cryptographic structure is invalid

### Troubleshooting

**Q: Verification failed - what should I check?**  
A:
1. Ensure the hash matches the document exactly
2. Verify the .tsr file isn't corrupted (check file size > 0)
3. Confirm the provider name is correct (case-sensitive)
4. Try with `--debug` flag for detailed error information

**Q: I get "File not found" error**  
A: Check the file paths are correct. Use absolute paths if needed:
```bash
python verify_timestamp.py \
  --tsr /full/path/to/document.tsr \
  --hash abc123... \
  --provider SSL
```

**Q: The tool says "Unknown provider"**  
A: The provider name must match exactly (case-sensitive). Use `--list-providers` to see exact names. Common mistakes:
- ❌ "ssl" → ✓ "SSL"
- ❌ "DigiCert" → ✓ "SSL"
- ❌ "freetsa" → ✓ "FreeTSA"

### Security Questions

**Q: How do I know this tool isn't manipulated?**  
A: 
1. The code is open source - audit it yourself
2. Have a security expert review it
3. Compare results with other RFC 3161 verification tools
4. Check the GitHub repository's commit history

**Q: What if the timestamping service was hacked?**  
A: Independent verification protects you! Even if the service is compromised:
- Old timestamps remain valid (cryptographic proof)
- You can verify without contacting the service
- The verification doesn't depend on service integrity

**Q: Can this be used as legal evidence?**  
A: Yes! The tool provides cryptographic proof that meets international standards. However, always consult with legal experts for your specific jurisdiction.

## Support and Contributing

### Getting Help

- 📖 **Documentation**: [https://docs.probatia.com](https://docs.probatia.com)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/unai-probatia/tsa-independent-verifier.git/issues)
- 📧 **Email**: hello@probatia.com

### Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Security Vulnerabilities

If you discover a security vulnerability:
- 🔒 **DO NOT** open a public issue
- 📧 Email: security@yourcompany.com
- 🔐 Use PGP if possible (key on website)

We take security seriously and will respond promptly.

## License

MIT License

Copyright (c) 2025 Your Company Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-21  
**Made with ❤️ for transparency in digital timestamping**