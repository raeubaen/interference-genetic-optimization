import ROOT
import numpy as np
import asimov_bkg

def asimov_delta_chi2(cat, gamma, sig_hist, sig_plus_int_hist, bkg_hist, blind=True):

  ROOT.gROOT.cd()
  data_or_asimov_hist = bkg_hist.Clone()

  if blind:
    data_or_asimov_hist.Add(sig_plus_int_hist)

  if not blind:
    asimov_bkg_hist = asimov_bkg.asimov_bkg(bkg_hist)
  else:
    asimov_bkg_hist = bkg_hist.Clone()

  curr_mix_hist = asimov_bkg_hist.Clone()
  curr_mix_hist.Add(sig_hist, 1-np.sqrt(gamma))
  curr_mix_hist.Add(sig_plus_int_hist, np.sqrt(gamma))

  chi2 = 0
  for i in range(1, curr_mix_hist.GetNbinsX()):
    if data_or_asimov_hist.GetBinContent(i) != 0 and abs(data_or_asimov_hist.GetBinCenter(i) - 125) < 10:
      chi2 += (curr_mix_hist.GetBinContent(i) - data_or_asimov_hist.GetBinContent(i))**2 / data_or_asimov_hist.GetBinContent(i)

  if gamma==1 or gamma == 25:
    c = ROOT.TCanvas("c")
    bkg_hist.SetTitle(f"Gamma/GammaSM: {gamma}, cat:{cat}")
    bkg_hist.SetName("bkg")
    bkg_hist.Draw()
    #asimov_bkg_hist.Draw()
    curr_mix_hist.SetName(f"sig_plus_bkg_{int(gamma)}")
    curr_mix_hist.Draw("same")
    curr_mix_hist.SetLineColor(ROOT.kRed)
    c.SaveAs(f"{cat}_{gamma}.root")
    c.SaveAs(f"{cat}_{gamma}.pdf")
    d = ROOT.TCanvas("d")
    res = curr_mix_hist.Clone()
    res.SetName("res")
    res.SetTitle(f"Gamma/GammaSM: {gamma}, cat:{cat}")
    res.Add(bkg_hist, -1)

    low = 125 - 2.5
    high = 125 + 2.5
    sig_int = res.Integral(res.FindBin(low), res.FindBin(high))
    bkg_int = bkg_hist.Integral(bkg_hist.FindBin(low), bkg_hist.FindBin(high))
    bkg_hist_scaled = bkg_hist.Clone()
    curr_mix_hist_scaled = curr_mix_hist.Clone()
    weight  = sig_int/(sig_int+bkg_int)
    curr_mix_hist_scaled.Scale(weight)
    bkg_hist_scaled.Scale(weight)
    curr_mix_hist_scaled.SaveAs(f"histo_sig_plus_bkg_{int(gamma)}_{cat}.root")
    bkg_hist_scaled.SaveAs(f"histo_bkg_{int(gamma)}_{cat}.root")
    print(f"S/(S+B): {weight}, gamma: {gamma}")
    print(f"S: {sig_int}, gamma: {gamma}")
    print(f"w*S: {weight*sig_int}, gamma: {gamma}")

    for i in range(1, res.GetNbinsX()): res.SetBinError(i, 0)
    band = curr_mix_hist.Clone()
    band.SetName("band")
    for i in range(1, band.GetNbinsX()): band.SetBinError(i, bkg_hist.GetBinError(i))
    for i in range(1, band.GetNbinsX()): band.SetBinContent(i, 0)
    band.SetLineColor(ROOT.kBlue)
    res.Draw()
    band.Draw("same")
    d.SaveAs(f"res_{cat}_{gamma}.root")
    d.SaveAs(f"res_{cat}_{gamma}.pdf")

  return chi2
