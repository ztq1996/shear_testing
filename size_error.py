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
	e1 = 0.0       
	e2 = 0.2   
	e_truth = np.sqrt(e1**2+e2**2)
	psf_sigma = 0.6  

	pixel_scale = 0.1  # arcsec / pixel

	psf_model_range = np.arange(0.58,0.62,0.001)
	e_error_gaussian = []



	gal = galsim.Gaussian(flux=gal_flux, sigma=gal_sigma)
	gal = gal.shear(e1=e1, e2=e2)

	psf = galsim.Gaussian(flux = 1.0, sigma = psf_sigma)
	final = galsim.Convolve([gal, psf])

# method = 'no_pixel'
	image = final.drawImage(scale=pixel_scale,method = 'no_pixel')

	# if not os.path.isdir('output'):
	#     os.mkdir('output')
	# file_name = os.path.join('output', 'gal+psf.fits')
	# image.write(file_name)
	for i in range(len(psf_model_range)):
		psf_model = galsim.Gaussian(flux = 1.0, sigma = psf_model_range[i])

		image_epsf = psf_model.drawImage(scale=pixel_scale,method = 'no_pixel')

		results = galsim.hsm.EstimateShear(image, image_epsf)
		print  results.moments_sigma
		e_measure = np.sqrt(results.corrected_e1**2 + results.corrected_e2**2)
		
		distance = np.sqrt((results.corrected_e1-e1)**2+(results.corrected_e2-e2)**2)

		e_error_gaussian.append(e_measure - e_truth)
	#gal_sigma = results.moments_sigma/10
	e_observed = np.sqrt(results.observed_shape.e1**2+results.observed_shape.e2**2)
	r_observed = results.moments_sigma/10
	#prediction = e_truth*(psf_model_range**2-psf_sigma**2)/(results.moments_sigma/10)**2
	prediction1 = e_observed*r_observed**2*(psf_model_range**2-psf_sigma**2)/(r_observed**2 - psf_model_range**2)**2

	#prediction2 = e_observed*(psf_model_range**2-psf_sigma**2)/r_observed**2

	prediction3 = e_truth*(psf_model_range**2-psf_sigma**2)/gal_sigma**2




	plt.plot(psf_model_range,e_error_gaussian,label="truth")
	plt.plot(psf_model_range,prediction1,label="prediction by myself")
	#plt.plot(psf_model_range,prediction2,label="prediction by approximate mine")
	plt.plot(psf_model_range,prediction3,label="prediction by paper")
	plt.ylabel("e_measure - e_truth")
	plt.xlabel("psf model size (truth = 0.6)")
	plt.title("gal_sigma = 2.0, psf = 0.6")
	plt.legend()
	plt.grid()
	plt.show()


if __name__ == "__main__":
    main(sys.argv)