from setuptools import Command, find_packages, setup
from shutil import rmtree
import pathlib
import os
import sys

NAME = "parameter-store-environ"
PACKAGE = "ps_environ"
DESCRIPTION = "A simple configuration variable wrapper around AWS SSM Parameter Store"
URL = "https://github.com/talroo/parameter-store-environ"
EMAIL = "ebarajas@talroo.com"
AUTHOR = "ebarajas"
VERSION = "0.1.2"
REQUIRES_PYTHON = ">=3.6.0"
LICENSE = "MIT"

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

REQUIRED = [
    "boto3"
]

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(HERE / 'dist')
        except OSError:
            pass

        self.status('Building Source and Wheel distribution…')
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')
        
        sys.exit()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # $ setup.py upload support.
    cmdclass={
        'upload': UploadCommand,
    },
)
