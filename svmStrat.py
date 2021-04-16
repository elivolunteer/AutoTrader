import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
from sklearn import svm
from sklearn import utils
from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay


def plot_series(waveforms, labels):
    print(np.shape(waveforms))
    print(np.shape(labels))

    t = np.arange(len(waveforms[0]))

    np.random.shuffle(waveforms)

    for waveform in waveforms[:10]:
        plt.plot(t, waveform)
    plt.title("Training Data Waveforms")
    plt.show()

def train_svm(waveforms, labels, industry):
    print("Started training")
    #shuffle in unision
    waveforms, labels = utils.shuffle(waveforms, labels)

    #seperate training subset
    cutOff = 20000
    trainingWaveforms = waveforms[:cutOff]
    trainingLabels = labels[:cutOff]
    waveforms = waveforms[cutOff:]
    labels = labels[cutOff:]

    #train
    clf = svm.SVC()
    clf.fit(trainingWaveforms, trainingLabels)

    #metrics
    predictedLabels = clf.predict(waveforms)
    print(accuracy_score(labels, predictedLabels))
    cm = confusion_matrix(labels, predictedLabels)
    confusion_matrix_df = pd.DataFrame(cm)
    print(confusion_matrix_df)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_).plot()
    plt.matshow(cm, cmap = 'binary')
    plt.show()


    #save
    with open(f"strategies/{industry}_svm_clf.pickle", "wb") as f:
        pickle.dump(clf, f)
