"""
Case: Model Operationalization
Part 1b: Deploying a model into production
SOLUTION

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
csv_path = 'HR_new_recruitment.csv'

# We just received new data from HR.
df = pd.read_csv(r'{}'.format(csv_path), header=0, sep=',')
print(df.describe())
# Do we see changes in the production (near real-time) data compared to the training (well
# governed) data?

# Load the relevant model objects

# Load the model
forest = pickle.load(open('model.pickle', 'rb'))

# Load the column names
col_names = pickle.load(open('columns.pickle', 'rb'))

# Load the imputation mean
impute = pickle.load(open('impute.pickle', 'rb'))

# Load the scaling parameters
scale = pickle.load(open('scaling.pickle', 'rb'))

# Load the salary encoder
encode = pickle.load(open('salary_encoding.pickle', 'rb'))


# This is a test to illustrate what happens if you don't impute using the trained model, but create
# a new scaler instead.
trained_scaler_value = scale.data_range_[0]
reshaped_column = df.average_monthly_hours.values.reshape(-1, 1)
new_data_scaler = sklearn.preprocessing.MinMaxScaler().fit(reshaped_column)
new_data_scaler_value = new_data_scaler.data_range_[0]
print('Trained model Max-Min range: %0.2f' % trained_scaler_value)
print('New data Max-Min range: %0.2f' % new_data_scaler_value)
print('This will cause incorrect predictions for sure')

# What happens if you don't scale using the trained model?
print('Trained model imputation value: %0.2f' % impute)
print('New data imputation value: %0.2f' % df.satisfaction_level.mean())
print('This will cause incorrect predictions for sure')


# Create pipeline to transform the test set
# Hint - use str.replace('%','') to remove specific punctuation from a string
def test_transformation(prediction_set):
    prediction_set_copy = prediction_set.copy()
    prediction_set_copy['department'] = prediction_set_copy['department'].apply(
            lambda x: 'other' if x not in ['RandD', 'management'] else x)
    prediction_set_copy['last_evaluation'] = prediction_set.last_evaluation.str. \
        replace('%', '').astype(int) * 0.01
    prediction_set_copy = pd.concat([prediction_set_copy,
                                     pd.get_dummies(prediction_set_copy['department'])], axis=1)
    prediction_set_copy.drop('department', axis=1, inplace=True)
    prediction_set_copy.replace(encode, inplace=True)
    prediction_set_copy['hours_per_project'] = prediction_set_copy['average_monthly_hours'] / \
        prediction_set_copy['number_project']
    prediction_set_copy['average_monthly_hours'] = scale.transform(
            prediction_set_copy['average_monthly_hours'].values.reshape(-1, 1))
    prediction_set_copy.satisfaction_level.fillna(impute, inplace=True)
    prediction_set_copy = prediction_set_copy.loc[:, col_names]
    return prediction_set_copy


X_predict = test_transformation(df)

# Make new predictions
predicted = forest.predict(X_predict)

# Save the predictions to a csv file
X_predict['predictions'] = predicted
X_predict.to_csv('predictions.csv')
