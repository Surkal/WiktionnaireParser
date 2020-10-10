import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setuptools.setup(
    name="wiktionnaireparser", # Replace with your own username
    version="0.0.3",
    author="Surkal",
    description="A library for parsing the french wiktionnary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Surkal/WiktionnaireParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Text Processing",
        "Natural Language :: English",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
)
