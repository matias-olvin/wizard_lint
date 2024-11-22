from setuptools import find_packages, setup


with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="wizard_lint",
    version="0.1.0",
    author="matias-olvin",
    author_email="matias@olvin.com",
    description="A package to add jinja templating to SQL code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matias-olvin/wizard_lint",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10,<3.14',
    install_requires=[
        "pyyaml>=6.0.1,<7.0.0",
        "rich>=13.7.1,<14.0.0",
        "jinja2>=3.1.4,<4.0.0",
    ],
    extras_require={
        "dev": [
            "black>=24.2.0,<25.0.0",
            "isort>=5.13.2,<6.0.0",
            "flake8>=7.0.0,<8.0.0",
            "pytest>=8.3.3,<9.0.0",
            "wheel>=0.45.0,<0.46.0",
        ],
    },
)
