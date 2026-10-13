import scan_chi2
import numpy as np
import scan_analysis
import utils
import ROOT
import argparse
import mva_middle_boundary_optimize

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--default_cats", help="scan for default categories",
                      action="store_true")
  parser.add_argument("--new_cats", help="scan for new categories",
                      action="store_true")
  parser.add_argument("--mva_middle_boundary_optimize", help="Optimize the MVA boundary in the middle",
                      action="store_true")
  parser.add_argument("--kI_optimize", help="Optimize for kI (high chi2 at 0)",
                      action="store_true")

  args = parser.parse_args()

  data_th3_file = ROOT.TFile("data_th3_recat.root")
  sig_plus_int_th3_file = ROOT.TFile("sig_plus_int_th3_recat.root")
  sig_th3_file = ROOT.TFile("sig_th3_recat.root")

  data_th3 = data_th3_file.Get("h_0")
  data_th3.SetName("data")

  sig_th3 = sig_th3_file.Get("h_0")
  sig_th3.SetName("sig")

  sig_plus_int_th3 = sig_plus_int_th3_file.Get("h_0")
  sig_plus_int_th3.SetName("sig_plus_int")

  print("histograms read")

  if args.default_cats or args.mva_middle_boundary_optimize:
    n_pt_cat = 5
    mva_boundaries = [[0.9353,0.9866], [0.8821,0.9798], [0.9346,0.9847], [0.9014,0.9862], [0.9532,0.9945]] #2018 from flashgg

    pt_boundaries = [15, 21, 31, 47, 77, 3000]
    gammas = np.linspace(0, 25, 51)
    default_cats = utils.initialize_cats(n_pt_cat, mva_boundaries, pt_boundaries)

  if args.default_cats:
    scan = scan_chi2.scan_chi2_all_cats(gammas, data_th3, sig_th3, sig_plus_int_th3, default_cats, blind=True, lumi=137)
    outfile = "scan_default_cats.npy"
    np.save(outfile, scan)
    scan_analysis.scan_analysis(scan, gammas, sum_over_axis0=True)

  if args.mva_middle_boundary_optimize:
   mva_middle_boundary_optimize.mva_middle_boundary_optimize(default_cats, data_th3, sig_th3, sig_plus_int_th3, opt_for_kI=args.kI_optimize)

  if args.new_cats:
    gammas = np.linspace(0, 20, 201)
    pt_boundaries = [15, 35.5361476348193, 52.90853759582434, 58.525712929715084, 111.83037362470361, 3000]
    mva_boundaries = [[0.6903240641585451, 0.9790326424703222], [0.9235631096640082, 0.9868959690821945], [0.9626331719715515, 0.9926437168465366], [0.9267179916210302, 0.9901084244829116], [0.9762135939688283, 0.9917360157278843]]
    new_cats = utils.initialize_cats(5, mva_boundaries, pt_boundaries)
    scan = scan_chi2.scan_chi2_all_cats(gammas, data_th3, sig_th3, sig_plus_int_th3, new_cats, blind=True, lumi=137)
    scan_analysis.scan_analysis(scan, gammas, sum_over_axis0=True)
