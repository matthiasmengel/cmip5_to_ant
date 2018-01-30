
import os
import glob
import jinja2
import numpy as np
import netCDF4 as nc
import settings


def find_nearest(array,range_to_average):

  idx0=(np.abs(array-range_to_average[0])).argmin()
  idx1=(np.abs(array-range_to_average[1])).argmin()
  return ",".join([str(z) for z in array[idx0:idx1+1]])


def write_cdo_script(settings, model, scenario):

    source_path = os.path.join(settings.pcmdipath,scenario,
        settings.time_res,settings.variable,model,
        settings.cmip5_runid)

    runid = "_".join([settings.variable,settings.time_res,
        model,scenario,settings.cmip5_runid])

    target_path = os.path.join(settings.target_path, runid)

    cmip_files = sorted(glob.glob(os.path.join(source_path,"*")))
    cmip_files = [os.path.basename(f) for f in cmip_files]
    cmipfilesstring=" ".join(cmip_files)

    if len(cmip_files) == 0:
        text = "No files in "+source_path+" , or path not existent."
        print(text)
        raise IOError(text)

    # get z axis, assume they are consistent through files.
    ncf = nc.Dataset(os.path.join(source_path,cmip_files[0]), 'r')
    nc_zlevels = ncf.variables['lev'][:]
    ncf.close()

    zlevelstring = find_nearest(nc_zlevels, settings.depth_range_to_average)

    # make jinja aware of templates
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(settings.project_root,"templates")))

    template = jinja_env.get_template("regrid_template.jinja2")
    out = template.render(source_path=source_path,
                          target_path=target_path,
                          target_grid=settings.target_grid,
                          zlevelstring=zlevelstring,
                          cmip_files=cmip_files,
                          cmipfilesstring=cmipfilesstring,
                          runid=runid,
                          cluster_regridding=settings.cluster_regridding)

    fname = os.path.join("cdo_scripts","cdo_"+runid+".sh")
    with open(fname, 'w') as f: f.write(out)

    print fname, "written."

    return fname

if __name__ == "__main__":

    # for testing or single model use. always pick first of list.
    model = settings.models[0]
    scenario = settings.scenarios[0]

    write_cdo_script(settings, model, scenario)
