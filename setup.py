from setuptools import setup, find_packages

with open("README.rst") as f:
    readme = f.read()

setup(
    name="simpleclock",
    version="0",
    author="lpc",
    author_email="l.pinto.castaneda@gmail.com",
    description="A simple clock",
    long_description=readme,
    long_description_content_type="text/x-rst",
    license="MIT",
    keywords="clock",
    url="https://github.com/ma3da/simpleclock",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
)
