from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="arxiv_bot",
    version="1.6",
    packages=find_packages(),
    install_requires=requirements,
    test_suite='tests',
)
