import sys
from setuptools import setup, find_packages

install_requires = [
    'annotated-types>=0.6.0',
    'configparser>=6.0.1',
    'dnspython>=2.6.1',
    'pydantic>=2.6.4',
    'pydantic-settings>=2.2.1',
    'pydantic_core>=2.16.3',
    'pymongo>=4.6.3',
    'python-dotenv>=1.0.1',
    'typing_extensions>=4.10.0'
]

DESCRIPTION = "A database migration tool for MongoDB"

def get_read_me():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return DESCRIPTION

setup(
    name='mongo_migrate',
    version='1.0.0',
    description=DESCRIPTION,
    long_description=get_read_me(),
    long_description_content_type="text/markdown",
    author='Dankov Sergey',
    author_email='beyond31@mail.ru',
    license='GNU General Public License v3 (GPLv3)',
    package_dir={"": "src"},
    packages=find_packages(
        where='src',
    ),
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)