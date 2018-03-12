
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy
import input
import time
from config import *
import utils as ut 
import recurrent_network as myrnn



def BiRNN(x, weights, biases, n_hidden, n_steps, keep_prob):

    # Unstack to get a list of 'n_steps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, n_steps, 1)

    # Define lstm cells with tensorflow
    # Forward direction cell
    lstm_fw_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    lstm_fw_cell = tf.contrib.rnn.DropoutWrapper(lstm_fw_cell, output_keep_prob=keep_prob)    
    # Backward direction cell
    lstm_bw_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    lstm_bw_cell = tf.contrib.rnn.DropoutWrapper(lstm_bw_cell, output_keep_prob=keep_prob)    

    # Get lstm cell output
    try:
        outputs, _, _ = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x,
                                              dtype=tf.float32)
    except Exception: # Old TensorFlow version only returns outputs not states
        outputs = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x,
                                        dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

def run(trainFile, trainLabelFile, testFile, testLabelFile, groupFile, suspFile, featureDistribution, loss):
    # reset graph                                                                                                                                            
    tf.reset_default_graph()    
    # Network Parameters                                                                                                                                     
    n_input = numpy.array(featureDistribution).max()
    n_steps = len(featureDistribution)
    n_hidden = numpy.array(featureDistribution).max()
    n_classes = 2 # number of output classes                                                                                                                 

    # tf Graph input                                                                                                                                         
    x = tf.placeholder("float", [None, n_steps, n_input])
    y = tf.placeholder("float", [None, n_classes])
    g = tf.placeholder(tf.int32, [None, 1])

    # dropout                                                                                                                                                 
    keep_prob = tf.placeholder(tf.float32)

    # Define weights                                                                                                                                          
    weights = {
        # Hidden layer weights => 2*n_hidden because of forward + backward cells
        'out': tf.Variable(tf.random_normal([2*n_hidden, n_classes]))
    }
    biases = {
        'out': tf.Variable(tf.random_normal([n_classes]))
    }

    pred = BiRNN(x, weights, biases, n_hidden, n_steps, keep_prob)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32)) 

    # load datasets
    datasets = input.read_data_sets(trainFile,trainLabelFile, testFile,testLabelFile, groupFile)
    
    # load test data
    test_data=myrnn.fillMatrix(datasets.test.instances,featureDistribution)
    test_data = test_data.reshape((-1, n_steps, n_input))
    test_label = datasets.test.labels

    # Define loss and optimizer                                                                                                                                                                             
    variables  = tf.trainable_variables()
    regularizer = tf.add_n([ tf.nn.l2_loss(v) for v in variables if 'bias' not in v.name]) * L2_value  # l2 regularization   
    cost = ut.loss_func(pred, y, loss, datasets, g)
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost+regularizer)

    init = tf.global_variables_initializer()

    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)
        step = 1
        # Keep training until reach max iterations
        #while step * batch_size < training_epochs*:
        total_batch = int(datasets.train.num_instances/batch_size)
        for epoch in range(training_epochs):
            avg_cost = 0.
            # Loop over all batches
            for i in range(total_batch):
                batch_x, batch_y, batch_g = datasets.train.next_batch(batch_size)
                # Reshape data to get 28 seq of 28 elements
                batch_x = myrnn.fillMatrix(batch_x,featureDistribution)
                batch_x = batch_x.reshape((batch_size, n_steps, n_input))
                # Run optimization op (backprop)
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y, g: batch_g, keep_prob:dropout_rate})
                # Compute average loss
                avg_cost += c / total_batch
            if epoch % display_step == 0 and i==(total_batch-1):
                    print("Epoch " + str(epoch+1) + ", Minibatch Loss= " + "{:.6f}".format(avg_cost))
            if epoch % (dump_step) == (dump_step-1):
                res=sess.run(tf.nn.softmax(pred),feed_dict={x: test_data, y: test_label, keep_prob:1.0})
                with open(suspFile+'-'+str(epoch+1),'w') as f:
                    for susp in res[:,0]:
                        f.write(str(susp)+'\n')
        print("Optimization Finished!")

