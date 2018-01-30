""" create a set of scripts that can be run individually or
    be submitted to the compute cluster. """

import os
import settings
import create_cdo_script

script_names = []

for model in settings.models:
    for scenario in settings.scenarios:

        try:
            script_name = create_cdo_script.write_cdo_script(settings, model, scenario)
            script_names.append(script_name)
        except IOError:
            continue

fname = os.path.join("cdo_scripts","submit_cdo_sripts.sh")

with open(fname, 'w') as f:
    f.write("#!/bin/bash\n")
    for nm in script_names:
        f.write("sbatch "+nm.split("/")[-1]+"\n")

print fname, "written."
