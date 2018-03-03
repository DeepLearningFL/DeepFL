import os
import time
import numpy as np
from config import *

#dir='/home/lixia/XiaLi/ICSE18/DeepLearningData'
#out_dir='/home/lingming/deep-debugging/results'
#subs=['Time','Chart','Lang','Math','Closure']
#subs=['Closure']
#vers=[27, 26, 65, 106, 133]
#vers=[133]
#techs=['SpectrumJhawkByteMutor12Class', 'SpectrumJhawkByteMutor12NoClass', 'SpectrumTestJhawkByteMutor12Class', 'SpectrumTestJhawkByteMutor12NoClass']
#dnns=['rnn','birnn']
#dnns=['mlp']
#features=[210]
#train_file='Train.csv'
#train_label_file='TrainLabel.csv'
#test_file='Test.csv'
#test_label_file='TestLabel.csv'
#susp_file='rank'
#test_name_file='list.txt'

# parse rank info                                                                                        
def parse(rank_file,test_label_file):
    with open(rank_file) as r:
        rank_list=[line.rstrip('\n') for line in r]
    with open(test_label_file) as l:
        label_list=[line.rstrip('\n').split(',')[0] for line in l]
    rank_list=np.asarray(rank_list,np.float32)
    label_list=np.asarray(label_list,np.int)
    # compute the worst rank of each element as array cost
    u,v=np.unique(-rank_list,return_inverse=True)
    cost=(np.cumsum(np.bincount(v)))[v]
    ranks=[]
    for i in range(len(label_list)):
        if label_list[i]==1:
            ranks.append(cost[i])
    ranks=np.asarray(ranks,np.float32)
    if len(ranks)==0:
        return -1,-1
    min=ranks.min()
    avg=ranks.mean()
    return min,avg

# main                                                                                                                 
def main():
    # iterate all projects                                                                               
    for s in range(len(subs)):
        sub=subs[s]
        ver=vers[s]
        for i in range(len(techs)):
#            if techs[i] == 'rnn':
#                continue
            for d in range(len(dnns)):
                steps=range(dump_step,(training_epochs+1),dump_step)
                #steps=range(20,501,20)
                for epoch in steps:
                    #ls=range(0,3,2)
                    for l in range(1,len(losses)):
                        tops=np.zeros(4)
                        ranks=np.zeros(2)
                        actual_ver=0
                        # iterate all versions of the current proj                                               
                        for v in range(ver):
                            v=str(v+1)
                            #if sub == 'Math' and v=='39':
                            #    continue
                            #if sub == 'Closure' and v=='83':
                            #    continue
                            #print(sub+'-'+v)
                            test_label_path=os.path.join(dir,techs[i],sub,v,test_label_file)
                            susp_path=os.path.join(out_dir,sub,v,techs[i],dnns[d]+'-'+losses[l]+'-'+str(epoch))
                            min,avg=parse(susp_path,test_label_path)
                            if min == -1:
                                continue
                            if min <= 1:
                                tops[0]+=1
                            if min <=3:
                                tops[1]+=1
                            if min<=5:
                                tops[2]+=1
                            if min<=10:
                                tops[3]+=1
                            ranks[0]+=min
                            ranks[1]+=avg
                            actual_ver+=1
                            #print('>',sub,v,min)
                        ranks=ranks/actual_ver
                        print(sub,techs[i], dnns[d], losses[l], epoch, tops,ranks)
main()


# test
def testParse():
    susp_file='/home/lingming/faultlocalization-xia/deep-debugging/results/Time/1/SpectTIRMetricM/rnn-rank.txt'
    label_file='/media/StorageData1/MutationFaultLocalization/LearningRankData/NfolderData/Deep/All25Features/SpectTIRMetricM/Time/1/TestLabel.csv'
    min,avg=parse(susp_file,label_file)
    print(min,avg)

#testParse()
