m2pycrypto
==========

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


Links
=====
[Homepage of m2secret](http://www.heikkitoivonen.net/m2secret/)
[Source code of m2secret (subversion)](http://svn.heikkitoivonen.net/svn/m2secret/trunk/)
[PyCrypto Homepage](https://www.dlitz.net/software/pycrypto/)
[PyCrypto on PyPI](https://pypi.python.org/pypi/pycrypto)







