# Sequential Link Prediction on HPC

# What?

This is a wrapper for easy usage of the tool that is published in [Sequential stacking link prediction algorithms for temporal networks](https://www.nature.com/articles/s41467-024-45598-0) by Xie He, and is available in [this github repository](https://github.com/hexie1995/Sequential-Link-Prediction).
The algorithm used here is the basic topological sequentual stacking, used for temporal network link prediction.
This wrapper for the tool only allows for prediction of partially observed layers, 
even though the original tool allows for unobserved pradictions as well. \
this wrapper also allows usage with bipartite networks, unlike the original tool that was only suitable for unipartite ones.

# How?

## Running the tool
It is available for usage in the lab's HPC under:
project/software/Sequential_LP/

Usage includes:
1. uploading the data file saved in the correct format to the HPC.
2. running the `main.py` sctipt on the data file.
3. collecting the data when it is done, to your computer for further analysis.
4. clean the output folders (as this is a community usage tool).

## Input
running the tool (via HPC) should be as follews: \ 
Go to the terminal and log into the HPC then into the relevant node (bhn1089, using ssh). \
use `cd` to navigate to the folder of the tool \
`cd ../../project/software/Sequential_LP`

then, assuming you already have your input file on the server,\
enter in the command line either: \
`python3 main.py <path/to/mln/file.csv> <q> <u> <target_layer_index> <is_unipartite>` \

when: \
`<path/to/mln/file.csv>` - path to the input file, containing the multilayer network in edgelist format. \
`<q>` - flow variable from the original tool: number of layers in a stack.\
`<u>` - search varianle from the original tool: number of layers overall used to predict the target.\
`<target_layer_index>` - the index of the target layer (1 indexed).\
`<is_unipartite>` - indication whether the network given in the input file is unipartite (1) or bipartite(0).

or, if you wish to use the tool's defaults: \
`python3 main.py <path/to/mln/file.csv>`

Note that the tool's defaults are specific to the example data, 
so it is not recommended to use them unless they are identical 
to the structure of the network you are analysing as well.

so to run the example:\
`python3 main.py input/WinfreeYYc_mln.csv` \
or \
`python3 main.py input/WinfreeYYc_mln.csv 3 6 7 0` 

Note: \
when runing the script you should pass to it either exactly one argument or 
5 in total, and not in between those number of arguments.

## Input mln data file format
The file should be a csv file structured of 3 columns, with the first row as column names:

`layer | node_from | node_to`

The tool is meant to be used only with indexes and not with node labels or layer labels.
The indexes should be given beforehand and the ids with corresponding lables should be saved elsewhere.

*Importent*: \
layer IDs should be in the range of 1 .. n_layers. \
Also - nodes should labeled from 0 .. N-1 (with integer as their index)

For an example of assigning ids in R, see `prepare_for_temporal_lp.R` available under `example` folder, 
that prepares the example data for usage in the tool.

## Output 

The resulting stats of the overall run are written under `results/<input_file_name>/RF_Best_metrics.txt`.

Lists of edges used in the training and holdout, for positive and negitive samples are in: \
`edge_tf_tr` and `edge_tf_true` folders

Lists of features calculated for stacked layers are located under: \
`ef_gen_ho`, `ef_gen_tr`, and `feature_metrices/<input_file_name>`

List of predicted links (by node index): \
`edge_membership.csv` \
It details an edge's true classification, membership probabilities and clasification by the module.


## Secondary usage:
In the same folder exists a wrapper for the tool that runs a sweep across all possible q and u values, 
and saves performance measurements. 

### Input
running process is similar to the one above, only the command will be: \
`python3 main_sweep.py example/WinfreeYYc_mln.csv <number_of_layers> <is_unipartite>` \
or \
`python3 main_sweep.py example/WinfreeYYc_mln.csv 7 0` 

### input file format
the same as the one for a single lp run: `layer | node_from | node_to`

### output
the same as a single run, with the addision of a new file: \
`results/<input_file_name>_sweep.csv` \
in it the performance measurments for each pair of possible q and u.

# Source
Example data paper: https://nsojournals.onlinelibrary.wiley.com/doi/full/10.1111/oik.07303 \
The DB itself: https://datadryad.org/stash/dataset/doi:10.5061/dryad.qz612jmbp