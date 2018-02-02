
import os
import glob
import numpy as np
import netCDF4 as nc
import dimarray as da
import itertools
import shutil
import subprocess
import settings

def copy_cmip_file(settings, model, scenario):

    source_path = os.path.join(settings.pcmdipath,scenario,
        settings.time_res,settings.variable,model,
        settings.cmip5_runid)

    runid = "_".join([settings.variable,settings.time_res,
        model,scenario,settings.cmip5_runid])

    filename = runid+"_"+settings.grid_id+".nc"
    target_path = os.path.join(settings.target_path, runid)

    out_path = os.path.join(target_path,"schmidtko_anomaly/")

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    shutil.copyfile(os.path.join(target_path,"concat",filename),
                    os.path.join(out_path,filename))

    return os.path.join(out_path,filename)

def anomalize_to_schmidtko(cmip_file,schmidtko_file):

    """ also add schmidtko salinity """

    print "## now process", cmip_file

    ncf = nc.Dataset(cmip_file,'a')
    ncs = nc.Dataset(schmidtko_file,"a")

    var = ncf.variables["thetao"]

    mask_year0 = var[0,:,:].mask
    unmasked_var_year_0 = np.array(var[0,:,:])
    unmasked_var_year_0[mask_year0] = 0.

    schmidtko_data = ncs.variables["theta_ocean"][:]

    timeindex = np.arange(0,var.shape[0],1)
    chunklen = 50
    chunks = [timeindex[i:i + chunklen] for i in xrange(0, len(timeindex), chunklen)]
    # run through chunks of n timesteps

    for chunk in chunks:

        mask = var[chunk,:,:].mask
        unmasked_var = np.array(var[chunk,:,:])
        unmasked_var[mask] = 0.
        var[chunk,:,:] = unmasked_var - unmasked_var_year_0 + schmidtko_data

    salinity = ncs.variables["salinity_ocean"]
    ncsal = ncf.createVariable("salinity_ocean",var.dtype, dimensions=var.dimensions)
    ncsal[:] = np.tile(salinity[:],(var.shape[0],1,1))

    # todo: move this to function
    for attr in salinity.ncattrs():
        print attr + ': ' + salinity.getncattr(attr)
        setattr(ncsal, attr, salinity.getncattr(attr))

    basins =  ncs.variables["basins"]
    print basins.dimensions
    ncbas = ncf.createVariable("basins",basins.dtype, dimensions=basins.dimensions)
    ncbas[:] = basins[:]

    # todo: move this to function
    for attr in basins.ncattrs():
        print attr + ': ' + basins.getncattr(attr)
        setattr(ncbas, attr, basins.getncattr(attr))

    ncf.close()
    ncs.close()

    print cmip_file, " created."


def fill_with_schmidtko_means(cmip_file,schmidtko_file):

    def fill_with_basin_means(var,basins):

        mvar = var.copy()

        for b in range(int(basins.max())+1):

            print b
            mask = np.tile(basins!=b,(var.shape[0],1,1))
            varmean = np.ma.masked_array(var[:,:,:], mask=mask).mean(axis=2).mean(axis=1)
            mvar[~mask] = np.repeat(varmean,(~mask[0,:,:]).sum())

        return mvar

    ncf = nc.Dataset(cmip_file,'a')
    ncs = nc.Dataset(schmidtko_file,"a")

    basins =  ncs.variables["basins"]
    var = ncf.variables["thetao"]

    var[:] = fill_with_basin_means(var[:], basins[:])

    ncf.close()
    ncs.close()


def add_coordinate_variables(cmip_file,schmidtko_file):

    subprocess.check_call("module load nco && ncks -A -v x,y "+
        schmidtko_file+" "+cmip_file, shell=True)


def rename_ocean_variable(cmip_file):

    tempfile = cmip_file.rstrip(".nc")+"_temp.nc"
    subprocess.check_call("module load cdo/1.8.0 && cdo chname,thetao,theta_ocean "+
        cmip_file+" "+tempfile, shell=True)

    os.remove(cmip_file)
    os.rename(tempfile, cmip_file)

    print "renamed variable thetao to theta_ocean."


if __name__ == "__main__":

    # for testing or single model use. always pick first of list.
    model = settings.models[0]
    scenario = settings.scenarios[0]

    out_file = copy_cmip_file(settings, model, scenario)
    anomalize_to_schmidtko(out_file, settings.schmidtko_file)
    fill_with_schmidtko_means(out_file, settings.schmidtko_file)
    add_coordinate_variables(out_file,settings.schmidtko_file)
    rename_ocean_variable(out_file)