import pandas as pd
import streamlit as st
import pickle as pkl
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def local_css():
    return """
        <style>
  
        .main {
            background-color: #F0F4F8;
            padding: 2rem;
        }
        .stApp {
            background: linear-gradient(135deg, #F0F4F8 0%, #E1E8F0 100%);
        }
        .css-1d391kg {
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }

        .st-emotion-cache-1v0mbdj {
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }
        .st-emotion-cache-1n76uvr {
            border-radius: 12px;
        }
        .st-emotion-cache-1wivap2 {
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 1.75rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.25rem;
        }
        .prediction-box {
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 1.75rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin-top: 1.25rem;
        }
        .header-container {
            background: linear-gradient(135deg, #005BBB 0%, #003876 100%);
            padding: 2.5rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2.5rem;
            box-shadow: 0 4px 12px rgba(0, 91, 187, 0.2);
        }
        .sidebar-header {
            background: linear-gradient(135deg, #005BBB 0%, #003876 100%);
            color: white;
            padding: 1.25rem;
            border-radius: 12px;
            margin-bottom: 1.25rem;
            box-shadow: 0 4px 12px rgba(0, 91, 187, 0.2);
        }
        .slider-label {
            color: #111111;
            font-weight: 500;
            margin-bottom: 0.75rem;
        }
        /* Enhanced slider styling */
        .stSlider > div > div > div {
            background-color: #0000000;
        }
        .stSlider > div > div > div > div {
            background-color: #005BBB;
        }
        /* Custom button styling */
        .stButton > button {
            background-color: #005BBB;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            box-shadow: 0 2px 4px rgba(0, 91, 187, 0.2);
        }
        .stButton > button:hover {
            background-color: #003876;
        }
        /* Custom metrics styling */
        .metric-container {
            background-color: #FFFFFF;
            padding: 1.25rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin: 1rem 0;
        }
        
        </style>
    """


def get_clean_data():
    data = pd.read_csv("data/data.csv")
    data = data.drop(['id', 'Unnamed: 32'], axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M':1, "B":0})
    print("Available columns:", data.columns.tolist())  # Add this line
    return data

def add_sidebar():
    st.markdown("""
        <div class="sidebar-header">
            <h3 style='margin-bottom: 0px;'>Cell Nuclei Measurements</h3>
            <small>Adjust the values using the sliders below</small>
        </div>
    """, unsafe_allow_html=True)

    data = get_clean_data()
    
    # Group measurements for better organization
    measurement_groups = {
        "Mean Values": [
            ("Radius (mean)", "radius_mean"),
            ("Texture (mean)", "texture_mean"),
            ("Perimeter (mean)", "perimeter_mean"),
            ("Area (mean)", "area_mean"),
            ("Smoothness (mean)", "smoothness_mean"),
            ("Compactness (mean)", "compactness_mean"),
            ("Concavity (mean)", "concavity_mean"),
            ("Concave points (mean)", "concave points_mean"),
            ("Symmetry (mean)", "symmetry_mean"),
            ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ],
        "Standard Error": [
            ("Radius (se)", "radius_se"),
            ("Texture (se)", "texture_se"),
            ("Perimeter (se)", "perimeter_se"),
            ("Area (se)", "area_se"),
            ("Smoothness (se)", "smoothness_se"),
            ("Compactness (se)", "compactness_se"),
            ("Concavity (se)", "concavity_se"),
            ("Concave points (se)", "concave points_se"),
            ("Symmetry (se)", "symmetry_se"),
            ("Fractal dimension (se)", "fractal_dimension_se"),
        ],
        "Worst Values": [
            ("Radius (worst)", "radius_worst"),
            ("Texture (worst)", "texture_worst"),
            ("Perimeter (worst)", "perimeter_worst"),
            ("Area (worst)", "area_worst"),
            ("Smoothness (worst)", "smoothness_worst"),
            ("Compactness (worst)", "compactness_worst"),
            ("Concavity (worst)", "concavity_worst"),
            ("Concave points (worst)", "concave points_worst"),
            ("Symmetry (worst)", "symmetry_worst"),
            ("Fractal dimension (worst)", "fractal_dimension_worst"),
        ]
    }

    input_dict = {}

    for group_name, sliders in measurement_groups.items():
        st.sidebar.markdown(f"### {group_name}")
        for label, key in sliders:
            input_dict[key] = st.sidebar.slider(
                label,
                min_value=float(0),
                max_value=float(data[key].max()),
                value=float(data[key].mean()),
                help=f"Adjust the {label.lower()} value"
            )
    
    return input_dict

def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data.drop(['diagnosis'], axis=1)
    
    scaled_dict = {}
    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val)/(max_val - min_val)
        scaled_dict[key] = scaled_value
    
    return scaled_dict

def get_radar_chart(input_data):
    input_data = get_scaled_values(input_data)
    
    categories = ['Radius', 'Texture', 'Perimeter', 'Area',
                 'Smoothness', 'Compactness', 'Concavity', 
                 'Concave Points', 'Symmetry', 'Fractal Dimension']
    
    def get_value(category, suffix):
        category = category.lower()
        if category == 'concave points':
            category = 'concave points'
        else:
            category = category.replace(' ', '_')
            
        key = f'{category}_{suffix}'
        return input_data.get(key, 0)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[get_value(cat, 'mean') for cat in categories],
        theta=categories,
        fill='toself',
        name='Mean Value',
        line_color='rgb(0, 91, 187)',
        fillcolor='rgba(0, 91, 187, 0.2)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[get_value(cat, 'se') for cat in categories],
        theta=categories,
        fill='toself',
        name='Standard Error',
        line_color='rgb(41, 128, 185)',
        fillcolor='rgba(41, 128, 185, 0.2)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[get_value(cat, 'worst') for cat in categories],
        theta=categories,
        fill='toself',
        name='Worst Value',
        line_color='rgb(192, 57, 43)',
        fillcolor='rgba(192, 57, 43, 0.2)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor='rgba(0, 0, 0, 0.1)',
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=12,
                    color='#2C3E50'
                ),
                linecolor='#2C3E50',
            ),
            bgcolor='rgba(255, 255, 255, 0.95)',
        ),
        showlegend=True,
        legend=dict(
            bgcolor='#f7dc6f',
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=1,
            font=dict(
                size=12,
                color='#2C3E50'
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=40, b=40)
    )

    return fig

