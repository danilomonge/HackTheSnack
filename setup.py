from setuptools import setup, find_packages

setup(
    name="fakethesnack",
    version="0.1",
    packages=find_packages(where="hts_lib"),
    package_dir={"": "hts_lib"},
)