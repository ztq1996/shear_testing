import sys
import os
import math
import logging
import galsim
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import Angle


def main(argv):

	gal_flux = 1.e5    # counts
	gal_sigma = 2.0		 
	e1 = np.arange(0.0,0.9,0.01) 
	e1 = [0]

	

	#psf_sigma_list = [0.1,0.2,0.3,0.4,0.5,0.6]
	psf_sigma_list = np.arange(0.1,0.6,0.01)
	gal_sig_measure_list=[]

	for psf_sigma in psf_sigma_list:
		gal_sig_measure = np.empty_like(e1)
		pixel_scale = 0.1  # arcsec / pixel
		sky_level = 2.5e3  # counts / arcsec^2
		psf_model = galsim.Gaussian(flux = 1.0, sigma = psf_sigma)
		image_epsf = psf_model.drawImage(scale = pixel_scale,method = 'no_pixel')
		for e_num, e in enumerate(e1):
			gal = galsim.Gaussian(flux=gal_flux, sigma=gal_sigma)
			gal = gal.shear(e1=e1[e_num])

			final = galsim.Convolve([gal, psf_model])

			image = final.drawImage(scale=pixel_scale,method = 'no_pixel')

			results = galsim.hsm.EstimateShear(image,image_epsf)

			gal_sig_measure[e_num]=results.moments_sigma/10
			print results.moments_sigma
			gal_sig_measure_list.append(results.moments_sigma/10)

		#gal_sig_measure_list.append(gal_sig_measure)


	print gal_sig_measure_list



	# for ind,psf in enumerate(psf_sigma_list):
	# 	plt.plot(e1,gal_sig_measure_list[ind]-gal_sigma,label="PSF="+str(psf))
	# plt.ylabel("sigma measurement bias (arcsec) ")
	# plt.xlabel("e")
	# plt.title("galaxy sigma = 2 arcsec, use same true and model for psf")
	# plt.legend()
	# plt.grid()
	# plt.show()

	plt.plot(psf_sigma_list,np.array(gal_sig_measure_list)-gal_sigma)
	plt.ylabel("bias in R2(arcsec)")
	plt.xlabel("psf(arcsec)")
	plt.title("galaxy sigma = 2 arcsec, use same true and model for psf")
	plt.legend()
	plt.grid()
	plt.show()


if __name__ == "__main__":
    main(sys.argv)