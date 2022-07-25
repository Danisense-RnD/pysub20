from setuptools import setup
long_description = open('README.rst').read()
if __name__ == "__main__":
    setup(
        setup_requires=['pbr'],
        pbr=True,
        long_description=long_description
    )