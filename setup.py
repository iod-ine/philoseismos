""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='philoseismos',
    version='0.0.29_alpha',
    author="Ivan Dubrovin",
    author_email="io.dubrovin@icloud.com",
    description="Engineering seismologist's toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iod-ine/philoseismos",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
    ],
    python_requires='>=3.6',
)
