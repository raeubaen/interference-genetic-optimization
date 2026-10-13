import scan_chi2
import numpy as np
import utils
import copy
import sys

#pt0 = 15 GeV
#pt1 = pt0 + a0 * (max - pt0)
#pt2 = pt1 + a1 * (max - pt1)
#pt3 = pt2 + a2 * (max - pt2)
#pt4 = pt3 + a3 * (max - pt3)
#pt5 = 3000

#mva0 = -1 + 2*b0
#mva1 = mva0 + (1 - mva0)*b1

#a0,a1,a2,a3 + 5*(b0, b1) = 14 parametri

def get_boundaries_from_parameters(pt_pars, mva_pars):

  pt0 = 15
  pt1 = pt0 + pt_pars[0] * (150 - pt0)
  pt2 = pt1 + pt_pars[1] * (150 - pt1)
  pt3 = pt2 + pt_pars[2] * (150 - pt2)
  pt4 = pt3 + pt_pars[3] * (150 - pt3)
  pt5 = 3000

  mva_boundaries = []
  for i in range(5):
    mva0 = -0.5 + 1.5*mva_pars[i][0]
    mva1 = mva0 + (1 - mva0)*mva_pars[i][1]
    mva_boundaries.append([mva0, mva1])

  return {"pt": [pt0, pt1, pt2, pt3, pt4, pt5], "mva": mva_boundaries}

def chi2_gamma0(pt_pars, mva_pars, data_th3, sig_th3, sig_plus_int_th3):

  boundaries = get_boundaries_from_parameters(pt_pars, mva_pars)
  cats = utils.initialize_cats(5, boundaries["mva"], boundaries["pt"])

  chi2 = np.asarray(scan_chi2.scan_chi2_all_cats([0], data_th3, sig_th3, sig_plus_int_th3, cats))

  print("chi2: ", sum(chi2))

  return sum(chi2)
