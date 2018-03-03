
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy
import input
import time
import config
import utils as ut
import sys

def RNN(x, weights, biases, n_hidden, n_steps, keep_prob):

    # Unstack to get a list of 'n_steps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, n_steps, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    lstm_cell = tf.contrib.rnn.DropoutWrapper(lstm_cell, output_keep_prob=keep_prob)
    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
	# Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


# add additional columns to make all info the same length
def fillMatrix(x,featureDistribution):
    maxGroup=numpy.array(featureDistribution).max()
    filled=numpy.zeros(shape=(x.shape[0],maxGroup*len(featureDistribution)))
    index=0
    for i in range(len(featureDistribution)):
        for j in range(i*maxGroup,i*maxGroup+featureDistribution[i]):
            filled[:,j]=x[:,index]
            index+=1
    return filled

# This function only help for bayesian search
def getMisrank(res, testlable):
    size = len(testlable)
    faultyvalues = []
    correctvalues = []
    for index in range(size):
        sys.stdout.write(str(res[index][0])+" ")
        if testlable[index][0] == 1:
            faultyvalues.append(res[index][0])
        elif testlable[index][0] == 0:
            correctvalues.append(res[index][0])
    print("")
    misrank=1.0   # less, better
    if len(faultyvalues) > 0:    # this version has buggy method
        if size == len(faultyvalues):    # all methods in test data are buggy
            misrank = 0.0
        elif size > len(faultyvalues):
            maxfaulty = max(faultyvalues)
            correct = 0.0
            for index in range(len(correctvalues)):
                if correctvalues[index] < maxfaulty:
                    correct = correct+1.0
            misrank = 1 - correct/(size - len(faultyvalues))
    return misrank

# call this function to run 
def run(trainFile, trainLabelFile, testFile, testLabelFile, groupFile, suspFile,featureDistribution, loss):

    learning_rate = config.learning_rate
    training_epochs = config.training_epochs
    batch_size = config.batch_size
    display_step = config.display_step
    dump_step = config.dump_step
    dropout_rate = config.dropout_rate
    L2_value = config.L2_value

    # reset graph
    tf.reset_default_graph() 
    # Network Parameters
    n_input = numpy.array(featureDistribution).max()
    n_steps = len(featureDistribution)
    #n_hidden = numpy.array(featureDistribution).max()
    n_hidden = config.rnn_hidden              
    n_classes = 2 # number of output classes

    # tf Graph input
    x = tf.placeholder("float", [None, n_steps, n_input])
    y = tf.placeholder("float", [None, n_classes])
    g = tf.placeholder(tf.int32, [None, 1])

    # dropout                                                                                                                                               
    keep_prob = tf.placeholder(tf.float32)

    # Define weights
    weights = {
        'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
    }
    biases = {
        'out': tf.Variable(tf.random_normal([n_classes]))
    }

    pred = RNN(x, weights, biases, n_hidden, n_steps, keep_prob)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # load test data
    datasets=input.read_data_sets(trainFile, trainLabelFile, testFile, testLabelFile, groupFile)
	test_data=fillMatrix(datasets.test.instances,featureDistribution)
    test_data = test_data.reshape((-1, n_steps, n_input))
    test_label = datasets.test.labels
        
    # Define loss and optimizer
	variables  = tf.trainable_variables() 
    regularizer = tf.add_n([ tf.nn.l2_loss(v) for v in variables if 'bias' not in v.name]) * L2_value      # l2 regularization
	cost = ut.loss_func(pred, y, loss, datasets, g)
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost+regularizer)
    # Initializing the variables
    init = tf.global_variables_initializer()
	
	# Launch the graph
    with tf.Session() as sess:
        sess.run(init)
        step = 1
        total_batch = int(datasets.train.num_instances/batch_size)
        res=[]
        for epoch in range(training_epochs):
            # Loop over all batches
            for i in range(total_batch):
                batch_x, batch_y, batch_g = datasets.train.next_batch(batch_size)
                # Reshape data 
                batch_x = fillMatrix(batch_x,featureDistribution)
                batch_x = batch_x.reshape((batch_size, n_steps, n_input))
                # Run optimization 
                sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, g: batch_g, keep_prob:dropout_rate})
                if epoch % display_step == 0 and i==(total_batch-1):
                    # Calculate batch accuracy
                    acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y, g: batch_g, keep_prob:1.0})
                    # Calculate batch loss
                    loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y, g: batch_g, keep_prob:1.0})
            # write result        
            res=sess.run(tf.nn.softmax(pred),feed_dict={x: test_data, y: test_label, keep_prob:1.0})
            with open(suspFile+'-'+str(epoch+1),'w') as f:
                for susp in res[:,0]:
                    f.write(str(susp)+'\n')
        misrank = getMisrank(res,test_label)
        print("Optimization Finished!")
        return misrank
