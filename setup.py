import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'matplotlib >= 3.2.0',
    'PyGithub >= 1.51'
]

setuptools.setup(
    name='linguist-breakdown',
    version='1.0.0',
    description='View the language breakdown of your entire GitHub account.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/justintime50/linguist',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': [
            'pylint >= 2.5.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'linguist=linguist.breakdown:main'
        ]
    },
    python_requires='>=3.6',
)
