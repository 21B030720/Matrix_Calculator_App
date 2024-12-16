from setuptools import setup, find_packages

setup(
    name='matrixlib_arslan_and_timur',
    version='1.0.0',
    description='A library for matrix operations, prepared for final',
    author='Arslan Toimbekov and Timur Baitukenov',
    author_email='jacklol5760@gmail.com',
    packages=find_packages(include=['matrixlib_arslan_and_timur']),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    extras_require={
        "gui": ["tkinter"],  # Extra feature 'gui' that requires tkinter
    },
)