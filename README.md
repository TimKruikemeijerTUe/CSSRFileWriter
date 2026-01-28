# CSSRFileWriter
Writes the OVITO frame to a CSD CSSR file as well as possible.

## Description
Write to a CSSR file format. Due to the nature of this format not all options are used.

## Parameters 
Has an optional `title` parameter 

## Example
```python
from CSSRFileWriter import CSSRFileWriter
from ovito.io import export_file, import_file

pipeline = import_file("data.xyz")
export_file(pipeline, "data.cssr", format=CSSRFileWriter, frame=0, title="Title")
```