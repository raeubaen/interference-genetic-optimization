import numpy as np
import ROOT

def scan_analysis(chi2, gammas, sum_over_axis0=False):
  if sum_over_axis0: chi2 = chi2.sum(axis=0)

  g = ROOT.TGraph(len(gammas), gammas.astype(np.float64), chi2.astype(np.float64))
  g.Draw("AP L ")
  g.SetMarkerStyle(7)
  l1 = ROOT.TLine(0, 1, 20, 1)
  l1.Draw()
  l2 = ROOT.TLine(0, 4, 20, 4)
  l2.Draw()
  input()
