from setuptools import setup, find_packages

setup(
    name='moroccan_resume_parser',
    version='0.1.0',
    description='A customized resume parser for the Moroccan market based on Pyresparser.',
    author='Hamza EL IDRISSI',
    author_email='hamza.ezzharelidrissi1@gmail.com',
    url='https://github.com/HMZElidrissi/moroccan_resume_parser',
    packages=find_packages(),
    install_requires=[
        'pyresparser',
        'nltk',
        'spacy==2.3.5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
