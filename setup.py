from setuptools import find_packages, setup

setup(
    name="online_retail",
    packages=find_packages(exclude=["online_retail_tests"]),
    install_requires=["dagster", "dagster-cloud"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
