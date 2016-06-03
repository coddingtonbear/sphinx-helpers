from setuptools import setup, find_packages


setup(
    name='sphinx-helpers',
    version='0.1',
    url='https://github.com/coddingtonbear/sphinx-helpers',
    description=(
        'Create sphinx roles and directives more easily.'
    ),
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    namespace_packages=['sphinxcontrib'],
)
