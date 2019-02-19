## cmip5_to_ant - quick batch processing of CMIP5 files with CDO to Antarctic grids

This package helps to process cmip5 files and makes them usable for PISM.

* select a depth or height level or range from 3D ocean or atmosphere fields
* average over a certain depth or height range.
* create yearly averages
* merge files for a certaion [model,scenario,runid] into one file along time. This is useful for 3D fields mainly.
* merge two scenarios (for example historical and rcp85)

### Usage

* edit [settings.py](settings.py) to your needs.

* run ```python create_cdo_regrid_and_merge.py``` to test for one scenario and model (the first in your list)
    if your setting produce useful output

* check the written ```.sh``` file in ```cdo_scripts/```

* run ```python create_set_of_scripts.py``` to write processing scripts for a whole list of models and scenarios.

* submit to cluster using ```submit_cdo_sripts.sh```.

* you can merge scenarios after the steps above are finished. Test with `python create_cdo_mergescen.py` and create a set of scripts to submit with `only_merge_scenarios = True` and ```python create_set_of_scripts.py```.

### TODO

* create a list of prepocess steps like

```
steps = [select_level, averave_over_dept,
average_over_year, merge_to_one_file]
```

* unify cluster submit option. if not set, write script that can run interactively.

* merging several scenarios is not really expensive, maybe get rid of the submitting to cluster part.

### Model specifics

EC-EARTH: Missing value (for land) is zero, and not recognized properly. It enters into means.
This needs special treatment.
MRI-CGCM3: Same as EC-EARTH

### License

This code is licensed under GPLv3, see the LICENSE.txt. See the commit history for authors.

