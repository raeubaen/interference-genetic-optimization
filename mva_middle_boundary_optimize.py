import scan_chi2
import numpy as np
import scan_analysis
import utils
import copy

def mva_middle_boundary_optimize(default_cats, data_th3, sig_th3, sig_plus_int_th3, opt_for_kI=False):
  if opt_for_kI:
    max_gamma = 3**2
    orig_gammas = np.linspace(0, max_gamma, 31)
    gammas = orig_gammas**2
  else:
    max_gamma = 60
    orig_gammas = np.linspace(0, max_gamma, 201)
    gammas = orig_gammas

  cats = copy.deepcopy(default_cats)
  opt_mva_bounds = []

  if len(cats) %2 != 0: raise ValueError("Cats not divisible by 2 as expected")
  for i in range(int(len(cats)/2)):
    default_mva_1_bound = cats[2*i]["mva"][1]
    mva_1_bounds = np.linspace((1 + default_mva_1_bound)/2 - (1 - default_mva_1_bound)/3, (1 + default_mva_1_bound)/2 + (1 - default_mva_1_bound)/3, 10)
    opt_mva_bound = mva_1_bounds[0]
    best_gamma = max_gamma

    cat_low_mva  = cats[2*i]
    cat_high_mva = cats[2*i+1]

    print("default cat_low_mva: ", cat_low_mva)
    print("default cat_high_mva: ", cat_high_mva)

    chi2_scan_low_mva = np.asarray(scan_chi2.scan_chi2_one_cat(gammas, data_th3, sig_th3, sig_plus_int_th3, cat_low_mva))
    chi2_scan_high_mva = np.asarray(scan_chi2.scan_chi2_one_cat(gammas, data_th3, sig_th3, sig_plus_int_th3, cat_high_mva))
    chi2_scan = chi2_scan_low_mva+chi2_scan_high_mva
    default_chi2_at_0 = chi2_scan[0]

    for j in range(len(chi2_scan)):
      if chi2_scan[j] < 1: optim_j = j
    default_best_gamma = gammas[optim_j]

    best_chi2_at_0 = 0

    for bound in mva_1_bounds:
      cat_low_mva["mva"][1]  = bound
      cat_high_mva["mva"][0] = bound

      chi2_scan_low_mva = np.asarray(scan_chi2.scan_chi2_one_cat(gammas, data_th3, sig_th3, sig_plus_int_th3, cat_low_mva))
      chi2_scan_high_mva = np.asarray(scan_chi2.scan_chi2_one_cat(gammas, data_th3, sig_th3, sig_plus_int_th3, cat_high_mva))
      chi2_scan = chi2_scan_low_mva+chi2_scan_high_mva
      if opt_for_kI:
        if chi2_scan[0] > best_chi2_at_0:
          best_chi2_at_0 = chi2_scan[0]
          opt_mva_bound = bound
      else:
        for j in range(len(chi2_scan)):
          if chi2_scan[j] < 1: optim_j = j
        if gammas[optim_j] < best_gamma:
          best_gamma = gammas[optim_j]
          opt_mva_bound = bound

    cats[2*i]["mva"][1]  = opt_mva_bound
    cats[2*i+1]["mva"][0] = opt_mva_bound
    opt_mva_bounds.append([cats[2*i]["mva"][0], opt_mva_bound])

    if opt_for_kI:
      print("pt cat: ", i, ", default mva 1 value: ", default_mva_1_bound, ", optimized value: ", opt_mva_bound, ", default chi2 at 0: ", default_chi2_at_0, ", optimized chi2 at 0: ", best_chi2_at_0)
    else:
      print("pt cat: ", i, ", default mva 1 value: ", default_mva_1_bound, ", optimized value: ", opt_mva_bound, ", default gamma limit: ", default_best_gamma, ", optimized gamma limit: ", best_gamma)

  print("Opt. Mva boundaries: ", opt_mva_bounds)
  scan = scan_chi2.scan_chi2_all_cats(gammas, data_th3, sig_th3, sig_plus_int_th3, cats)
  outfile = "scan_opt_mva_1_bound_cats.npy"
  np.save(outfile, scan)
  scan_analysis.scan_analysis(scan, orig_gammas, sum_over_axis0=True)
