from setuptools import setup, find_namespace_packages

setup(
    name='pie',
    version='1.0.0',
    package_dir = {"": "src"},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'pie = pie.pie:cli',
        ],
    },
)