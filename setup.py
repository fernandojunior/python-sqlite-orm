'''
Contains informations necessaries to build, release and install a distribution.
'''
from setuptools import setup

setup(
    name='sqlite-orm',
    version='0.0.2-beta',
    author='Fernando Felix do Nascimento Junior',
    url='https://github.com/fernandojunior/python-sqlite-orm',
    license='MIT License',
    description='A Python object relational mapper for SQLite.',
    py_modules=['orm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
    ],  # see more at https://pypi.python.org/pypi?%3Aaction=list_classifiers
    zip_safe=False
)
