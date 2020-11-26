from flask import Flask, request, render_template
import pandas as pd
from househunters_ml.predict import XgBoost, col_names, test_transformation



# endpoint = 'http://127.0.0.1:5008/predict_post'
#
# # The request parameters (in a Python dictionary)
# house_info = {'LivingArea_m2': 90,
#               'QuietRoad': 1,
#               '#Bedrooms': 3,
#               'StatusRank': 2233,
#               'Avg_house_value_WOZ_1000euros': 600,
#               'Avg_WOZ_m2': 60,
#               'CitySide': 1,
#               'HouseType_Detached': 0,
#               'Age_cat_Before war': 0,
#               'Urbanity_class_5': 1}
#
# # Make the request
# r = request.post(url=endpoint, data=house_info)
#
# # Extract the response
# response_text = r.text
# print(response_text)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to HouseHunters'


@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, please enter the information on the house you want to sell, and we will give you a price rec!'


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/json_prediction', methods=['GET', 'POST'])
def predict_json():
    # Create empty DataFrame with exact order of columns as needed for prediction
    df = pd.DataFrame(columns=col_names)
    print(col_names)

    house_info = parse_json(request)

    df = df.append(house_info, ignore_index=True)
    df = df.astype(int)

    # Predict
    predicted_asking_price = XgBoost.predict(df)[0]

    return ('The suggested asking price for the house is %s' % predicted_asking_price)


def parse_json(request):
    house_info = request.get_json(force=True)
    return house_info


@app.route('/url_prediction', methods=['GET', 'POST'])
def predict_url():
    # Create empty DataFrame with exact order of columns as needed for prediction
    house_info = {}

    df = pd.DataFrame(columns=col_names)

    for column in col_names:
        house_info[column] = request.args.get(column)

    df = df.append(house_info, ignore_index=True)
    print(df.values)
    df = df.astype(int)
    print(df.dtypes)

    # Predict
    predicted_asking_price = XgBoost.predict(df)[0]

    return ('The suggested asking price for the house is %s' % predicted_asking_price)

# Test using this
# http://127.0.0.1:5008/url_prediction?LivingArea_m2=90&QuietRoad=1&#Bedrooms=3&StatusRank=2233&Avg_house_value_WOZ_1000euros=600&Avg_WOZ_m2=60&CitySide=1&HouseType_Detached=0&Age_cat_Before_war=0&Urbanity_class_5=1


def load_batch_for_prediction(data_location="data/190322 - HouseTable_vDef_excel.csv"):
    csv_path = "data/190322 - HouseTable_vDef_excel.csv"
    test_df = pd.read_csv(r'{}'.format(csv_path),  delimiter=';', decimal=',', thousands='.')
    return test_df


@app.route('/predict_all', methods=['GET'])
def predict_all():
    # Hint: you can use the test_transformation function you have made yesterday!
    try:
        X_predict = test_transformation(load_batch_for_prediction())

        # Make new predictions
        predicted = XgBoost.predict(X_predict)

        # Save the predictions to a csv file
        X_predict['correct_prediction'] = predicted
        X_predict.to_csv('batch_predictions.csv', header=True)
        return 'prediction was successful'

    except Exception as e:
        print(e)
        return 'Error occurred'


# /Index route that displays the form
@app.route('/post_listing')
def my_template():
    return render_template('hh_post_listing.html')


@app.route('/form')
def show_form():
    # A form that sends a post request to /predict_based_on_form when the submit button is clicked
    return render_template('hh_private_sales_form.html')


@app.route('/form_prediction')
def predict_based_on_form():
    user_input = request.form
    print(user_input)
    return render_template('hh_private_sales_form.html')
    # return render_template('hh_private_sales_form.html', pred=prediction_text)


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


if __name__ == '__main__':
    app.run(port=5008,
            debug=True)  # Instantly see changes on the server


