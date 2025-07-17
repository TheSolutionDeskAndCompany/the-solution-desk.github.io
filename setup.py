from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [
        line.strip()
        for line in f.readlines()
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="thesolutiondesk",
    version="0.1.0",
    packages=find_packages(),
    python_requires='>=3.11.0',  # Matches Python 3.11.4
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
