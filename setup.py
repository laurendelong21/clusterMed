#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['bayespy==0.5.22',
                'click==8.1.3',
                'kmodes==0.12.1',
                'matplotlib==3.5.2',
                'numpy==1.22.3',
                'pandas==1.4.2',
                'plotnine==0.8.0',
                'scikit-learn==1.1.1',
                'scikit-learn-extra==0.2.0',
                'scipy==1.9.0',
                'seaborn==0.11.2',
                'statsmodels==0.14.1',
                'tqdm==4.64.0']

test_requirements = ['pytest>=3', ]

setup(
    author="Lauren Nicole DeLong",
    author_email='l.n.delong@sms.ed.ac.uk',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
    ],
    description="UK BioBank Multimorbidity Clustering",
    entry_points={
        'console_scripts': [
            'clustr=clustr.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='clustr',
    name='clustr',
    packages=find_packages(include=['clustr', 'clustr.*']),
    test_suite='tests',
    tests_require=test_requirements,
    version='1.0.0',
    zip_safe=False,
)
