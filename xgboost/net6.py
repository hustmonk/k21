import numpy as np
#import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import site;
from nolearn.dataset import Dataset
from nolearn.grid_search import *
print site.getsitepackages()
from lasagne.layers import DenseLayer
from lasagne.layers import InputLayer
from lasagne.layers import DropoutLayer
from lasagne.layers import *
from lasagne.updates import *
from lasagne.nonlinearities import softmax
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
#from nolearn.dbn import DBN
from lasagne.objectives import categorical_crossentropy
from matplotlib import pyplot
import nolearn

import sys
import logging
import logging.config
logging.config.fileConfig("log.conf")
logger = logging.getLogger("example")
class Model():
    def make_submission(self,clf, X_test, ids, encoder, name='my_neural_net_submission.csv'):
        y_prob = clf.predict_proba(X_test)
        with open(name, 'w') as f:
            for id, probs in zip(ids, y_prob):
                probas = ','.join([id] + map(str, probs.tolist()))
                f.write(probas)
                f.write('\n')
        print("Wrote submission to file {}.".format(name))

    def train(self, X, y_train, X_test, ids_test, y_test, outfile, is_valid):
        X = np.array(X)
        encoder = LabelEncoder()
        y = encoder.fit_transform(y_train).astype(np.int32)
        num_classes = len(encoder.classes_)
        num_features = X.shape[1]

        layers0 = [('input', InputLayer),
           ('dense1', DenseLayer),
           ('dropout1', DropoutLayer),
           ('dense2', DenseLayer),
           ('dropout2', DropoutLayer),
           ('output', DenseLayer)]

        net0 = NeuralNet(layers=layers0,
                 input_shape=(None, num_features),
                 dense1_num_units=3500,
                 dropout1_p=0.4,
                 dense2_num_units=2300,
                 dropout2_p=0.5,
                 output_num_units=num_classes,
                 output_nonlinearity=softmax,
                 #update=nesterov_momentum,
                 update=adagrad,
                 update_learning_rate=0.01,
                 #update_momentum=0.9,
                 #objective_loss_function=softmax,
                 objective_loss_function=categorical_crossentropy,
                 eval_size=0.2,
                 verbose=1,
                 max_epochs=20)
        net0.fit(X, y)
        X_test = np.array(X_test)
        self.make_submission(net0, X_test, ids_test, encoder)
