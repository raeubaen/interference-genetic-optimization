import ROOT

def asimov_bkg(bkg_hist, blind=True):

  ROOT.gROOT.cd()

  unblinded_hist = bkg_hist.Clone()

  if not blind:
    for i in range(1, unblinded_hist.GetNbinsX()+1):
      unblinded_hist.SetBinError(i, ROOT.TMath.Sqrt(unblinded_hist.GetBinContent(i)))
    return unblinded_hist

  for i in range(30, 70):
    unblinded_hist.SetBinError(i, unblinded_hist.GetMaximum())
  f = ROOT.TF1("f", "expo", 115, 135)
  unblinded_hist.Fit(f, "QON")
  ROOT.gROOT.cd()
  blinded_hist = ROOT.TH1F("blind_"+unblinded_hist.GetName(), unblinded_hist.GetTitle(), 160, 100, 180)
  for i in range(1, blinded_hist.GetNbinsX()+1):
    blinded_hist.SetBinContent(i, f.Eval(blinded_hist.GetBinCenter(i)))
    blinded_hist.SetBinError(i, ROOT.TMath.Sqrt(blinded_hist.GetBinContent(i)))
  return blinded_hist
