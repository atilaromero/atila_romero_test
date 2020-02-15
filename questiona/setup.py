import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atila_romero_overlap",
    version="1.1.0",
    description="A program to check if two 1D lines intercept each other",
    author="Atila Leites Romero", 
    author_email="atilaromero@gmail.com",
    url="https://github.com/atilaromero/atila_romero_test/tree/master/questiona",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)