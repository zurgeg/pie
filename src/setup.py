from setuptools import setup

setup(
    name='pie',
    version='0.1.0',
    py_modules=['pie'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'pie = pie:cli',
        ],
    },
)