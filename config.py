'''
Configuration and parameters can be set in this file
'''


from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy
import input
import time
import sys
                                                                                                                                                                     
dir=sys.argv[1]      # The directory of dataset
out_dir=sys.argv[2]  # The directory of results
model = sys.argv[3]  # model name, such as "mlp" "mlp2" "rnn" "birnn"                          
subs=['Time','Chart','Lang','Math','Mockito','Closure']
vers=[27, 26, 65, 106, 38, 133]

dnns = [model]
techs=['SpectrumTestJhawkByte']                                                                                                                 
featureDistributions=[[34,35,35,35,35,37]]
features=[211]

learning_rate = 0.001
training_epochs = 300
batch_size = 500
display_step = 10
dump_step = 2
dropout_rate = 0.9
L2_value = 0.0001
rnn_hidden=max(featureDistributions[0])
losses=['wsoftmax', 'softmax', 'epairwise','epairwiseSoftmax', 'hpairwise','hpairwiseSoftmax']
                                                 
train_file='Train.csv'
train_label_file='TrainLabel.csv'
test_file='Test.csv'
test_label_file='TestLabel.csv'
group_dir='groupfile'
group_file='traidata.txt.group'
susp_file='rank'


