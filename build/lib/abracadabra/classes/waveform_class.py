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


