"""
Case: Model Operationalization
Part 3: Deploying your model behind an api

Good luck and have fun!
---------------------------

After creating the model in case part 1 and creating your own API routes in part 2,
it is now time to combine both! You are going to put your model behind an API.

This part of the case consists of the following exercises:
1. Single prediction: pass the features as API parameters and get a returned prediction
2. Batch prediction: use an API to trigger predictions for a whole batch of data
3. Trigger your model from a form in an application

Small extra exercise: if you finish early, use the requests package from yesterday to call your
model API from python (part 2 extra)
"""


# Exercise 1.Put the model behind an API
# The basic web server from before, add your new routes to this basic version!
# Instructions are put in comments in between the code!
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

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


# A server shutdown function
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# Initialize the server
app = Flask(__name__)

# Your first API! It is a GET request that simply returns some text.
@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to your first web server!'

# This is our route that shuts down the server
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


"""
Now it's time to put your model behind an API.
We will start by having the API return a prediction for one person (one datapoint).  Next (in
exercise 2), we will create an API that will make a prediction for all people in the dataset and
write this to a new csv.

We pass the parameters that our model needs through the API into the model. The API will return
whether the model predicted that someone would leave or not.  Keep in mind that the parameter in the
url is a string and you might have to convert it to the data type your model expects.

What steps should you follow to achieve this in your API route? Have a look below:
    1. Extract the parameters from the URL request
    2. Load the model objects using pickle
    3. Insert the user input variables into a dictoionary and append it to a DataFrame
    4. Make the prediction
    5. Return whether the employee will leave or not based on the predicted value

Tip: Try to write steps 2, 3 and 4 seperately before putting them into the API, since the syntax can
be confusing.  This will make debugging much easier! And have a look at the code from part 1 of the
case (train the model), that can help you along.

We can send multiple parameters in the URL like:

http://127.0.0.1:5000/returnName?name=Charlotte&age=45&height=179
"""


# This function dummifies the department variables using a dictionary You can use it in your
# transformation pipeline.
def dummify_department(value, dict_x):
    if value == 'RandD':
        dict_x['RandD'] = 1
        dict_x['management'] = 0
        dict_x['other'] = 0
    elif value == 'management':
        dict_x['RandD'] = 0
        dict_x['management'] = 1
        dict_x['other'] = 0
    else:
        dict_x['RandD'] = 0
        dict_x['management'] = 0
        dict_x['other'] = 1
    return dict_x


# The route that takes the parameters and returns a prediction for one datapoint
@app.route('/predict', methods=['GET'])
def predict():
    # Create empty dictionary to insert the variables to
    dict_x = {}

    # Create empty DataFrame with exact order of columns as needed for prediction
    df = pd.DataFrame(columns=col_names)

    # Define columns that should be extracted from the API
    # Variables like hours per project are not asked from the user, but calculated in the backend
    variables = ['average_monthly_hours',
                 'salary',
                 'number_project',
                 'last_evaluation',
                 'satisfaction_level',
                 'department']

    # Use a loop to extract variable by variable and handle each one.
    # this step should make sure of several things:
    # 1. average monthly hours, number of projects, satisfaction level (remember: might need to be
    #       imputed) and last evaluation should be saved as float
    # 2. salary should be kept as string
    # 3. department should be dummified using the function above
    for variable in variables:
        if variable in ('average_monthly_hours', 'number_project'):
            dict_x[variable] = float(request.args.get(variable))
        elif variable in ('satisfaction_level') and request.args.get(variable) == '':
            # If satisfaction level is null, fill with the imputated value.
            dict_x[variable] = impute
        elif variable in ('satisfaction_level', 'last_evaluation'):
            dict_x[variable] = float(request.args.get(variable))
        elif variable in ('salary'):
            # Since we expect a string and not a float, we should add this part
            dict_x[variable] = request.args.get(variable)
        else:
            # Dummify department variables
            dict_x = dummify_department(request.args.get(variable), dict_x)

    # Create hours per project
    dict_x['hours_per_project'] = dict_x['average_monthly_hours'] / dict_x['number_project']

    # Append dictionary to the empty Dataset
    df = df.append(dict_x, ignore_index=True)

    # Apply the rest of the transformations(salary encoding, monthly hours scaling)
    # Encode salary
    df.replace(encode, inplace=True)

    # Scale monthly hours
    df['average_monthly_hours'] = scale.transform(df['average_monthly_hours'].values.reshape(1, -1))

    # Predict
    prediction = forest.predict(np.array(df).reshape(1, -1))[0]
    if prediction == 0:
        return "Prediction: Employee won't leave"

    return "Prediction: Employee will leave"


# Exercise 2: Create an API route that will make a prediction on the full dataset and writes this to
# a new CSV

