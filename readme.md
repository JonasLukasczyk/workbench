# Cinema v2.0 prototyping and design repository
![smoke](https://github.com/cinemascience/workbench/actions/workflows/CinemaSmokeTest.yml/badge.svg)
![base](https://github.com/cinemascience/workbench/actions/workflows/CinemaBaseTest.yml/badge.svg)

Cinema v2.0 is a newly designed toolkit of python-based components for creating, filtering, transforming and viewing Cinema databases. The toolkit shall maintain compatibility with Cinema data specifications.

The code in this repository is released under open source license. See the license file for more information.

All code and examples are prototype and for design purposes only

# Contributing to the workbench

Contributions can be made by submitting issues and contributing code through pull requests. The code shall be reviewed by the core Cinema team, and accepted when both content and code standards are met.

# Running the example 

```
# IMPORTANT: CinemaLib repo must be in python path or in project directory
import cinemasci

# Open Cinema Database
cdb  = cinemasci.DatabaseReader();
cdb.inputs["Path"].setValue( 'cinema.cdb' );

# Select Some Data Products
query = cinemasci.DatabaseQuery();
query.inputs["Table"].setValue(cdb.outputs['Table']);
query.inputs["Query"].setValue('SELECT * FROM input LIMIT 5 OFFSET 0');

# Read Data Products
imageReader = cinemasci.ImageReader();
imageReader.inputs["Table"].setValue(query.outputs['Table']);

# Render Images in Black and White (to demo shader effects)
imageRenderer = cinemasci.ImageRenderer();
imageRenderer.inputs["Image"].setValue( imageReader.outputs["Images"] );

# Display Results
from IPython.display import display
images = imageRenderer.outputs["Image"].getValue();
for i in images:
    display(i)
```

