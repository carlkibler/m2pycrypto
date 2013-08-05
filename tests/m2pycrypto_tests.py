from unittest import TestCase
import os
from binascii import hexlify

from mock import patch

from m2pycrypto import Secret
from m2pycrypto.m2pycrypto import pkcs7_decode, pkcs7_encode
from m2pycrypto.m2pycrypto import encrypt, decrypt


class TestSecretObject(TestCase):
    """Verify the behavior of Secret class."""

    def setUp(self):
        self.iv = 'iv_45678123456781234567812345678'
        self.salt = 'salt____123456781234567812345678'
        self.ciphertext = 'yadda yadda'
        self.iterations = 1000
        self.algorithm = 'aes_256_cbc'
        assert len(self.iv) == 32
        assert len(self.salt) == 32

    def TestParamsSaved(self):
        """Parameters sent to init() should be saved."""
        secret = Secret(
            iv=self.iv,
            salt=self.salt,
            ciphertext=self.ciphertext,
            iterations=self.iterations,
            algorithm=self.algorithm)
        self.assertEqual(secret.salt, self.salt)
        self.assertEqual(secret.iv, self.iv)
        self.assertEqual(secret.ciphertext, self.ciphertext)
        self.assertEqual(secret.iterations, self.iterations)
        self.assertEqual(secret.algorithm, self.algorithm)

    @patch.object(os, 'urandom')
    def TestDefaultParams(self, urandom):
        """Known defaults should be used when no parameters are given to init()."""
        urandom.return_value = 'x' * 32
        secret = Secret()
        self.assertEqual(len(secret.iv), 32)
        self.assertEqual(len(secret.salt), 32)
        urandom.assert_called_with(32)
        self.assertEqual(secret.ciphertext, None)
        self.assertEqual(secret.iterations, 1000)

    def TestUnicodePasswordBecomesUTF8Encrypt(self):
        """Encrypt should not blow up when given a unicode password."""
        secret = Secret(
            iv=self.iv,
            salt=self.salt,
            iterations=self.iterations,
            algorithm=self.algorithm)
        secret.encrypt('my cleartext', u'UNICODE PASSWORD!!')

    #def TestUnicodePasswordBecomesUTF8Decrypt(self):
    #    """Encrypt should not blow up when given a unicode password."""
    #    secret = Secret(
    #        iv=self.iv,
    #        salt=self.salt,
    #        iterations=self.iterations,
    #        algorithm=self.algorithm,
    #        ciphertext='')
    #    secret.decrypt(u'UNICODE PASSWORD!!')

    def TestSerialize(self):
        """Serialize should pack up the instance's iv, salt, and ciphertext."""
        hex_iv = hexlify(self.iv)
        hex_salt = hexlify(self.salt)
        hex_ciphertext = hexlify(self.ciphertext)
        test_serialized = "{0}|{1}|{2}".format(hex_iv, hex_salt, hex_ciphertext)
        secret = Secret(
            iv=self.iv,
            salt=self.salt,
            iterations=self.iterations,
            algorithm=self.algorithm,
            ciphertext=self.ciphertext)
        serialized = secret.serialize()
        self.assertEqual(serialized.count('|'), 2)
        self.assertEqual(serialized, test_serialized)


    def TestDeserialize(self):
        """Deserialize should save the unpacked iv, salt, and ciphertext onto the instance."""
        test_iv = 'i' * 32
        test_salt = 's' * 32
        test_ciphertext = 'test ciphertext'
        test_serialized = "{0}|{1}|{2}".format(
            hexlify(test_iv),
            hexlify(test_salt),
            hexlify(test_ciphertext))

        # Build a secret with values from setUp
        secret = Secret(
            iv=self.iv,
            salt=self.salt,
            iterations=self.iterations,
            algorithm=self.algorithm,
            ciphertext=self.ciphertext)

        secret.deserialize(test_serialized)

        self.assertEqual(secret.salt, test_salt)
        self.assertEqual(secret.iv, test_iv)
        self.assertEqual(secret.ciphertext, test_ciphertext)


