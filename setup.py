from setuptools import setup, find_packages


setup(
    name='wizard_lint',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wizard_lint=wizard_lint.main:main',
        ],
    },
)