# --- include -----

# --- include -----
import numpy as np
import pandas as pd
import TOLP as tolp
import os
import sys
#from multiprocessing import Pool

# --- functions --------
def run_partially_observed_temporal_lp(mln_file_path, predict_num, search_var, layer_to_predict, is_unipartite=True):
    """
    this function gets the values for running tempotal link prediction using Xie's tool and runs it

    assumptions: 
    layer ids are from 1 to n_layers (included), and all exist in the same file, under the format <layer>, <from>, <to>. 
    the predicted layer must be one of those layers.

    vaiable:
    mln_file_path - path of the CSV file containing a mln in an edge list format, with ids for nodes and layers. first row is column names.
    predict_num - the number of layers in one stack of layers used to calculate features. q in the paper.
    search_var - the number of temporal layers to look back from the predicted layer. u in the paper.
    """
    mln_data = np.loadtxt(mln_file_path, delimiter=",", skiprows=1) # assumes the first row are column headers

    # get number of layers:
    n_layers = int(mln_data.max(axis=0)[0])

    # make sure the values received make sense:
    assert layer_to_predict <= n_layers, "layer ID cannot be higher then the number of layers avaiable in the data."
    assert search_var+1 <= layer_to_predict, "Search variable (u) + 1 cannot be higher then the ID of the ."
    assert predict_num < search_var, "Flow variable (q) must be smaller then the Search variable (u)."

    edges_orig = [] 
    for i in range(1,n_layers+1): # +1 for the range
        print(i)
        # filter from arrays rows that are relevant to that layer:
        layer = mln_data[mln_data[:,0]==i]
        edges_orig.append(layer[:,1:3])
        

        # load the layers - each layer in a different text file es edge lists
        #edges_orig.append(np.loadtxt(path+name+"/"+ name+"_{}.txt".format(i)))

    pred_ind = layer_to_predict-1

    target_layer = edges_orig[pred_ind] # set the one to be predicted (7th layer)
    edges_orig = edges_orig[pred_ind-search_var:pred_ind] # check how much backward should we look (6 layers + the observed)

    name = os.path.splitext(os.path.basename(mln_file_path))[0]# file name
    # run the lp algorithm
    auprc, auc, mcc, precision, recall, featim, feats = tolp.topol_stacking_temporal_partial(edges_orig, target_layer, predict_num, name)
    print("feat_imp: ", featim)

    # read feature file and predictions and merge column into a single dataframe
    memb = np.loadtxt("results/" + name + "/probabilities.txt", delimiter=",", dtype=float)
    pred = np.loadtxt("results/" + name + "/prediction.txt", delimiter=",", dtype=int)
    feat = np.loadtxt("results/" + name + "/predicted_edges.txt", delimiter=",", dtype=int) # per edge get nodes ids and true clasification
    
    # convert numpy arrays to pandas dataframes
    memb = pd.DataFrame(memb, columns=['memb_0', 'memb_1'])
    pred = pd.DataFrame(pred, columns=['prediction'])
    feat = pd.DataFrame(feat, columns=['node1', 'node2', 'true_class'])
    
    # merge pandas columns into a single dataframe
    edges_probs = pd.concat([feat, memb, pred], axis=1)

    # save the combination dataframe to a file
    edges_probs.to_csv("results/" + name + "/edges_membership.csv", index=False)

    return auprc, auc, mcc, precision, recall, featim, feats

# --- argument handling ------
# expected arguments:
# 1. filename - must
# 2. flow variable (q - n layers in a stack) - has default
# 3. search varianle (u - n layers used to predicte) - has default
# 4. predicted later index - has default

# set defaults
file_path = "for_HPC/input/WinfreeYYc_mln.csv"
q = 3
u = 6
target = 7

# read user input params
n_args = len(sys.argv)
print(n_args)
match n_args:
    case 1:
        raise Exception("Must have at leaset one argument - with file path to the mln file")
    case 2:
        print("Using default parameters: q=3, u=6, target_layer=7")
    case 5:
        print("Script arguments are:", sys.argv[1:])
        q = sys.argv[2]
        u = sys.argv[3]
        target = sys.argv[4]
    case _:
        raise Exception("invalide argument number, please see README.md for tool usage.")
        

file_path = sys.argv[1]
assert os.path.isfile(file_path), "First argument must point to a mln file."


# --- Run -------
if __name__ == "__main__":
    print("Running as main.")
    run_partially_observed_temporal_lp(file_path, q, u, target, is_unipartite > 0)
    print("Single lp run finished. ")


