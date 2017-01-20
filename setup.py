from setuptools import setup

setup(
    name='vcapi',
    packages=['vcapi'],
    version='0.0.0a1',
    description="Python API wrapper for Veracode's API",
    long_description=open('README.rst').read(),
    author="Anthony Lozano",
    author_email='amlozano1@gmail.com',
    keywords=['veracode', 'api', 'wrapper'],
    install_requires=['requests>=2.11.1',
                      'bs4',
                      'python-dateutil'],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    url='https://github.com/AnthonyLozano/vcapi',
    entry_points={
        'console_scripts': [
            'vcapi=vcapi.vcapi:main',
        ],
    },
)
