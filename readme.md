# Cinema v2.0 prototyping and design repository
![smoke](https://github.com/cinemascience/workbench/actions/workflows/CinemaSmokeTest.yml/badge.svg)
![base](https://github.com/cinemascience/workbench/actions/workflows/CinemaBaseTest.yml/badge.svg)
![rendering](https://github.com/cinemascience/workbench/actions/workflows/CinemaRenderTest.yml/badge.svg)

Cinema v2.0 is a newly designed toolkit of python-based components for creating, filtering, transforming and viewing Cinema databases. The toolkit shall maintain compatibility with Cinema data specifications.

The code in this repository is released under open source license. See the license file for more information.

All code and examples are prototype and for design purposes only

# Contributing to the workbench

Contributions can be made by submitting issues and contributing code through pull requests. The code shall be reviewed by the core Cinema team, and accepted when both content and code standards are met.

# Running the example

First, create a local python environment for this project, within the repository directory:
```
python3 -m venv csci
source csci/bin/activate
python setup.py install
```

Then, you can work within this environment and run the 'hello world' example:

```
mkdir run
cp -rf cinemasci run
./bin/create-database --database run/cinema.cdb
cp examples/hello.ipynb run
cd run
jupyter notebook hello.ipynb

```

