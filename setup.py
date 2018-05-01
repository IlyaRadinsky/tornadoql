from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='tornadoql',
    version='0.1.2',
    packages=['tornadoql'],
    url='https://github.com/IlyaRadinsky/tornadoql',
    license='MIT',
    keywords='graphql development web server api',
    author='Ilya Radinsky - Modifications by Michael Toutonghi',
    author_email='',
    description='Package for easily creating GraphQL APIs with Subscription support using TornadoQL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: GraphQL Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4'
    ],
    install_requires=['tornado', 'graphene', 'rx'],
    package_data={
        'tornadoql': ['static/graphiql.html'],
    }
)
