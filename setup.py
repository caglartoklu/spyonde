# -*- coding: utf-8 -*-

"""
setuptools module for project.

python setup.py install
"""

# pylint: disable=line-too-long

import setuptools

setuptools.setup(
    name="spyonde",
    version="0.1.0",
    url="https://github.com/caglartoklu/spyonde",

    author="Caglar Toklu",
    author_email="caglartoklu@gmail.com",

    description="Converts cell separated regular Python scripts to Jupyter notebooks.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Jupyter',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    entry_points={
        'console_scripts': ['spyonde=spyonde.spyondemain:start_command_line'],
    },

    # test_suite='nose2.collector.collector',
    # tests_require=['nose2'],

    include_package_data=True,
    zip_safe=False,
)
