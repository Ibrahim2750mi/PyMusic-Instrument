import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='PyMusic-Instrument',
    version='0.3',
    long_description=README,
    long_description_content_type="text/markdown",
    description='A python library which can generate sounds played by instruments',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    author='Mohammad Ibrahim',
    author_email='cshore.2750mi@gmail.com',
    url="https://www.github.com/Ibrahim2750mi/PyMusic-Instrument",

    packages=["Instrument"],
    install_requires=['wheel', "pyaudio", "numpy"],
    scripts=[]
)