"""
Next we will make a prediction on all datapoints and write (together with the data one each person)
to a new CSV.  Write a new route that will take no parameters, but will do a prediction on the full
dataset. Therefore the route should:

This is a simple example of model operationalization: we can initiate a quick process where a user
can send some datapoints, and receive the model output in return.

In a (slightly) more complex version of this exercise, the user would upload it's own datapoints and
receive a new csv with predictions to download from the server.

Steps:

    1. Import the data from the csv (HR_new_recruitment.csv)
    2. Load the model objects and pipeline and make a prediction on the data
    3. Append these predicitons as a new column to the dataframe that has all the data
    4. Write this dataframe to a new csv file (Pandas dataframes have a method to write the
            dataframe to csv!)
    5. Return on the API route whether the prediction process went successfully or not

"""

def test_transformation(prediction_set):
    prediction_set_copy = prediction_set.copy()
    prediction_set_copy['department'] = prediction_set_copy['department'].apply(lambda x: 'other' if x not in ['RandD','management'] else x)
    prediction_set_copy['last_evaluation'] = prediction_set.last_evaluation.str.replace('%','').astype(int) * 0.01
    prediction_set_copy = pd.concat([prediction_set_copy, pd.get_dummies(prediction_set_copy['department'])], axis=1)
    prediction_set_copy.drop('department', axis=1, inplace=True)
    prediction_set_copy.replace(encode, inplace=True)
    prediction_set_copy['hours_per_project'] = prediction_set_copy['average_monthly_hours'] / prediction_set_copy['number_project']
    prediction_set_copy['average_monthly_hours'] = scale.transform(prediction_set_copy['average_monthly_hours'].values.reshape(-1, 1))
    prediction_set_copy.satisfaction_level.fillna(impute, inplace=True)
    prediction_set_copy = prediction_set_copy.loc[:, col_names]
    return prediction_set_copy


# The route that makes a prediction on all data and writes this to a new CSV We use a try/except to
# here to catch any errors during the API call and still return something when an error happens
# Without this try/except the server can just crash when something goes wrong without returning
# valuable info
@app.route('/predict_all', methods=['GET'])
def predict_all():
    # Hint: you can use the test_transformation function you have made yesterday!
    try:
        df = pd.read_csv(r"HR_new_recruitment.csv", header=0, sep=",")
        X_predict = test_transformation(df)


        # Make new predictions
        predicted = forest.predict(X_predict)

        # Save the predictions to a csv file
        X_predict['correct_prediction'] = predicted
        X_predict.to_csv('correct_predictions.csv', header=True)
        return 'prediction was successful'
    except Exception:
        return 'Error occured'


# Exercise 3: Your first 'web app' using a form
"""
It is now time to take things one step further. We will use an index.html file so we have a
'front-end' and very basic web app.  The index.html page will display a form where characteristics
about someone can be entered (instead of in the URL) and a prediction will be returned by the model.
In order to do this we will use a POST request instead of a GET request.

First check out the /index route to see how the form will look like.  When you press 'estimate if
employee will leave' these will be send to the route predict_post. Can you make sure the correct
prediction is returned?
"""

# /Index route that displays the form
@app.route('/index')
def index():
    # A form that sends a post request to /predict_post
    return render_template('index.html')


# Define a route that receives a post request and returns the form together with a prediction
@app.route('/predict_post', methods=['POST'])
def pred_post():
    # We have extracted a dictionary with all variables:values pairs
    user_input = request.form

    # Create empty DataFrame with exact order of columns
    df = pd.DataFrame(columns=col_names)
    dict_x = {}

    # Apply a similar loop as before
    # Think - what has changed from the input we received from the URL?
    # Are we expecting to get the same format for the different variables?
    for variable in user_input:
        if variable in ('average_monthly_hours', 'number_project'):
            dict_x[variable] = float(user_input[variable])
        elif variable in ('satisfaction_level') and user_input[variable] == '':
            # If satisfaction level is null, fill with the imputated value
            dict_x[variable] = impute
        elif variable in ('satisfaction_level', 'last_evaluation'):
            dict_x[variable] = float(user_input[variable]) / 100
        elif variable in ('salary'):
            # Since we expect a string and not a float, we should add this part
            dict_x[variable] = user_input[variable]
        else:
            # Dummify department variables
            dict_x = dummify_department(user_input[variable], dict_x)

    # Create new variable
    dict_x['hours_per_project'] = dict_x['average_monthly_hours']/dict_x['number_project']

    # Append the dictionary
    df = df.append(dict_x, ignore_index=True)

    # Apply the rest of the transformations
    # Encode salary
    df.replace(encode, inplace=True)

    # Scale monthly hours
    df['average_monthly_hours'] = scale.transform(df['average_monthly_hours'].values.reshape(1, -1))

    # Predict
    prediction = forest.predict(np.array(df).reshape(1, -1))[0]
    prediction_text = 'Employee will leave' if prediction == 1 else "Employee won't leave"
    return render_template('index.html', pred=prediction_text)


# Extra: Call the API with your model behind it from Python

"""
Call the API directly from python.

We can also call the API directly from python without opening the link to the server in our browser.
You already did this yesterday using the requests module, otherwhise check case part 3 extra.
"""

# Add code here to call the API directly from python


# Move this condition to the end of your script every time you add a new part
if __name__ == '__main__':
    app.run(port=5008,
            debug=True)
