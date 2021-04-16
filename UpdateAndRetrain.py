import genTrainingData
import numpy as np
import pickle
import SP500
import svmStrat
import sys

def main(args):
    #check command line
    if len(args) < 3:
        print("Usage: UpdateAndRetrain.py <Industry> (IT, HC, Energy) <Strategy> (SVM)")
        return 1

    SP500.get_data_from_yahoo()

    # Gen new data depending on the given industry
    if args[1] == "IT":
        genTrainingData.genIT_bsh()
    elif args[1] == "HC":
        genTrainingData.genHC_bsh()
    elif args[1] == "Energy":
        genTrainingData.genEnergy_bsh()
    else:
        print("Unable to generate training for %s" % args[1])

    # Load in new data
    with open(f"serialized_data/{args[1]}_waveforms.pickle", "rb") as f:
        waveforms = pickle.load(f)
        waveforms = np.delete(waveforms,[0],0)
    with open(f"serialized_data/{args[1]}_labels.pickle", "rb") as f:
        labels = pickle.load(f)

    # Retrain based on given model
    if args[2] == "SVM":
        svmStrat.train_svm(waveforms, labels, args[1])

if __name__ == '__main__':
    main(sys.argv[0:])
