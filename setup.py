from setuptools import setup, find_packages

setup(
    name="simpleclock",
    version="0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    author="lpc",
    author_email="l.pinto.castaneda@gmail.com",
    description="A simple clock",
    license="MIT",
    keywords="clock",
)
