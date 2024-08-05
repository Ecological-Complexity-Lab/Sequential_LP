# Description: This script is used to run a sweep of the parameters q and u for the temporal link prediction algorithm.
# assumption: the last layer is the target layer

# --- include -----
import pandas as pd
import os
import for_HPC.main_sweep as sweep

# --- Run -------
if __name__ == "__main__":
    print("Running as main.")
    is_unipartite = 1

    # networks:
    # for_HPC/input/CaraDonna2017_aggregated.csv -  9 layers
    # for_HPC/input/WinfreeYYc_mln.csv           -  7 layers 
    # for_HPC/input/Lara_Romero2016_penalara.csv - 12 layers

    # run the sweeps
    resC = sweep.run_q_u_sweep("for_HPC/input/CaraDonna2017_aggregated.csv", 9, is_unipartite)
    resW = sweep.run_q_u_sweep("for_HPC/input/WinfreeYYc_mln.csv", 7, is_unipartite)
    resL = sweep.run_q_u_sweep("for_HPC/input/Lara_Romero2016_penalara.csv", 12, is_unipartite)

    # concat the 3 dataframes into a single dataframe
    all = pd.concat([resW, resL, resC])

    # save the result to a file
    ouptut_file = "results/grant_sweep.csv"
    all.to_csv(ouptut_file, index=False)
