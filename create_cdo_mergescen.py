
import os
import glob
import jinja2
import numpy as np
import netCDF4 as nc
import settings


def write_cdo_script(settings, model):


    # runids_to_merge = []
    source_paths_to_merge = []
    for scenario in settings.scenarios_to_merge:

        runid = "_".join([settings.variable,settings.time_res,
            model,scenario,settings.cmip5_runid])

        source_paths_to_merge.append(
            os.path.join(settings.target_path, runid, "concat",
            runid+"_"+settings.grid_id+".nc"))

    merged_scens = "+".join(settings.scenarios_to_merge)
    merged_runid = "_".join([settings.variable,settings.time_res,
            model,merged_scens,settings.cmip5_runid])
    target_path = os.path.join(settings.target_path, merged_runid)

    # make jinja aware of templates
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(settings.project_root,"templates")))

    template = jinja_env.get_template("mergescen_template.jinja2")

    out = template.render(source_paths_to_merge=" ".join(source_paths_to_merge),
                          merged_file=merged_runid+"_"+settings.grid_id+".nc",
                          target_path=target_path)

    fname = os.path.join("cdo_scripts","cdo_"+merged_runid+".sh")
    with open(fname, 'w') as f: f.write(out)

    print fname, "written."

    return fname

if __name__ == "__main__":

    # for testing or single model use. always pick first of list.
    model = settings.models[0]

    write_cdo_script(settings, model)
