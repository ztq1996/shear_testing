import sys
import os
import math
import logging
import galsim
import numpy as np
import matplotlib.pyplot as plt


def main(argv):


	#galaxy parameters
	gal_flux = 1.e2    # counts
	gal_sigma = 2.0		 
	e1 = 0.3           
	e2 = 0.4   
	e_truth = np.sqrt(e1**2+e2**2)

	#psf parameters
	truth_sigma1 = 0.7
	truth_sigma2 = 1.2
	truth_f = 0.2
	truth_second_moment = (1-truth_f)*truth_sigma1**2+truth_f*truth_sigma2**2

	model_f = np.arange(0.1,0.3,0.001)

	model_sigma2 = 1.2 

	model_sigma1 = np.sqrt((truth_second_moment-model_f*model_sigma2**2)/(1-model_f))

	#image parameters
	pixel_scale = 0.1  # arcsec / pixel
	sky_level = 2.5e3  # counts / arcsec^2

	plt.plot(model_f,model_sigma1)
	plt.xlabel("f")
	plt.ylabel("sigma 1 (arcsec)")
	plt.show()

	gal = galsim.Gaussian(flux=gal_flux, sigma=gal_sigma)
	gal = gal.shear(e1=e1, e2=e2)

	psf = (1-truth_f)*galsim.Gaussian(flux = 1.0, sigma = truth_sigma1) + truth_f*galsim.Gaussian(flux = 1.0, sigma = truth_sigma2)

	final = galsim.Convolve([gal,psf])
	image = final.drawImage(scale = pixel_scale,method = 'no_pixel')
	error_model = []

	for i in range(len(model_f)):
		epsf = (1-model_f[i])*galsim.Gaussian(flux = 1.0, sigma = model_sigma1[i])+model_f[i]*galsim.Gaussian(flux = 1.0 , sigma = model_sigma2)

		image_epsf = epsf.drawImage(scale=pixel_scale,method = 'no_pixel')

		results = galsim.hsm.EstimateShear(image, image_epsf)

		e_measure = np.sqrt(results.corrected_e1**2 + results.corrected_e2**2)

		error_model.append(e_measure-e_truth)

	plt.plot(model_f,error_model)
	plt.xlabel("f")
	plt.ylabel("delta_e")
	plt.title("shear estimation bias given correct second moment")
	plt.grid()
	plt.show()



if __name__ == "__main__":
    main(sys.argv)