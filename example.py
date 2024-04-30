import numpy as np
import TOLP as tolp
from multiprocessing import Pool
path = r"community_label_TSBM//"

data_name = "fake110"


def completely_unobserved_data(name):
    edges_orig = [] 
    data_length = 8
    
    
    for i in range(1,data_length):
        edges_orig.append(np.loadtxt(path+name+"/"+ name+"_{}.txt".format(i)))

    lstm = np.load(path+name+"/"+ name+".npy")
    target_layer = edges_orig[6]
    edges_orig = edges_orig[0:6]
    predict_num = 3
    auprc, auc, precision, recall, featim, feats = tolp.topol_stacking_temporal_with_edgelist(edges_orig, target_layer, predict_num,name)
    
    print("This is the Revision 1 AUC score")
    print(auc)

#completely_unobserved_data(data_name)



def partially_observed_data(name):
    data_length = 8 # this is the "u"+1 in the paper, number of layers + 1 for getting the range correctly later
    
    edges_orig = [] 
    for i in range(1,data_length):
        # load the layers - each layer in a different text file es edge lists
        edges_orig.append(np.loadtxt(path+name+"/"+ name+"_{}.txt".format(i)))

    lstm = np.load(path+name+"/"+ name+".npy") # load "community_label_TSBM//fake110/fake110.npy". why is this loadad?
    target_layer = edges_orig[6] # set the one to be predicted (7th layer)
    edges_orig = edges_orig[0:6] # check how much backward should we look (6 layers + the observed)
    predict_num = 3 # this is the "q" in the paper 
    auprc, auc, precision, recall, featim, feats = tolp.topol_stacking_temporal_partial(edges_orig, target_layer, predict_num,name)
    
    print("This is the Revision 1 AUC score")
    print(auc)
    return auc

# replace `data_name` with your desired dataset, e.g. fake111. 
partially_observed_data(data_name)
