import streamlit as st
from pydub import AudioSegment
# import pyglet ####
# from pyglet.media import Player####
import matplotlib.pyplot as plt

 
from tempfile import NamedTemporaryFile
from recogniser_class import Recogniser
from fingerprint_class import Fingerprinting
from db_manager import DataBaseManager
import tempfile
import os,sys
import librosa
#from librosa.display import waveplot


#import sounddevice 
import numpy as np
import pandas as pd
#import soundfile as sf
# import librosa
# import librosa.display
import matplotlib.pyplot as plt
import plotly.graph_objs as go


class Waveform:

    def __init__(self, audio_data, sr):
        self.audio_data = audio_data
        self.sr = sr
        

    def plot_waveform(self):
        try:
            # Calculates time values for x-axis
            time = np.arange(len(self.audio_data)) / self.sr

            # Plots waveform
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=self.audio_data, x=time, mode='lines'))

            # Adds labels and title
            fig.update_layout(
                xaxis_title="Time (seconds)",
                yaxis_title="Amplitude",
                title="Waveform of the Music Piece"
            )

            # Displays the plot
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error plotting waveform: {e}")

class Histogram:

    def __init__(self, audio_data):
        self.audio_data = audio_data

    def process_audio_for_histogram(self, audio_data):
        try:
            num_bins=10
            # Convert audio data to numpy array
            audio_array = np.array(audio_data)

            # Calculate histogram
            histogram, bin_edges = np.histogram(audio_array, bins=num_bins)
            return histogram, bin_edges
        except Exception as e:
            st.error(f"Error processing audio data: {e}")
            return None, None

    def read_audio_file(self, audio_file_path):
        try:
            sr=44100
            # Load audio file
            audio_data, _ = librosa.load(audio_file_path, sr=sr)
            return audio_data
        except Exception as e:
            print(f"Error reading audio file: {e}")
            return None

######
#if __name__ == " __main__":
    # # Create an instance of the Histogram class
    # histogram_instance = Histogram("../../../../Samples/337146__erokia__timelift-rhodes-piano.wav")

    # # Process the audio data for the histogram
    # histogram, bin_edges = histogram_instance.process_audio_for_histogram(num_bins=10)

    # # Check if the histogram and bin_edges are not None
    # if histogram is not None and bin_edges is not None:
    #     # Plot histogram
    #     fig, ax = plt.subplots()
    #     plt.bar(bin_edges[:-1], histogram, width=1)
    #     plt.xlabel('Amplitude')
    #     plt.ylabel('Frequency')
    #     plt.title('Histogram of Recognized Song')
    #     st.pyplot(fig)  # Display the histogram in Streamlit