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

       # Use bins spaced 0.5 seconds apart
        binwidth = 0.5
        tks = list(map(lambda x: x[0] - x[1], offsets))
        hist, _ = np.histogram(tks,
                                bins=np.arange(int(min(tks)),
                                                int(max(tks)) + binwidth + 1,
                                                binwidth))
        return np.max(hist)
    
    def best_match(self, matches):

        matched_song = None
        best_score = 0
        for song_id, offsets in matches.items():
            if len(offsets) < best_score:
                continue
            score = self.score_match(offsets)
            if score > best_score:
                best_score = score
                matched_song = song_id
        print(f"score:{score}")
        # if score > 300:
        return matched_song
        # else:
        #     return None

    
    def recognise_song(self, filename, threshold=800):

        hashes = self.fingerprinting.fingerprint_file(filename)

        matches = self.db_manager.get_matches(hashes, threshold)
        if not matches:
            return None
        matched_song = self.best_match(matches)
        #print(f"macthed_song: {matched_song}")

        if matched_song:
            info = self.db_manager.get_song_info(matched_song)
            print("info", info)
        else: 
            info = None
        #print(f"info: {info}")

        if info is not None:
            #print("in if !")
            return info
        #print("!matched song")
        return matched_song

    def compare(self):
        matches = self.db_manager.get_all_hashes()
        return_data = self.best_match(matches)
        return return_data
    

        
            

    
