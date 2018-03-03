import bidirectional_rnn as birnn
import recurrent_network as myrnn
import multilayer_perceptron_one_hidden_layer as mlp
import multilayer_perceptron_two_hidden_layer as mlp2
import os
import time
import numpy as np
from config import *
import sys
import config

  
# main run driver
def experiment(params):
    totalTest_loss=0.0
    config.learning_rate = params['learning_rate'][0]
    config.training_epochs = params['training_epochs'][0]
    config.batch_size = params['batch_size'][0]
    config.dropout_rate = params['dropout_rate'][0]
    config.L2_value = params['L2_value'][0]
    config.rnn_hidden = params['hiddenNumber'][0]
    # iterate all projects
    for s in range(0,(len(subs))):
        sub=subs[s]
        ver=vers[s]
        vs = range(ver)
        # iterate all versions of the current proj
        for v in vs:
            v=str(v+1)
            sys.stdout.write(sub + '-'+ v + "-CurrentResult:")
            for i in range(len(techs)):
                train_path=os.path.join(dir,techs[i],sub,v,train_file)
                train_label_path=os.path.join(dir,techs[i],sub,v,train_label_file)
                test_path=os.path.join(dir,techs[i],sub,v,test_file)
                test_label_path=os.path.join(dir,techs[i],sub,v,test_label_file)
                group_path=os.path.join(dir,techs[i],group_dir,sub,v,group_file)
                susp_dir=os.path.join(out_dir,sub,v,techs[i])
                if not os.path.exists(susp_dir):
                    os.makedirs(susp_dir)
                l = 1 #softmax
                    
                start_time=time.time()

                susp_path=os.path.join(susp_dir, model+'-'+losses[l])
                test_loss = myrnn.run(train_path,train_label_path, test_path,test_label_path, group_path, susp_path, featureDistributions[i], l)
                totalTest_loss = totalTest_loss + test_loss
                end_time=time.time()
                
                print("--- %s %s %s time: %s seconds ---" % (model, techs[i], losses[l], (end_time - start_time)))
    return totalTest_loss/100 
#main function execution
def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #:', str(job_id)
    print params
    return experiment(params)