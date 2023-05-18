from setuptools import setup, find_packages

VERSION = "0.1.0-alpha"
DESCRIPTION = "The building block for decentralized media"
GITHUB_LINK = "https://github.com/SynapseMedia/nucleus"

LICENSE = "AGPL-3"
AUTHOR = "synapse"
MAINTAINER_EMAIL = "gmjun2000@gmail.com"

setup(
    name="nucleus",
    author=AUTHOR,
    version=VERSION,
    description=DESCRIPTION,
    author_email=MAINTAINER_EMAIL,
    url=GITHUB_LINK,
    license=LICENSE,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    install_require=[
        "ffmpeg-python==0.2.0",
        "pydantic==1.10.1",
        "hexbytes==0.2.2",
        "multiformats==0.2.1",
        "dag-cbor==0.3.2",
        "Pillow==9.2.0",
        "requests==2.27.1"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ],
)
