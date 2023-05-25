from setuptools import find_packages, setup

setup(
    name="biorxiv-retreiver",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
)
