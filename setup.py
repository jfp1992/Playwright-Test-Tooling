import setuptools

REQUIREMENTS = ["playwright", "colorama"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Playwright-Test-Tooling",
    version="2.0",
    author="James Potter",
    install_requires=REQUIREMENTS,
    long_description=long_description,
    packages=["base"],
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: Any OS",
    ],
)
