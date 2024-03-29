# Cinema v2.0 prototyping and design repository
![smoke](https://github.com/cinemascience/workbench/actions/workflows/CinemaSmokeTest.yml/badge.svg)
![base](https://github.com/cinemascience/workbench/actions/workflows/CinemaBaseTest.yml/badge.svg)
![rendering](https://github.com/cinemascience/workbench/actions/workflows/CinemaRenderTest.yml/badge.svg)

Cinema v2.0 is a newly designed toolkit of python-based components for creating, filtering, transforming and viewing Cinema databases. The toolkit shall maintain compatibility with Cinema data specifications.

The code in this repository is released under open source license. See the license file for more information.

All code and examples are prototype and for design purposes only

# Creating a local python environment for the workbench

To create a local python environment for this project, run the following commands within the repository directory:
```
python3 -m venv csenv
source csenv/bin/activate
python setup.py install
pip install jupyterlab
```

# Running the example

You can now use this python environment to run the 'hello world' example, using the `make_test_area` script. This will create a directory under `testing/`, copy files, and run a jupyter notebook example:

```
source csenv/bin/activate
./bin/make_test_area
```

# Contributing to the workbench

Contributions can be made by submitting issues and contributing code through pull requests. The code shall be reviewed by the core Cinema team, and accepted when both content and code standards are met.


