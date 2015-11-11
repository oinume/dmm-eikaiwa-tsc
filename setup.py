import os
import sys


def read_file(name):
    return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)).read()

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3, 5):
    print("dmm-eikaiwa-tsc requires at least Python 3.5 to run.")
    sys.exit(1)

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

# TODO
tests_require = [
    'flexmock', 'pytest', 'pytest-cov',
    'sphinx', 'sphinx_rtd_theme',
]

install_requires = read_file("requirements.txt").splitlines()

setup(
    name="dmm-eikaiwa-tsc",
    version="1.0.0",
    url="https://github.com/oinume/dmm-eikaiwa-tsc/",
    license="MIT",
    author="Kazuhiro Oinuma",
    author_email="oinume@gmail.com",
    description="Teacher Schedule Checker for DMM Eikaiwa",
    long_description=read_file("README.md"),
    packages=["tsc"],
#    scripts=[os.path.join("bin", p) for p in ["tomahawk", "tomahawk-rsync"]],
    zip_safe=False,
    platforms="unix",
    install_requires=install_requires,
#    tests_require=tests_require,
#    data_files=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Topic :: Education",
    ],
)
