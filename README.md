# steinertthrelkeldmodals

Inside a virutal env:

* `pip install -e .`
* `pip install -r requirements.txt`
* `cldfbench catconfig` and say `y` to `glottolog`
* `cldfbench makecldf cldfbench_steinertthrelkeldmodals.py`

## Notes

* I had an issue using `pycldf.term_uri` for the column names in `add_table` (which I was doing following the README of `pycldf`).  What's the right way of making sure the column names are "correct" / linked up to the proper RDF terms?

## TODO
* Glottolog for lang metadata
* How to best to get descriptions for each force and flavor? (This is a data-gathering question for SST; they're not in the raw data at present)