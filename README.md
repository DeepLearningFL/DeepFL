# DeepFL
DeepFL is a deep-learning-based fault localization technique. 

The dataset is collected from real faults project [Defects4j](https://github.com/rjust/defects4j), including different dimensions of features, e.g., spectrum-based, mutation-based, complexity-based (code metrics) and textual-similarity-based features. The dataset can be downloaded from a online [Cloud Drive](https://mega.nz/#F!ffxXBISD!UQjggpnjw8oWrjSc0D7PdA). There are six .gz files, each of them represents our setting in our paper. For example, DeepFL.tar.gz is the data with four dimensions features above and CrossDeepFL.tar.gz is just in the cross-project scenario. DeepFL-XXX.tar.gz is the the data excluding one a certain dimension, which has three dimensions features. For example, DeepFL-Metrics.tar.gz excludes complexity-based information. 

DeepFL implements two multi-layer perceptron variants and two recurrent neural networks variants by [Tensorflow](https://www.tensorflow.org/).
## Requirements ##
- Python 2/3 with Pandas and Numpy
- Tensorflow
## Running DeepFL ##
The command to run DeepFL for each version is follows:

```
$ cd DeepFL
```

```
$python main.py /absolute/path/to/ParentDirofDataset /absolute/path/to/Result subject version model tech loss
```
Each parameter can be explained as follows:
1. /absolute/path/to/ParentDirofDataset: The absolute path of the parent directory including all datasets, for example, if the dataset is DeepFL, its directory can be /home/DeepLearningData/DeepFL ("/home/DeepLearningData/" is created by users, and "DeepFL" is put
into it)
2. /absolute/path/to/Result: The directory of the results. 
3. subject: The subject name, which can be Time, Chart, Lang, Math, Mockito or Closure.
4. version: The version number of the subject. Note that, the maximum numbers of subjects above are 27, 26, 65, 106, 38, 133.
5. model: The implemented model name, which can be mlp, mlp2, rnn, birnn, representing multi-layer perceptron with one hidden layer,
multi-layer perceptron with two hidden layer, recurrent neural network and Bidirectional recurrent neural network respectivly.
6. tech: The different dimensions of features, corresponding to the name of dataset, can be DeepFL, DeepFL-Metrics, DeepFL-Mutation,
DeepFL-Spectrum, DeepFL-Textual, CrossDeepFL
7. loss: The name of loss function, which can be softmax, epairwise, epairwiseSoftmax
## Results statistics##
After running all subject versions, run the following command to calculate the five measurments Top-1, Top-3, Top-5, MFR, MAR:

```
python rank_parser.py /absolute/path/to/ParentDirofDataset /absolute/path/to/Result tech model loss epoch
```




