# Sequential Link Prediction on HPC

# What?

This is a wrapper for easy usage of the tool that is published in [Sequential stacking link prediction algorithms for temporal networks](https://www.nature.com/articles/s41467-024-45598-0) by Xie He, and is available in [this github repository](https://github.com/hexie1995/Sequential-Link-Prediction).
The algorithm used here is the basic topological sequentual stacking, used for temporal network link prediction.
This wrapper for the tool only allows for prediction of partially observed layers, 
even though the original tool allows for unobserved pradictions as well.

# How?

## Running the tool
It is available for usage in the lab's HPC under:
project/software/Sequential_LP/

Usage includes:
1. uploading the data file in the correct format to the HPC.
2. running the `main.py` sctipt on the data file.
3. collecting the data when it is done, to your computer for further analysis.
4. clean the output folders (as this is a common usage tool).

## Input
running the tool script should be as follews:
use `cd` to navigate to the folder of the tool
then enter in the command line either:
`python3 main.py <path/to/mln/data.csv> <q> <u> <target_layer_index>`

or, if you wish to use the tool's defaults:
`python3 main.py <path/to/mln/data.csv>`

but these are specific to the example data, 
so it is not recommended to use them unless they are identical 
to the structure of the network you are analysing as well.

so to run the example:
`python3 main.py example/WinfreeYYc_mln.csv` 
or
`python3 main.py example/WinfreeYYc_mln.csv 3 6 7` 

Note: when runing the script you should pass to it either exactly one argument or 
4 in total, and not in between those number of arguments.

## Input mln data file format
The file should be a csv file structured of 3 columns, with the first row as column names:

`layer | node_from | node_to`

The tool is meant to be used only with indexes and not with node labels or layer labels.
The indexes should be given beforehand and the ids with corresponding lables should be saved elsewhere.

*Importent*: layer IDs should be in the range of 1 .. n_layers. 

For an example of assigning ids in R, see `prepare_for_temporal_lp.R` available under  `example` folder, 
that prepares the example data for usage in the tool.

## Output 

The resulting stats of the overall run are written under `results/<input_file_name>/RF_Best_metrics.txt`.

Lists of edges used in the training and holdout, for positive and negitive samples are in:
`edge_tf_tr` and `edge_tf_true` folders

Lists of features calculated for stacked layers are located under: 
`ef_gen_ho`, `ef_gen_tr`, and `feature_metrices/<input_file_name>`

List of predicted links (by node index):
`edge_membership.csv`
It details an edge's true classification, membership probabilities and clasification by the module.


# Source
Example data paper: https://nsojournals.onlinelibrary.wiley.com/doi/full/10.1111/oik.07303
The DB itself: https://datadryad.org/stash/dataset/doi:10.5061/dryad.qz612jmbp