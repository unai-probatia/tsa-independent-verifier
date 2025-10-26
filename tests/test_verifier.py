# tests/test_verifier.py
import base64
import unittest

from tsa_verifier import IndependentTSAVerifier


class TestIndependentTSAVerifier(unittest.TestCase):

    def setUp(self):
        self.verifier = IndependentTSAVerifier(debug=False)

    def test_token_decode_mongodb_format(self):
        """Test decoding MongoDB binary format"""
        token_data = {
            "$binary": {
                "base64": "VGVzdFRva2Vu",  # "TestToken" in base64
                "subType": "00"
            }
        }
        result = self.verifier._decode_token(token_data)
        self.assertEqual(result, b'TestToken')

    def test_token_decode_base64_string(self):
        """Test decoding base64 string"""
        token_data = base64.b64encode(b'TestToken').decode()
        result = self.verifier._decode_token(token_data)
        self.assertEqual(result, b'TestToken')

    def test_token_decode_bytes(self):
        """Test handling raw bytes"""
        token_data = b'TestToken'
        result = self.verifier._decode_token(token_data)
        self.assertEqual(result, b'TestToken')

    def test_missing_hash(self):
        """Test error handling for missing hash"""
        data = {
            "timestamp_token": "base64token"
        }
        result = self.verifier.verify_from_dict(data)
        self.assertFalse(result['valid'])
        self.assertIn('hash', result['error'].lower())

    def test_missing_token(self):
        """Test error handling for missing token"""
        data = {
            "hash": "abc123"
        }
        result = self.verifier.verify_from_dict(data)
        self.assertFalse(result['valid'])
        self.assertIn('token', result['error'].lower())


if __name__ == '__main__':
    unittest.main()