def add_prediction(input_data):
    model = pkl.load(open('model/model.pkl', 'rb'))
    scaler = pkl.load(open('model/scaler.pkl', 'rb'))

    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)
    prediction = model.predict(input_array_scaled)
    prediction_proba = model.predict_proba(input_array_scaled)[0]

    st.markdown("""
        <div class="prediction-box">
            <h3 style='color: #2C3E50;'>Diagnosis Prediction</h3>
    """, unsafe_allow_html=True)

    # Enhanced prediction result styling
    if prediction[0] == 0:
        st.markdown("""
            <div style='background-color: #EBF5E9; color: #1B5E20; padding: 1.25rem; border-radius: 12px; margin-bottom: 1.25rem; border-left: 5px solid #2E7D32;'>
                <h4 style='margin: 0; color: #2E7D32;'>Benign</h4>
                <p style='margin: 0.5rem 0 0 0;'>The cell cluster appears to be non-cancerous.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background-color: #FDECEA; color: #B71C1C; padding: 1.25rem; border-radius: 12px; margin-bottom: 1.25rem; border-left: 5px solid #C62828;'>
                <h4 style='margin: 0; color: #C62828;'>Malignant</h4>
                <p style='margin: 0.5rem 0 0 0;'>The cell cluster appears to be cancerous.</p>
            </div>
        """, unsafe_allow_html=True)

    # Enhanced gauge charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_benign = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction_proba[0] * 100,
            title={'text': "Probability of Benign", 'font': {'color': '#2C3E50'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#2C3E50"},
                'bar': {'color': "#2E7D32"},
                'steps': [
                    {'range': [0, 50], 'color': "#F5F5F5"},
                    {'range': [50, 100], 'color': "#EBF5E9"}
                ],
                'threshold': {
                    'line': {'color': "#2E7D32", 'width': 4},
                    'thickness': 0.75,
                    'value': prediction_proba[0] * 100
                }
            }))
        st.plotly_chart(fig_benign)

    with col2:
        fig_malignant = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction_proba[1] * 100,
            title={'text': "Probability of Malignant", 'font': {'color': '#2C3E50'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#2C3E50"},
                'bar': {'color': "#C62828"},
                'steps': [
                    {'range': [0, 50], 'color': "#F5F5F5"},
                    {'range': [50, 100], 'color': "#FDECEA"}
                ],
                'threshold': {
                    'line': {'color': "#C62828", 'width': 4},
                    'thickness': 0.75,
                    'value': prediction_proba[1] * 100
                }
            }))
        st.plotly_chart(fig_malignant)

    # Enhanced disclaimer
    st.markdown("""
        <div style='background-color: #F8F9FA; color: #2C3E50; padding: 1.25rem; border-radius: 12px; margin-top: 1.25rem; border: 1px solid #E1E8F0;'>
            <p style='margin: 0; font-size: 0.9rem;'><strong>Disclaimer:</strong> This tool is designed to assist medical professionals in diagnosis but should not be used as a substitute for professional medical judgment. Always consult with qualified healthcare providers for medical decisions.</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title='Breast Cancer Prediction Tool',
        page_icon="🎗️",
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.markdown(local_css(), unsafe_allow_html=True)

    st.markdown("""
        <div class="header-container">
            <h1 style='margin-bottom: 0.5rem;'>Breast Cancer Diagnosis Assistant</h1>
            <p style='margin-bottom: 0; opacity: 0.9;'>An AI-powered tool to assist medical professionals in breast cancer diagnosis</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: white; padding: 1.75rem; border-radius: 15px; margin-bottom: 2.5rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);'>
            <h4 style='color: #2C3E50; margin-bottom: 1rem;'>About This Tool</h4>
            <p style='color: #34495E;'>This application uses machine learning to analyze breast cell nuclei measurements and predict whether a mass is benign or malignant. The tool processes various cellular characteristics measured from fine needle aspirates (FNA) of breast masses.</p>
            <p style='color: #34495E; margin-bottom: 0;'>Use the sliders in the sidebar to adjust measurements or connect directly to your cytology lab's digital output.</p>
        </div>
    """, unsafe_allow_html=True)

    input_data = add_sidebar()
    col1, col2 = st.columns([5, 4])

    with col1:
        st.markdown("""
            <div style='background-color: white; padding: 1.75rem; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);'>
                <h4 style='color: #2C3E50; margin-bottom: 1rem;'>Cellular Features Visualization</h4>
            </div>
        """, unsafe_allow_html=True)
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart, use_container_width=True)

    with col2:
        add_prediction(input_data)

    st.markdown("""
        <div style='background-color: #F8F9FA; padding: 1.25rem; border-radius: 12px; margin-top: 2.5rem; text-align: center; border: 1px solid #E1E8F0;'>
            <small style='color: #6C757D;'>Last updated: {} UTC</small>
        </div>
    """.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)

if __name__ == '__main__':
    main()