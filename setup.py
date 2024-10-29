from setuptools import setup, find_packages

setup(
    name="ai-conventional-commit",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'click',
        'anthropic',
    ],
    entry_points={
        'console_scripts': [
            'ai-commit=ai_commit.cli:cli',
            ],
    },
)