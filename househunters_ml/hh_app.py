# This is a web application of a real estate platform called HouseHunters that
from flask import Flask, request, render_template
import pandas as pd
from househunters_ml.predict import XgBoost, col_names, test_transformation


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    """Loads the homepage"""
    return render_template('hh_home.html')


@app.route('/shutdown', methods=['GET'])
def shutdown():
    """Shuts down server"""
    shutdown_server()
    return 'Server shutting down...'


def parse_json(request):
    """Helper function to parse the data supplied in a json when loading the page"""
    house_info = request.get_json(force=True)
    return house_info


@app.route('/json_prediction', methods=['GET', 'POST'])
def predict_json():
    """
    Runs a prediction with the model based on model features supplied through a json in a curl command.
    See curl-test.sh for a test of this function.
    """
    # Create empty DataFrame with exact order of columns as needed for prediction
    df = pd.DataFrame(columns=col_names)
    print(col_names)

    house_info = parse_json(request)

    df = df.append(house_info, ignore_index=True)
    df = df.astype(int)

    # Predict
    predicted_asking_price = XgBoost.predict(df)[0]

    return ('The suggested asking price for the house is %s' % predicted_asking_price)


@app.route('/url_prediction', methods=['GET', 'POST'])
def predict_url():
    """
     Runs a prediction with the model based on model features supplied through a url.
     See curl-test.sh for a test of this function.
     """
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


def load_batch_for_prediction(data_location="data/190322 - HouseTable_vDef_excel.csv"):
    """Loads the data for a batch prediction"""
    csv_path = "data/190322 - HouseTable_vDef_excel.csv"
    test_df = pd.read_csv(r'{}'.format(csv_path),  delimiter=';', decimal=',', thousands='.')
    return test_df


@app.route('/predict_all', methods=['GET'])
def predict_all():
    """Runs a batch prediction of the model"""
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
@app.route('/post_listing', methods=['GET', 'POST'])
def post_listing():
    """Web page for posting listings, here you can choose if you are a private or business seller"""
    return render_template('hh_post_listing.html')


@app.route('/form_prediction', methods=['GET', 'POST'])
def predict_based_on_form():
    """
    Web page where once you fill in the information on your house
    you get a prediction of how much you should ask for your house
    """
    user_input = request.form

    if user_input == {}:
        return render_template('hh_private_sales_form.html')

    house_info = {}

    df = pd.DataFrame(columns=col_names)

    for column in col_names:
        house_info[column] = user_input[column]

    df = df.append(house_info, ignore_index=True)
    df = df.astype(int)

    # Predict
    predicted_asking_price = XgBoost.predict(df)[0]

    prediction_text = ('The suggested asking price for the house is ' % predicted_asking_price)

    return render_template('hh_private_sales_form.html', pred=prediction_text)


if __name__ == '__main__':
    app.run(port=5008,
            debug=True)  # Instantly see changes on the server


