from setuptools import setup


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    requirements = (line.strip() for line in open(filename))
    return [line for line in requirements if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        install_requires=parse_requirements('requirements.txt')
    )
