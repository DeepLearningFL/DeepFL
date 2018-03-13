# DeepFL
DeepFL is a deep-learning-based fault localization technique. It implements two multi-layer perceptron variants and two recurrent neural networks variants by [Tensorflow](https://www.tensorflow.org/). The benchmark subject is from [Defects4j](https://github.com/rjust/defects4j), which is an open source repository, providing  some buggy versions and corresponding fixed versions of different projects. Features of the dataset include different dimensions, e.g., spectrum-based, mutation-based, complexity-based (code metrics) and textual-similarity-based information.  

## Requirements ##
- Python 2/3 with Pandas and Numpy
- Tensorflow

## DataSet ##
The dataset can be downloaded from an online [Cloud Drive](https://mega.nz/#F!ffxXBISD!UQjggpnjw8oWrjSc0D7PdA). There are six .gz files, each of them represents one setting in our paper as follows:

*DeepFL.tar.gz*: Dataset with all of four dimensions features above.

*CrossDeepFL.tar.gz*: Dataset with all of four dimensions features in the cross-project scenario. 

*DeepFL-Spectrum.tar.gz*: Dataset with three dimensions features, i.e.,mutation-based, complexity-based and textual-similarity-based information.

*DeepFL-Mutation.tar.gz*: Dataset with three dimensions features, i.e.,spectrum-based, complexity-based and textual-similarity-based information.

*DeepFL-Metrics.tar.gz*: Dataset with three dimensions features, i.e.,spectrum-based, mutation-based and textual-similarity-based information.

*DeepFL-Textual.tar.gz*: Dataset with three dimensions features, i.e.,spectrum-based, mutation-based and complexity-based information.
## Running DeepFL ##
The command to run DeepFL for each version is as follows:

```
$ cd DeepFL
```

```
$python main.py /absolute/path/to/ParentDirofDataset /absolute/path/to/Result $subject $version $model $tech $loss $epoch $dump_step
```
Each parameter can be explained as follows:
1. /absolute/path/to/ParentDirofDataset: The absolute path of the parent directory including all datasets, for example, if the dataset is DeepFL, its directory can be /home/DeepLearningData/DeepFL ("/home/DeepLearningData/" is created by users, and "DeepFL" is put
into it)
2. /absolute/path/to/Result: The directory of the results. 
3. $subject: The subject name, which can be *Time*, *Chart*, *Lang*, *Math*, *Mockito* or *Closure*.
4. $version: The version number of the subject. Note that, the maximum numbers of subjects above are 27, 26, 65, 106, 38, 133, respectively.
5. $model: The implemented model name, which can be *mlp*, *mlp2*, *rnn*, *birnn*, representing multi-layer perceptron with one hidden layer, multi-layer perceptron with two hidden layers, recurrent neural network and Bidirectional recurrent neural network respectively.
6. $tech: The different dimensions of features, corresponding to the name of dataset, can be *DeepFL*, *DeepFL-Metrics*, *DeepFL-Mutation*, *DeepFL-Spectrum*, *DeepFL-Textual*, *CrossDeepFL*.
7. $loss: The name of loss function, which can be *softmax*, *epairwise*, *epairwiseSoftmax*.
8. $epoch: The number of training epochs.
9. $dupm_step: The interval number of epoch in which the result will be stored into the result file. For example, if $dump_step = 10, the results in epochs 10, 20, 30... will be written into the files.

## Results statistics ##
After running all subject versions, run the following command to calculate the five measurements Top-1, Top-3, Top-5, MFR, MAR:

```
python rank_parser.py /absolute/path/to/ParentDirofDataset /absolute/path/to/Result $tech $model $loss $epoch
```
Please note that due to the randomly initialized parameters, the results may be slightly different from our paper.




