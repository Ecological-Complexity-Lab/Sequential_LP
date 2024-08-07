# Description: This script is used to run a sweep of the parameters q and u for the temporal link prediction algorithm.
# assumption: the last layer is the target layer

# --- include -----
import pandas as pd
import os
import sys
import for_HPC.main as mn

# --- functions --------
def run_q_u_sweep(filepath, n_layers, is_unipartite):
    name = os.path.splitext(os.path.basename(filepath))[0]# file name
    target = n_layers # we always target the last layer
    max_u = n_layers - 1
    min_q = 2
    max_q = max_u-1
    
    result_df = pd.DataFrame(columns=["study", "q", "u", "roc", "prc", "mcc", "precision", "recall"])
    nrows=0
    for q in range(min_q, max_q+1):
        for u in range(q+1, max_u+1):
            print("Running for q: ", q, " and u: ", u)
            auprc, auc, mcc, precision, recall, _, _2 = mn.run_partially_observed_temporal_lp(filepath, q, u, target, is_unipartite > 0)
            result_df.loc[nrows] = [name, q, u, auc, auprc, mcc, precision, recall]
            nrows = nrows+1
    
    return result_df

# --- argument handling ------
# expected arguments:
# 1. filename - must
# 2. number of layers - has default
# 3. is unipartite (1) or bipartite (2)- has default

# set defaults
file_path = "for_HPC/input/WinfreeYYc_mln.csv"
n_layers = 7
is_unipartite = 1

# read user input params
n_args = len(sys.argv)
print(n_args)
match n_args:
    case 1:
        raise Exception("Must have at leaset one argument - with file path to the mln file")
    case 2:
        print("Using default parameters: n_layers=7, is_unipartite=1")
    case 5:
        print("Script arguments are:", sys.argv[1:])
        n_layers = sys.argv[2]
        is_unipartite = sys.argv[3]
    case _:
        raise Exception("invalide argument number, please see README.md for tool usage.")
        
file_path = sys.argv[1]
assert os.path.isfile(file_path), "First argument must point to a mln file."

# --- Run -------
if __name__ == "__main__":
    print("Running as main.")

    # run the sweeps
    res = run_q_u_sweep(file_path, n_layers, is_unipartite)

    # save the result to a file
    name = os.path.splitext(os.path.basename(file_path))[0]# file name
    ouptut_file = "results/"+ name +"_sweep.csv"
    res.to_csv(ouptut_file, index=False)
