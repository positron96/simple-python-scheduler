from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

install_requires = (here / 'requirements.txt').read_text(encoding='utf-8').splitlines()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='schedulr',
    version='0.0.1',
    description='A sample Python scheduler utility', 
    long_description=long_description,
    long_description_content_type='text/markdown', 
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='>=3.6, <4',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'schedulr=schedulr.cli:main'
        ],
    },
)