## TODO

* create a list of prepocess stops like

```
steps = [select_level, averave_over_dept,
average_over_year, merge_to_one_file]
```

* unify cluster submit option. if not set, write script that can run interactively.



## Model specifics

EC-EARTH: Missing value (for land) is zero, and not recognized properly. It enters into means.
This needs special treatment.
MRI-CGCM3: Same as EC-EARTH

