import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle as pkl


def create_model(data):
    X = data.drop('diagnosis', axis = 1)
    y = data['diagnosis']

    # split the data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 80, random_state=1)

    #scaling
    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # model building
    model = LogisticRegression() # 97.5
    model.fit(X_train, y_train)

    #prediction model
    y_pred = model.predict(X_test)
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    return model, scaler


def get_clean_data():
    data = pd.read_csv("A:/Users/VARSHA/Downloads/streamlit tutorial/Breast Cancer Prediction/data/data.csv")

    data = data.drop(['id', 'Unnamed: 32'], axis = 1)

    data['diagnosis'] = data['diagnosis'].map({'M':1, "B":0})
    return data


def main():
    data = get_clean_data()
    # print(data.info())
    model, scaler = create_model(data)

    with open('model/model.pkl', 'wb') as f:
        pkl.dump(model, f)

    with open('model/scaler.pkl', 'wb') as g:
        pkl.dump(scaler, g)

if __name__ == '__main__':
    main()