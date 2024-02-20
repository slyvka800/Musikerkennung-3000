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
                # can't be best score, avoid expensive histogram
                continue
            score = self.score_match(offsets)
            if score > best_score:
                best_score = score
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

        
            

    