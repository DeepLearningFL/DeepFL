# DeepFL
DeepFL is a deep-learning-based fault localization technique. 

The dataset is collected from real faults project [Defects4j](https://github.com/rjust/defects4j), including different dimensions of features, e.g., spectrum-based, mutation-based, complexity-based (code metrics) and textual-similarity-based features. The dataset can be downloaded from a online [Cloud Drive](https://mega.nz/#F!ffxXBISD!UQjggpnjw8oWrjSc0D7PdA). There are six .gz files, each of them represents our setting in our paper. For example, DeepFL.tar.gz is the data with four dimensions features above and CrossDeepFL.tar.gz is just in the cross-project scenario. DeepFL-XXX.tar.gz is the the data excluding one a certain dimension, which has three dimensions features. For example, DeepFL-Metrics.tar.gz excludes complexity-based information. 

DeepFL implements two multi-layer perceptron variants and two recurrent neural networks variants by [Tensorflow](https://www.tensorflow.org/)
## Requirements ##
- Python 2/3 with Pandas and Numpy
- Tensorflow
## Running DeepFL ##

