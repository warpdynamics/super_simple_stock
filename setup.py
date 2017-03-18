from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
    name="super_simple_stock",
    version="0.1.0",
    install_requires=requirements,
    author="Michal Wojcik",
    author_email="michal.s.wojcik@gmail.com",
    description=(""),
    license="BSD",
    keywords="",
    url="",
    packages=find_packages(),
)
