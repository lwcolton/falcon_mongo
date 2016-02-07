from setuptools import setup, find_packages

setup(
    name = "falcon-mongo",
    version = "0.0.1",
    description = "Falcon HTTP resources for mongo documents",
    author = "Colton Leekley-Winslow",
    package_dir = {"":"src"},
    packages = find_packages("src"),
)
