import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from scipy.signal import find_peaks

# Function to process data and calculate peaks
def process_data(file):
    data = pd.read_csv(file)
    time = data['Time']
    voltage = data['Wl-ShootingVoltage']
    depth = data['Wl-Depth']
    # Finding peaks with a specified minimum height
    peaks, properties = find_peaks(-voltage, height=10)  # Negative for finding dips as peaks
    # Create a DataFrame for peaks
    peaks_df = pd.DataFrame({
        'Time': time.iloc[peaks],
        'Voltage': voltage.iloc[peaks],
        'Depth': depth.iloc[peaks],
        'Prominence': properties['peak_heights']  # Peak properties from find_peaks
    })
    return time, voltage, depth, peaks_df

# Setting up Streamlit
st.title("Visualization of Peaks in Wl-ShootingVoltage Data")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    time, voltage, depth, peaks_df = process_data(uploaded_file)

    # Creating the Plotly graph
    fig = go.Figure()

    # Adding voltage trace
    fig.add_trace(go.Scatter(x=time, y=voltage, mode='lines', name='Voltage'))
    # Adding peaks as a separate trace
    fig.add_trace(go.Scatter(x=peaks_df['Time'], y=peaks_df['Voltage'], mode='markers', marker=dict(size=8, color='red'), name='Peaks'))

    # Update layout for better visualization
    fig.update_layout(
        title='Wl-ShootingVoltage with Identified Peaks',
        xaxis_title='Time',
        yaxis_title='Wl-ShootingVoltage',
        template='plotly_white'  # Using a light theme for better visibility
    )

    # Display the plot
    st.plotly_chart(fig)

    # Display the DataFrame of peaks
    st.subheader("Details of Identified Peaks")
    st.dataframe(peaks_df)
