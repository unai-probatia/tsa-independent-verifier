#!/usr/bin/env python3
"""
Independent TSA Timestamp Verifier - Command Line Tool
=======================================================

Verify RFC 3161 timestamp tokens independently, without relying on
the original timestamping service.

COMMON USAGE (with .tsr file):
    python verify_timestamp.py --tsr document.tsr --hash <hash> --provider SSL

OTHER OPTIONS:
    python verify_timestamp.py --json verification_data.json
    python verify_timestamp.py --list-providers

For help: python verify_timestamp.py --help
"""

import argparse
import sys

from tsa_verifier import (
    IndependentTSAVerifier,
    print_verification_result,
    print_provider_list
)


def main():
    parser = argparse.ArgumentParser(
        description='Independent TSA Timestamp Verifier - Verify timestamps without trusting the original service',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:

  Verify with .tsr file (most common):
    python verify_timestamp.py --tsr document.tsr --hash abc123... --provider SSL

  Show all supported providers:
    python verify_timestamp.py --list-providers

  Verify from JSON file:
    python verify_timestamp.py --json verification_data.json

  Compare with original system:
    python verify_timestamp.py --tsr document.tsr --hash abc123... --provider SSL --compare true

  Verbose output with all details:
    python verify_timestamp.py --tsr document.tsr --hash abc123... --provider SSL --verbose

For more information, visit: https://github.com/yourcompany/tsa-independent-verifier
        """
    )

    # Primary method: .tsr file
    parser.add_argument(
        '--tsr',
        type=str,
        help='Path to timestamp token file (.tsr)'
    )
    parser.add_argument(
        '--hash',
        type=str,
        help='SHA-256 hash of the original document'
    )
    parser.add_argument(
        '--provider',
        type=str,
        help='TSA provider name (e.g., SSL, FreeTSA, Sectigo). Use --list-providers to see all.'
    )

    # Alternative: JSON file
    parser.add_argument(
        '--json',
        type=str,
        help='JSON file containing hash, token, and provider'
    )

    # List providers
    parser.add_argument(
        '--list-providers',
        action='store_true',
        help='Show list of known TSA providers'
    )

    # Options
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed verification information'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--compare',
        type=str,
        choices=['true', 'false'],
        help='Compare with original verified status (true/false)'
    )
    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        help='Minimal output (only show if valid or not)'
    )

    args = parser.parse_args()

    # Handle list providers
    if args.list_providers:
        print_provider_list()
        return 0

    # Validate input
    if not args.tsr and not args.json:
        parser.error("Either --tsr (with --hash and --provider) or --json is required")

    if args.tsr and (not args.hash or not args.provider):
        parser.error("--tsr requires both --hash and --provider")

    # Initialize verifier
    verifier = IndependentTSAVerifier(debug=args.debug)

    try:
        # Verify based on input method
        if args.tsr:
            # Primary method: .tsr file
            if not args.quiet:
                print(f"\n🔍 Verifying timestamp token from: {args.tsr}")
                print(f"📄 Document hash: {args.hash[:32]}...")
                print(f"🏢 Provider: {args.provider}\n")

            result = verifier.verify_from_tsr_file(
                tsr_file_path=args.tsr,
                original_hash=args.hash,
                provider_name=args.provider
            )
        else:
            # Alternative: JSON file
            if not args.quiet:
                print(f"\n🔍 Verifying from JSON file: {args.json}\n")

            result = verifier.verify_from_json_file(args.json)

        # Print result
        if args.quiet:
            # Minimal output
            if result.get('valid', False):
                print("✓ VALID")
                sys.exit(0)
            else:
                print("✗ INVALID")
                sys.exit(1)
        else:
            # Full output
            print_verification_result(result, verbose=args.verbose)

        # Compare with original system if requested
        if args.compare:
            original_verified = args.compare.lower() == 'true'
            comparison = verifier.compare_with_original_verification(
                verification_data=result,
                original_verified=original_verified
            )

            print("=" * 80)
            print(" " * 20 + "COMPARISON WITH ORIGINAL SYSTEM")
            print("=" * 80)
            print(f"\n  Independent Verification: {comparison['independent_verification']}")
            print(f"  Original System:          {comparison['original_verification']}")
            print(f"  Results Match:            {comparison['results_match']}")
            print(f"  Trust Level:              {comparison['trust_level']}")
            print(f"\n  {comparison['note']}")
            print("\n" + "=" * 80 + "\n")

        # Exit with appropriate code
        sys.exit(0 if result.get('valid', False) else 1)

    except KeyboardInterrupt:
        print("\n\n⚠ Verification cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()