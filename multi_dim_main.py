import scan_chi2
import numpy as np
import scan_analysis
import utils
import ROOT
import argparse
import generic_optim
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population
import sys
import pickle

class InterferenceSignificanceProblem(ElementwiseProblem):

  def __init__(self):
    data_th3_file = ROOT.TFile("data_th3_recat.root")
    sig_plus_int_th3_file = ROOT.TFile("sig_plus_int_th3_recat.root")
    sig_th3_file = ROOT.TFile("sig_th3_recat.root")

    ROOT.gROOT.cd()
    self.data_th3 = data_th3_file.Get("h_0").Clone()
    self.data_th3.SetName("data")

    self.sig_th3 = sig_th3_file.Get("h_0").Clone()
    self.sig_th3.SetName("sig")

    self.sig_plus_int_th3 = sig_plus_int_th3_file.Get("h_0").Clone()
    self.sig_plus_int_th3.SetName("sig_plus_int")

    super().__init__(n_var=14,
                     n_obj=1,
                     n_ieq_constr=0,
                     xl=np.array([0]*14),
                     xu=np.array([1]*14))

  def _evaluate(self, x, out, *args, **kwargs):
    pt_pars = x[:4]
    mva_pars_flat = x[4:]
    mva_pars = []
    for i in range(5): mva_pars.append([mva_pars_flat[2*i], mva_pars_flat[2*i+1]])
    out["F"] = [ - generic_optim.chi2_gamma0(pt_pars, mva_pars, self.data_th3, self.sig_th3, self.sig_plus_int_th3)]


if __name__ == "__main__":
  problem = InterferenceSignificanceProblem()

  initial_pars = [0.045, 0.07, 0.142, 0.3, 0.9568666666666666, 0.7928902627511596, 0.9213999999999999, 0.8286683630195081, 0.9564, 0.76605504587156, 0.9342666666666667, 0.8600405679513181, 0.9688, 0.8824786324786335]

  X = np.asarray([initial_pars]*300).reshape(300, 14)

  algorithm = NSGA2(pop_size=300, sampling=X)

  res = minimize(problem,
               algorithm,
               seed=1,
               save_history=True,
               verbose=True)



  # open a file, where you ant to store the data
  file = open('res.pkl', 'wb')

  # dump information to that file
  pickle.dump(res.X, file)

  print(res.X)

  print(res.F)
