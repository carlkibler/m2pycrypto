m2pycrypto
==========

![Build Status](https://secure.travis-ci.org/carschar/m2pycrypto.png?branch=master)

This library is a drop-in replacement for the m2secret helper library.
m2secret is a handy wrapper around M2Crypto to make secure 256-bit AES
encryption very simple.

The m2pycrypto library has an identical interface and behavior to
m2secret, but with the underlying encryption library swapped out:
instead of M2Crypto it relies on the much more current PyCrypto.

The code is about 95% identical to m2secret and the interface is 100%
identical. Therefore, most of the credit goes to [Heikki Toivonen](http://www.heikkitoivonen.net/),
the original author of m2secret.


Why switch to PyCrypto?
=======================
* M2Crypto is unmaintained. No commits since January 2011.
* M2Crypto is a pain to compile on OS X and some other platforms.
* PyCrypto is the opposite: actively maintained and easy to install.
* PyCrypto supports Python 2.1 through 3.3.


How to replace m2secret with m2pycrypto
=======================================

1. Add 'm2pycrypto' to your environment with pip.
2. Replace "import m2secret" with "import m2pycrypto"
3. Run your tests
4. Verify your encrypted data

Yes, it should be that simple!


Installation
============
```
# Test and then install
python setup.py test
python setup.py install
```


Usage
=====
Here is simple usage to encrypt and decrypt.
```python
# Encrypt (auto-generate initialization vector and salt)
import m2pycrypto
secret = m2pycrypto.Secret()
ciphertext = secret.encrypt(plaintext, password)
# Better store these for later - you need them for decryption!
my_iv = secret.iv
my_salt = secret.salt


# Decrypt
import m2pycrypto
secret = m2secret.Secret(salt=my_salt, iv=my_iv)
plaintext = secret.decrypt(password)
```

More common use is encrypting before storing in a database, like 
for passwords. Instead of worrying about storing the 3 important
elements: ciphertext, salt, and iv, m2pycrypto has a serialize()
function which combines these into a single, ascii-safe string.

Similarly, there is a deserialize() function which re-parses that
specially-formatted string to extract the salt, iv, and ciphertext
which it needs to decrypt the data.

```python
# Encrypt (auto-generate initialization vector and salt)
import m2pycrypto
secret = m2pycrypto.Secret()
secret.encrypt(plaintext, password)
# This string can be saved to file or database
serialized_ciphertext = secret.serialize()


# Decrypt
import m2pycrypto
secret = m2secret.Secret()
secret.deserialize(serialized_ciphertext)
plaintext = secret.decrypt(password)
```


Links
=====
[Homepage of m2secret](http://www.heikkitoivonen.net/m2secret/)  
[Source code of m2secret (subversion)](http://svn.heikkitoivonen.net/svn/m2secret/trunk/)  
[PyCrypto Homepage](https://www.dlitz.net/software/pycrypto/)  
[PyCrypto on PyPI](https://pypi.python.org/pypi/pycrypto)  







