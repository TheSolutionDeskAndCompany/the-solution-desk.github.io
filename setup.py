from setuptools import setup, find_packages

setup(
    name="thesolutiondesk",
    version="0.1.0",
    packages=find_packages(),
    python_requires='>=3.11.14,<3.12',
    install_requires=[
        line.strip() for line in open('requirements.txt').readlines()
        if line.strip() and not line.startswith('#')
    ],
)
