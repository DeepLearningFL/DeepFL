import bidirectional_rnn as birnn
import recurrent_network as myrnn
import multilayer_perceptron_one_hidden_layer as mlp
import multilayer_perceptron_two_hidden_layer as mlp2
import os
import time
import numpy as np
from config import *

  
# main run driver
def main():
    print(sub + '-' + v)
    train_path = os.path.join(dir,tech,sub,v,train_file)
    train_label_path = os.path.join(dir,tech,sub,v,train_label_file)
    test_path = os.path.join(dir,tech,sub,v,test_file)
    test_label_path = os.path.join(dir,tech,sub,v,test_label_file)
    group_path = os.path.join(dir,tech,group_dir,sub,v,group_file)
    susp_dir = os.path.join(out_dir,sub,v,tech)
    if not os.path.exists(susp_dir):
        os.makedirs(susp_dir)

    l = losses.index(loss)   #get index of loss function
    start_time = time.time()
    susp_path = os.path.join(susp_dir, model + '-' + losses[l])

    if model == "rnn":
        myrnn.run(train_path,train_label_path, test_path,test_label_path, group_path, susp_path, featureDistribution, l)
    elif model == "birnn":
        birnn.run(train_path,train_label_path, test_path,test_label_path, group_path, susp_path, featureDistribution, l)
    elif model == "mlp":
        mlp.run(train_path,train_label_path, test_path,test_label_path, group_path ,susp_path, l, featureNum=feature,nodeNum=feature)
    elif model == "mlp2":
        mlp2.run(train_path, train_label_path, test_path, test_label_path, group_path, susp_path, l, featureNum=feature,nodeNum=feature)
    
    end_time = time.time()
        
    print("--- %s %s %s time: %s seconds ---" % (model, tech, losses[l], (end_time - start_time)))
#main function execution
if __name__=='__main__':
    main()
