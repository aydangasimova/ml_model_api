import numpy as np
import pandas as pd
import random
import warnings
import pickle
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

# We set a random seed to get the same results with every run
random.seed(15)

csv_path = "data/190322 - HouseTable_vDef_excel.csv"

df = pd.read_csv(r'{}'.format(csv_path),  delimiter=';', decimal=',', thousands='.')

test_df = pd.read_csv(r'{}'.format(csv_path),  delimiter=';', decimal=',', thousands='.')


# Load the model
XgBoost = pickle.load(open('model/model.pickle', 'rb'))

# Load the column names
col_names = pickle.load(open('model/columns.pickle', 'rb'))


#TODO: Figure out how this horrendous function can be improved, which parts are redundant.
def test_transformation(prediction_set):
    prediction_set_copy = prediction_set.copy()
    prediction_set_copy = prediction_set_copy.rename(columns={"#Bedrooms": "Num_Bedrooms"})

    prediction_set_copy['Age_cat'] = prediction_set_copy['ConstructionYear']
    prediction_set_copy['Age_cat'][prediction_set_copy['ConstructionYear'] < 1940] = 'Before_war'
    prediction_set_copy['Age_cat'][(prediction_set_copy['ConstructionYear'] >= 1940) &
                                   (prediction_set_copy['ConstructionYear'] < 1990)] = 'Existing'
    prediction_set_copy['Age_cat'][prediction_set_copy['ConstructionYear'] >= 1990] = 'New_construction'

    #    iii. Create dummy-variable whether a house in the city- or countryside
    cityside = ['Noord Holland',
                'Zuid Holland',
                'Utrecht'
                ]

    countryside = ['Zeeland',
                   'Fryslân',
                   'Groningen',
                   'Drenthe'
                   ]

    prediction_set_copy['CitySide'] = prediction_set_copy['Province'].isin(cityside).astype(np.int8)
    prediction_set_copy['CountrySide'] = prediction_set_copy['Province'].isin(countryside).astype(np.int8)

    prediction_set_copy['good_hood'] = (prediction_set_copy.Num_benefit_total - prediction_set_copy.Num_AOW) < 1000
    prediction_set_copy['enough_bedroom'] = prediction_set_copy['Num_Bedrooms']

    dataProv = prediction_set_copy['Province']
    dataHouse = prediction_set_copy['HouseType']
    dataAge = prediction_set_copy['Age_cat']
    dataUrban = prediction_set_copy['Urbanity_class']

    # Get/add dummies
    categoricals = ['Province',
                    'HouseType',
                    'Age_cat',
                    'Urbanity_class',
                    'Garden'
                    ]
    prediction_set_copy = pd.get_dummies(prediction_set_copy, columns=categoricals)

    # Add the original categorical column
    prediction_set_copy['Province'] = dataProv
    prediction_set_copy['HouseType'] = dataHouse
    prediction_set_copy['Age_cat'] = dataAge
    prediction_set_copy['Urbanity_class'] = dataUrban

    prediction_set_copy = prediction_set_copy[col_names]

    return prediction_set_copy


if __name__ == '__main__':

    X_predict = test_transformation(df)

    # Make new predictions
    predicted = XgBoost.predict(X_predict)

    # Save the predictions to a csv file
    X_predict['predictions'] = predicted
    X_predict.to_csv('output/predictions.csv')