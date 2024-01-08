from setuptools import setup, find_packages
from plugin.checker import Plugin


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="flake8-restrict-imports",
    version=Plugin.version,
    author="Siva Narayanan",
    author_email="siva@fylehq.com",
    description="Flake8 plugin for restricting unwanted imports in a module.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["flake8", "imports", "python", "restrict"],
    url="https://github.com/fylein/flake8-restrict-imports",
    packages=find_packages(
        include=["plugin*"]
    ),
    install_requires=[
        "flake8==7.0.0"
    ],
    entry_points={
        "flake8.extension": [
            "PRI = plugin.checker:Plugin",
        ],
    },
    classifiers=[
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)