from setuptools import setup, find_packages

VERSION = "0.1.0"
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
)
