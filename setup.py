from setuptools import setup, find_namespace_packages

print("Found", find_namespace_packages(
        where='src',
        exclude=["*skeleton*"]
    ))

setup(
    name='pie',
    version='0.1.0',
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