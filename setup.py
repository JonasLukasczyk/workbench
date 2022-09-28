import setuptools

# read the description file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'doc/description.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="pycinema",
    version="0.1",
    author="David H. Rogers",
    author_email="dhr@lanl.gov",
    description="Cinema scientific toolset.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/cinemascience/pycinema",
    include_package_data=True,
    packages=[  "pycinema",
                "pycinema.smoke"
             ],
    install_requires=[
        "numpy",
        "scipy",
        "h5py",
        "matplotlib",
        "py",
        "Pillow",
        "ipywidgets",
        "pytest",
        "pytest-xvfb",
        "moderngl<6",
        "opencv-python",
        "torch"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    scripts=[
        "cinema"
    ],
)
