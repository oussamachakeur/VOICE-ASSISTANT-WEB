from setuptools import setup, find_packages

setup(
    name="your_project_name",  # replace with your project name
    version="1.0.0",  # specify your project version
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g.,
        "fastapi",
        "uvicorn",
        # Add any other packages your project depends on
    ],
)
