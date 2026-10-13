def edge_to_bin(edge, bin_edges):
  selected = 0
  for i, bin_edge in enumerate(bin_edges):
    if abs(bin_edge-edge) < abs(bin_edges[selected]-edge):
      selected = i
  return selected + 1

def initialize_cats(n_pt_cat, mva_boundaries, pt_boundaries):
  cats = []
  for pt_cat_idx in range(n_pt_cat):
    for mva_cat_idx in range(2):
      if mva_cat_idx == 0:
        d = {"pt": [pt_boundaries[pt_cat_idx], pt_boundaries[pt_cat_idx+1]], "mva": mva_boundaries[pt_cat_idx]}
      else:
        d = {"pt": [pt_boundaries[pt_cat_idx], pt_boundaries[pt_cat_idx+1]], "mva": [mva_boundaries[pt_cat_idx][1], 1]}
      cats.append(d)
  return cats
