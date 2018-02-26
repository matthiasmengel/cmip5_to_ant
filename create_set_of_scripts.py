""" create a set of scripts that can be run individually or
    be submitted to the compute cluster. """

import os
import settings

import create_cdo_regrid_and_merge
import create_cdo_mergescen
# import create_cdo_script

if settings.only_merge_scenarios:
    print "only merge scenario files that have been preprosessed before."
    print "for full preprocessing, set merge_scenarios_only to False."
    create = create_cdo_mergescen
else:
    create = create_cdo_regrid_and_merge

script_names = []

if settings.only_merge_scenarios:

    for model in settings.models:

        try:
            script_name = create.write_cdo_script(settings, model)
            script_names.append(script_name)
        except IOError:
            continue

else:

    for model in settings.models:
        for scenario in settings.scenarios:

            try:
                script_name = create.write_cdo_script(settings, model, scenario)
                script_names.append(script_name)
            except IOError:
                continue

fname = os.path.join("cdo_scripts","submit_cdo_sripts.sh")

with open(fname, 'w') as f:
    f.write("#!/bin/bash\n")
    for nm in script_names:
        f.write("sbatch "+nm.split("/")[-1]+"\n")

print fname, "written."
