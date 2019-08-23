import sys
import os
import math
import logging
import galsim
import numpy as np
import matplotlib.pyplot as plt


def main(argv):

	gal_flux = 1.e2    # counts
	gal_sigma = 2.0		 
	e1 = 0.3           
	e2 = 0.4   
	e_truth = np.sqrt(e1**2+e2**2)
	psf_sigma = 0.6  

	pixel_scale = 0.1  # arcsec / pixel
	sky_level = 2.5e3  # counts / arcsec^2





	gal = galsim.Gaussian(flux=gal_flux, sigma=gal_sigma)
	gal = gal.shear(e1=e1, e2=e2)


	###################image with gaussian psf###########################
	psf_gau = galsim.Gaussian(flux = 1.0, sigma = psf_sigma)
	final_gau = galsim.Convolve([gal, psf_gau])

	image_gau = final_gau.drawImage(scale=pixel_scale)

	###################image with moffat psf###########################
	psf_beta = 5       #
	psf_re = 1.0       # arcsec

	psf_mof = galsim.Moffat(beta=psf_beta, flux=1., half_light_radius=psf_re)

	final_mof = galsim.Convolve([gal, psf_mof])

	image_mof = final_mof.drawImage(scale=pixel_scale)



	psf_model_range = np.arange(0.5,0.7,0.01)

	e_error_gg = []
	for i in range(len(psf_model_range)):
		psf_model = galsim.Gaussian(flux = 1.0, sigma = psf_model_range[i])

		image_epsf = psf_model.drawImage(scale=pixel_scale)

		results = galsim.hsm.EstimateShear(image_gau, image_epsf)

		e_measure = np.sqrt(results.corrected_e1**2 + results.corrected_e2**2)

		e_error_gg.append(e_truth-e_measure)

	e_error_mm = []
	for i in range(len(psf_model_range)):
		psf_model = galsim.Moffat(beta = psf_beta, flux = 1.0, half_light_radius = psf_model_range[i])

		image_epsf = psf_model.drawImage(scale=pixel_scale)

		results = galsim.hsm.EstimateShear(image_mof, image_epsf)

		e_measure = np.sqrt(results.corrected_e1**2 + results.corrected_e2**2)

		e_error_mm.append(e_truth-e_measure)

	e_error_mg = []
	for i in range(len(psf_model_range)):
		psf_model = galsim.Gaussian(flux = 1.0, sigma = psf_model_range[i])

		image_epsf = psf_model.drawImage(scale=pixel_scale)

		results = galsim.hsm.EstimateShear(image_mof, image_epsf)

		e_measure = np.sqrt(results.corrected_e1**2 + results.corrected_e2**2)

		e_error_mg.append(e_truth-e_measure)

	e_error_gm = []
	for i in range(len(psf_model_range)):
		psf_model = galsim.Moffat(beta = psf_beta, flux = 1.0, half_light_radius = psf_model_range[i])

		image_epsf = psf_model.drawImage(scale=pixel_scale)

		results = galsim.hsm.EstimateShear(image_gau, image_epsf)

		e_measure = np.sqrt(results.corrected_e1**2 + results.corrected_e2**2)

		e_error_gm.append(e_truth-e_measure)

	plt.subplot(221)
	plt.plot(psf_model_range,e_error_gg)

	plt.subplot(222)
	plt.plot(psf_model_range,e_error_gm)

	plt.subplot(223)
	plt.plot(psf_model_range,e_error_mg)

	plt.subplot(224)
	plt.plot(psf_model_range,e_error_mm)



	plt.show()


	







if __name__ == "__main__":
    main(sys.argv)