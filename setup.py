from setuptools import setup, find_packages

setup(
    name='abdes1',
    version='0.1.0',
    description='Actor based Discrete Event Simulator inspired by SimPy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Peter Bruinsma',
    author_email='peter@23min.com',
    url='https://github.com/23min/abdes1',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project's dependencies here
        # e.g., 'numpy>=1.18.5',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    extras_require={
        'dev': [
            # List additional dependencies for development here
            # e.g., 'pytest>=5.4.3',
        ],
    },
    entry_points={
        'console_scripts': [
            # If you want to create any command-line scripts, list them here.
            # e.g., 'my_script = project_name.scripts.my_script:main',
        ],
    },
)