class TestEncryptionFunctions(TestCase):
    def setUp(self):
        self.iv = 'i' * 32
        self.salt = 's' * 32
        self.key = 'k' * 32
        self.algorithm = 'aes_256_cbc'
        self.plaintext = 'Hello World!'
        self.ciphertext = ''

    #def test_normal_encrypt(self):
    #    ciphertext = encrypt(self.plaintext, self.key, self.iv, self.algorithm)
    #    print ciphertext
    #    self.assertEqual(ciphertext, self.ciphertext)
    #
    #def test_normal_decrypt(self):
    #    plaintext = encrypt(self.ciphertext, self.key, self.iv, self.algorithm)
    #    print plaintext


class TestPKDS7(TestCase):
    """Exercise the PKCS#7 Padding Functions."""

    def TestEncodeEmptyString(self):
        """Text of length zero should become a full pad block."""
        self.assertEqual(pkcs7_encode(''), '\x10' * 16)

    def TestEncodeFullString(self):
        """Text of length block size should get a full pad block added."""
        self.assertEqual(pkcs7_encode('d' * 16), 'd' * 16 + '\x10' * 16)

    def TestEncodeNormalStrings(self):
        """Text of length < block size should get padded to block size."""

        # Why not be exhaustive, especially if it helps someone
        # understand the algorithm?
        self.assertEqual(pkcs7_encode('a' * 1), 'a' * 1 + '\x0f' * 15)
        self.assertEqual(pkcs7_encode('a' * 2), 'a' * 2 + '\x0e' * 14)
        self.assertEqual(pkcs7_encode('a' * 3), 'a' * 3 + '\x0d' * 13)
        self.assertEqual(pkcs7_encode('a' * 4), 'a' * 4 + '\x0c' * 12)
        self.assertEqual(pkcs7_encode('a' * 5), 'a' * 5 + '\x0b' * 11)
        self.assertEqual(pkcs7_encode('a' * 6), 'a' * 6 + '\x0a' * 10)
        self.assertEqual(pkcs7_encode('a' * 7), 'a' * 7 + '\x09' * 9)
        self.assertEqual(pkcs7_encode('a' * 8), 'a' * 8 + '\x08' * 8)
        self.assertEqual(pkcs7_encode('a' * 9), 'a' * 9 + '\x07' * 7)
        self.assertEqual(pkcs7_encode('a' * 10), 'a' * 10 + '\x06' * 6)
        self.assertEqual(pkcs7_encode('a' * 11), 'a' * 11 + '\x05' * 5)
        self.assertEqual(pkcs7_encode('a' * 12), 'a' * 12 + '\x04' * 4)
        self.assertEqual(pkcs7_encode('a' * 13), 'a' * 13 + '\x03' * 3)
        self.assertEqual(pkcs7_encode('a' * 14), 'a' * 14 + '\x02' * 2)
        self.assertEqual(pkcs7_encode('a' * 15), 'a' * 15 + '\x01' * 1)

    def TestDecodeEmptyString(self):
        """An empty string should raise ValueError."""
        with self.assertRaises(ValueError):
            pkcs7_decode('')

    def TestDecodeBackToEmptyString(self):
        """A single full block of \x10 should decode to empty string."""
        self.assertEqual(pkcs7_decode('\x10' * 16), '')

    def TestDecodeBackToBlockSizedString(self):
        """A normal block followed by block of just padding should decode
        back to a string that was exactly the block size."""
        self.assertEqual(pkcs7_decode('d' * 16 + '\x10' * 16), 'd' * 16)





        # Yeah yeah, will write these soon.
        # <insert normal unit tests here>

        #############
        # Separate bank of tests that will prove the exact equivalence of
        # m2pycrypto and m2secret. These will only run if all of these packages
        # are installed:
        #   1. M2Crypto
        #   2. m2secret
        #   3. PyCrypto
        #   4. m2pycrypto

        # Add some logic to test imports and escape if not met

        # Tests go here