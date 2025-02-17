# Breast Cancer Diagnosis Predictor

## Overview
The **Breast Cancer Diagnosis Predictor** is a machine learning-powered application designed to assist medical professionals in diagnosing breast cancer. By analyzing specific measurements, it predicts whether a breast mass is **benign** or **malignant**. The app provides a visual representation of the input data using a **radar chart** and displays the predicted diagnosis along with the probability of malignancy or benignity.

Users can either **manually input measurements** or integrate the app with a **cytology lab** to retrieve data directly from laboratory machines. However, this integration is external and not included within the app itself.

> **Note:** This project was developed as an educational machine learning exercise using the publicly available **Breast Cancer Wisconsin (Diagnostic) Dataset**. As such, it is not intended for professional medical use.

## Features
- **Machine Learning-Based Prediction:** Identifies whether a breast mass is benign or malignant.
- **Radar Chart Visualization:** Displays a graphical representation of the input data.
- **Probability Score:** Provides a confidence level for each diagnosis.
- **Manual & Automated Data Input:** Users can manually enter data or integrate it with lab systems.

## Dataset
The model is trained using the **Breast Cancer Wisconsin (Diagnostic) Dataset**, which is publicly available. It includes several key features such as:
- Radius
- Texture
- Perimeter
- Area
- Smoothness
- etc.

More details on the dataset can be found [here](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic)).

## Live Demo
A live version of the application is available on **[Streamlit Community Cloud](https://breast-cancer-predictor-vjpdcdsbuuswpstgyuqrda.streamlit.app/)**.

## Limitations
- **Not for Clinical Use:** This app is for educational purposes only and should not be used for real medical diagnoses.
- **Dataset Reliability:** The dataset is publicly available but may not be suitable for real-world medical applications.
