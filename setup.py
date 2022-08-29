from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="sample",
    version="0.1.0",
    description="Destination memes",
    long_description=readme,
    author="Daniel Coo, Carter Hall",
    author_email="danieljohncoo@gmail.com",
    url="https://github.com/DC00/meme-compiler",
    packages=find_packages(exclude=("tests", "docs"))
)

