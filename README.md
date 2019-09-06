Testing shear bias induced by non-gaussian moments of PSF
===

Goals:
---
1. Understand how the error of measuring higher (non-gaussian) moments of PSF is going to cause bias/uncertainty to the shear measurement.
2. Testing the goodness of higher moments being measured by previous surveys: Is the affection on the shear comparable with the second moment bias? with the statistical error? 
3. 


Archieved tests:
---

1. `sizeerror_test.ipynb`:
- Implement shear measurement functionality with `Galsim`
- Verify the prediction of shape bias induced by the error of measuring second moment, which is suggested in 0711.4886. In this notebook, only the size error is tested.
- The prediction works pretty well when the galaxy and PSF are both gaussian. 
-When galaxy and psf are non-gaussian, there appears to be an intersection (which means deconvolve(convolve([gal,psf]),psf) has the different shape with gal) in the bias prediction. This is bizard so we subtract that part by `get_intersection()`
- After subtracting the intersection, the slope of the bias vs size error is different from what is predicted for non-gaussian galaxy and psf. The slope is varying from 





Created by Tianqing Zhang
Advisor: Rachel Mandelbaum
