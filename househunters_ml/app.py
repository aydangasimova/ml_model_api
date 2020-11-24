import pandas as pd
import random
import warnings
import sklearn
import pickle

pd.options.mode.chained_assignment = None

# We set a random seed to get the same results with every run
random.seed(15)

csv_path = ''

df = pd.read_csv(r'{}'.format(csv_path), header=0, sep=',')
print(df.describe())