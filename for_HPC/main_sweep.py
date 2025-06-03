# Description: This script is used to run a sweep of the parameters q and u for the temporal link prediction algorithm.
# assumption: the last layer is the target layer
print("main_sweep.py start.")

# --- include -----
import pandas as pd
import numpy as np
import os
import sys
import shutil
import main as mn

# --- functions --------
def run_q_u_sweep(filepath, n_layers, is_unipartite, is_in_hpc):
    name = os.path.splitext(os.path.basename(filepath))[0]# file name
    folder = os.path.dirname(filepath)
    target = n_layers # we always target the last layer
    max_u = n_layers - 1
    min_q = 2
    max_q = max_u-1
    
    result_df = pd.DataFrame(columns=["study", "q", "u", "roc", "prc", "mcc", "precision", "recall", "tn", "fp", "fn", "tp"])

    nrows=0
    for q in range(min_q, max_q+1):
        for u in range(q+1, max_u+1):
            print("Running for q: ", q, " and u: ", u)
            # make it so that we have a different network file for each q and u
            new_file_name = folder+"/"+name+"_q"+str(q)+"_u"+str(u)+".csv"
            shutil.copyfile(filepath,new_file_name) 

            if is_in_hpc == 1:
                # give explicit path to qsub command, as it is not recognised when running from another job.
                # allows running sweep_main on a job, to run a bunch of them.
                qsub = "/storage/SGE6U8/bin/lx24-amd64/qsub" # relevant only for BGU HPC
                comd = qsub + " run_single.sh "+new_file_name+" "+str(q)+" "+str(u)+" "+str(target)+" "+str(is_unipartite)
                print("Running os command: ", comd)

                # run a system command to run as a job
                os.system(comd)
            else:
                auprc, auc, mcc, precision, recall, _, _2, cm = mn.run_partially_observed_temporal_lp(new_file_name, q, u, target, is_unipartite > 0)
                tn, fp, fn, tp = cm.ravel()
                result_df.loc[nrows] = [name, q, u, auc, auprc, mcc, precision, recall, int(tn), int(fp), int(fn), int(tp)]
                nrows = nrows+1

                # delete the file - only when not in HPC, because we dont want to delete before its used
                os.remove(new_file_name)
    
    return result_df

# --- main function ------
def main_func():
    # --- argument handling ------
    # expected arguments:
    # 1. filename - must
    # 2. number of layers - has default
    # 3. is unipartite (1) or bipartite (0)- has default

    # set defaults
    file_path = "for_HPC/input/WinfreeYYc_mln.csv"
    n_layers = 7
    is_unipartite = 1
    is_in_hpc = 0

    # read user input params
    n_args = len(sys.argv)
    if n_args == 1:
        raise Exception("Must have at least one argument - with file path to the mln file")
    elif n_args == 2:
        print("Using default parameters: n_layers=7, is_unipartite=1")
    elif n_args == 4:
        print("Script arguments are:", sys.argv[1:])
        n_layers = int(sys.argv[2])
        is_unipartite = int(sys.argv[3])
    elif n_args == 5:
        print("Script arguments are:", sys.argv[1:])
        n_layers = int(sys.argv[2])
        is_unipartite = int(sys.argv[3])
        is_in_hpc = int(sys.argv[4])
    else:
        raise Exception("Invalid argument number, please see README.md for tool usage.")

    file_path = sys.argv[1]
    assert os.path.isfile(file_path), "First argument must point to a mln file."

    # --- Run -------
    # run the sweeps
    res = run_q_u_sweep(file_path, n_layers, is_unipartite, is_in_hpc)

    if is_in_hpc != 1: # if this is not running in HPC, so each job didnt save the results yet
        # save the result to a file
        name = os.path.splitext(os.path.basename(file_path))[0]# file name
        ouptut_file = "results/"+ name +"_sweep.csv"
        res.to_csv(ouptut_file, index=False)

# --- Run -------
if __name__ == "__main__":
    print("main_sweep.py running as main.")
    main_func()
    print("sweep is done.")