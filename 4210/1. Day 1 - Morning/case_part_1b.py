"""
Case: Model Operationalization
Part 1b: Deploying a model into production

Good luck and have fun!
---------------------------

Welcome to the production environment!

Here we will be working with new data, that requires us to carefully transform the data and predict
on it.  Once a month, we receive a dataset with new data on the employees and we want to alert the
HR deparment if some of them are in potential risk of leaving.  The goal of this part is to
understand the required process and checks that are important to implement in production. Carefully
review the new data and transform it in a correct way - so that we can generate predictions for it.

Make sure all the files you need for the case are in the same directory as the python
scripts/notebooks.
"""

# Imports
import pandas as pd
import random
import warnings
import sklearn
import pickle
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

# We set a random seed to get the same results with every run
random.seed(15)

# Put your path to the CSV file here
csv_path = ''

# We just received new data from HR.
df = pd.read_csv(r'{}'.format(csv_path), header=0, sep=',')
print(df.describe())
# Do we see changes in the production (near real-time) data compared to the training (well
# governed) data?

# Load the relevant model objects

# Load the model
forest = ...

# Load the column names
col_names = ...

# Load the imputation mean
impute = ...

# Load the scaler
scale = ...

# Load the salary encoder
encode = ...


# Create pipeline to transform the test set
# Hint - use str.replace('%','') to remove specific punctuation from a string
def test_transformation(prediction_set):
    ...


X_predict = test_transformation(df)

# Make new predictions
predicted = ...

# Save the predictions to a csv file
X_predict['predictions'] = predicted
X_predict.to_csv('predictions.csv')


# ===========Extra exercise===========
# What happens if we do not pickle our transformations but we do recompute them? Try to figure it
# out using the following code. This is a test to illustrate what happens if you don't impute using
# the trained model, but create a new scaler instead.
trained_scaler_value = scale.data_range_[0]
reshaped_column = df.average_monthly_hours.values.reshape(-1, 1)
new_data_scaler = sklearn.preprocessing.MinMaxScaler().fit(reshaped_column)
new_data_scaler_value = new_data_scaler.data_range_[0]

print('Trained model Max-Min range: %0.2f' % trained_scaler_value)
print('New data Max-Min range: %0.2f' % new_data_scaler_value)
print('This will cause incorrect predictions for sure')

# Can you do the same for the impute?


# ===========Extra exercise===========
# Can you further improve the model by doing other transformations? For example, creating new
# variables? If so, make sure that you pickle those as well!
