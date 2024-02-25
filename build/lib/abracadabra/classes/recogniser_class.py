import uuid
import time
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter
from pydub import AudioSegment
import os, sys

import logging
from multiprocessing import Pool, Lock, current_process
import numpy as np
from tinydb import Query
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import fingerprint as fp  # Hier wurde der Import geändert
import storage
import settings
from record import record_audio
from db_manager import DataBaseManager
from fingerprint_class import Fingerprinting

KNOWN_EXTENSIONS = ["mp3", "wav", "flac", "m4a"]


class Recogniser:

    def __init__(self):
        self.db_manager = DataBaseManager()
        self.query = Query()
        self.fingerprinting = Fingerprinting

    def score_match(self, offsets):

        binwidth = 0.5
        offsets_list = list(map(lambda x: x[0] - x[1], offsets))
        hist, _ = np.histogram(offsets_list, bins=np.arange(int(min(offsets_list)),
                                            int(max(offsets_list)) + binwidth + 1,
                                            binwidth))
        return np.max(hist)

    def best_match(self, matches):
 
        matched_song = None
        best_score = 0
        for song_id, offsets in matches.items():

            if len(offsets) >= best_score and self.score_match(offsets) > best_score:
                best_score = self.score_match(offsets)
                matched_song = song_id
                
        return matched_song
    
    def recognise_song(self, filename):

        hashes = self.fingerprinting.fingerprint_file(filename)
        matches = self.db_manager.get_matches(hashes)
        matched_song = self.best_match(matches)
        info = self.db_manager.get_song_info(matched_song)
        if info is not None:
            return info
        return matched_song

    def compare(self):
        matches = self.db_manager.get_all_hashes()
        return_data = self.best_match(matches)
        return return_data

        
            

    