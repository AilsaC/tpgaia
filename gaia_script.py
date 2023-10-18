from tpgaia import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##### Initializing, Optimizing and Sampling the Two Models #####

mod = AstrometricModel("TIC283722336", ecc_prior="kipping") #Trying a high mass and a bright/nearby star, and using the reparameterised eccentricity

mod.star_from_tic()

mod.init_planet('b', mpl_mjup=9, empl_mjup=0.25, per_d=550, eper_d=150,  t0_jd=2460200, et0_jd=0.04, b=0.4, eb=0.25)
mod.init_planet('c',mpl_mjup=14,empl_mjup=0.5,per_d=220,eper_d=60,t0_jd=2460000,et0_jd=0.04,b=0.6,eb=0.25,
                ecc=0.25,little_omega_rad=0.2516*np.pi,big_Omega_rad=1.6193*np.pi)

mod.init_gaia_data()

mod.optimize_model(w_planets=True)
mod.optimize_model(w_planets=False)

#Due to the difficulty of sampling this parameter space, I have boosted this for the with-planet case:
mod.sample_model(w_planets=True,regularization_steps=12,n_draws=3000,save_model=True)#, savenames=savenames, save_model=False) #n_draws was 15000 changed to 3000
mod.sample_model(w_planets=False,regularization_steps=6,n_draws=1500,save_model=False)#8000 changed to 1500

#################################################################

##### Making Parameters Tables #####

#mod.w_planets_param_table
mod.make_summary() #Making summary DataFrame (and csvs) for each of the two models (trace_output.csv)
#################################################################

##### Plotting Outputs #####

#mod.plot_planet_histograms(nbins=150)
#mod.plot_corners()

#################################################################

##### Comparing Models using WAIC #####
##Problems start here###
mod.compare_models()
mod.plot_residual_timeseries()
#################################################################

print(mod.planets) # Contains planet info

print(mod.starname,"\n astropy RADEC = ",mod.radec,"\n Gaia Mag = ",mod.GAIAmag,"\n Rs=",mod.rad_rsun,"\n Parallax=",mod.plx_mas) # star info

##### Saving ######

#mod.savenames
mod.save_model_nopickle()

'''This is hard-coded to be in a folder called "data" which is in the directory of the tpgaia.py file 
(a new folder is generated for each star name). Typically things are saved with one of two prefixes. 
One is model-dependent and includes a number (i.e. changes each time the model gets re-run) which is 
good as it means we won't overwrite old stuff. The other is model-independent and should include files 
which are model-independent (e.g. the Gaia GOST data)''' 

#################################################################