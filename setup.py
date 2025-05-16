from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name="protos",
    version="0.1.5",
    packages=find_packages(include=["protos", "protos.*"]),
    install_requires=[
        "protobuf==5.29.0",
        "betterproto==1.2.5",
        "grpcio==1.71.0",
        "grpcio-tools==1.71.0",
        "mypy-protobuf==3.6.0",
    ],
    long_description=open(join(dirname(__file__), "README.md")).read(),
)
