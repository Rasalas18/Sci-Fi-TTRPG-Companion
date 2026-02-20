from setuptools import find_packages, setup

with open("README.md") as file:
    readme = file.read()

setup(
    name="Space_Adv_Program",
    version="1.0.0",
    packages=find_packages(exclude=["tests", ".github"]),
    url="https://github.com/Rasalas18/SpaceSystemProgramPython/",
    license="LICENSE.txt",
    description="My program for my ttrpg game",
    long_description=readme,
    long_description_content_type="text/markdown",  # Specifica il tipo di contenuto del file README
    author="Rasalas",
    author_email="lanna.pietro@libero.it",
)
