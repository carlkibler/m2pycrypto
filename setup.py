# -*- coding: utf-8 -*-

from setuptools import setup, tests

setup(
    name="m2pycrypto",
    description="A drop-in replacement for replacing m2secret+M2Crypto with PyCrypto.",
    version='0.1',
    author="Carl Scharenberg",
    url="https://github.com/carschar/m2pycrypto",
    download_url="https://github.com/carschar/m2pycrypto",
    install_requires=[
        'pycrypto',
        ],
    test_suite="m2pycrypto",
    platforms=['any'],
    packages=['m2pycrypto'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security :: Cryptography',
    ],
)
