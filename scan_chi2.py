import ROOT
import asimov_bkg
import asimov_delta_chi2
import numpy as np
import utils
import sys

def scan_chi2_one_cat(gammas, data_th3, sig_th3, sig_plus_int_th3, cat, blind=True, lumi=137):

  pt_bins_edges = [data_th3.GetYaxis().GetXbins()[i] for i in range(data_th3.GetNbinsY()+1)]
  mva_bins_edges = [data_th3.GetZaxis().GetXbins()[i] for i in range(data_th3.GetNbinsZ()+1)]

  yz_projection_bins = [
    utils.edge_to_bin(cat["pt"][0], pt_bins_edges), utils.edge_to_bin(cat["pt"][1], pt_bins_edges),
    utils.edge_to_bin(cat["mva"][0], mva_bins_edges), utils.edge_to_bin(cat["mva"][1], mva_bins_edges)
  ]

  data_mass_hist = data_th3.ProjectionX(f"data_mass", *yz_projection_bins)
  sig_mass_hist = sig_th3.ProjectionX(f"sig_mass", *yz_projection_bins)
  sig_plus_int_mass_hist = sig_plus_int_th3.ProjectionX(f"sig_plus_int_mass", *yz_projection_bins)


  data_mass_hist.Scale(lumi/64.)

  sig_mass_hist.Scale(lumi)
  sig_plus_int_mass_hist.Scale(lumi)

  print(cat, data_mass_hist.Integral(data_mass_hist.FindBin(120), data_mass_hist.FindBin(130)), sig_mass_hist.Integral(data_mass_hist.FindBin(120), data_mass_hist.FindBin(130)), sig_plus_int_mass_hist.Integral(data_mass_hist.FindBin(120), data_mass_hist.FindBin(130)))

  bkg_mass_hist = asimov_bkg.asimov_bkg(data_mass_hist, blind=blind)

  chi2_scan = []
  for gamma in gammas:
    curr_chi2 = asimov_delta_chi2.asimov_delta_chi2(cat, gamma, sig_mass_hist, sig_plus_int_mass_hist, bkg_mass_hist, blind=blind)
    chi2_scan.append(curr_chi2)

  return chi2_scan

def scan_chi2_all_cats(
  gammas,
  data_th3, sig_th3, sig_plus_int_th3,
  cats,blind=True,lumi=137
):

  chi2_scan = [[]]*len(cats)
  for i, cat in enumerate(cats):
    print(cat)
    chi2_scan[i] = scan_chi2_one_cat(gammas, data_th3, sig_th3, sig_plus_int_th3, cat, blind=blind, lumi=lumi)

  return np.asarray(chi2_scan).reshape(len(cats), len(gammas))
