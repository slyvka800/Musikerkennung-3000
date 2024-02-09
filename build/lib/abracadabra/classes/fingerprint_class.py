import uuid
import time
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter
from pydub import AudioSegment

import logging
from multiprocessing import Pool, Lock, current_process
import numpy as np
#from tinytag import TinyTag

# Importing modules from the scripts package
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import fingerprint as fp  # Hier wurde der Import geändert
import settings
from record import record_audio
#from storage import store_song, get_matches, get_info_for_song_id, song_in_db, checkpoint_db
#from fingerprint import find_peaks, my_spectrogram


class Fingerprinting:
    def __init__(self):
            self.database = {}  # ...database to store hashes

    @staticmethod
    def find_peaks(Sxx):
        data_max = maximum_filter(Sxx, size=settings.PEAK_BOX_SIZE, mode='constant', cval=0.0)
        peak_goodmask = (Sxx == data_max)
        y_peaks, x_peaks = peak_goodmask.nonzero()
        peak_values = Sxx[y_peaks, x_peaks]
        i = peak_values.argsort()[::-1]
        j = [(y_peaks[idx], x_peaks[idx]) for idx in i]
        total = Sxx.shape[0] * Sxx.shape[1]
        peak_target = int((total / (settings.PEAK_BOX_SIZE**2)) * settings.POINT_EFFICIENCY)
        return j[:peak_target]
    
    @staticmethod
    def idxs_to_tf_pairs(idxs, t, f):
        """Helper function to convert time/frequency indices into values."""
        return np.array([(f[i[0]], t[i[1]]) for i in idxs])

    @staticmethod
    def enhanced_hash_point_pair(p1, p2):
        """Erweiterte Funktion zur Generierung eines Hashes aus zwei Zeit/Frequenz-Punkten."""
        
        return hash((p1[0], p2[0], p2[1]-p2[1]))  # Nur die Zeit- und Frequenzwerte werden verwendet
    
    @staticmethod
    def store_hashes(self, hashes):
        """
        Store hashes in the database.
        Args -> hashes (list): List of tuples (hash_value, time_offset, song_id).
        """
        for hash_value, time_offset, song_id in hashes:
            if hash_value not in self.database:
                self.database[hash_value] = []
            self.database[hash_value].append((time_offset, song_id))
        return self.database


    @staticmethod
    def hash_points(points, filename):
        hashes = []
        song_id = uuid.uuid5(uuid.NAMESPACE_OID, filename).int
        for anchor in points:
            for target in fp.target_zone(
                anchor, points, settings.TARGET_T, settings.TARGET_F, settings.TARGET_START
            ):
                hashes.append((
                    fp.hash_point_pair(anchor, target),
                    anchor[1],
                    str(song_id)
                ))
        return hashes

    @staticmethod
    def match_query(self, query_hashes, match_time_tolerance):
        """
        Matches query hashes against stored hashes in the database.
        Args -> query_hashes (list)-> List of query hashes.
        Returns -> dict-> Dictionary containing matched song IDs and their matched time offsets.
        """
        matched_songs = {}
        for hash_value, query_time_offset in query_hashes:
            if hash_value in self.database:
                for stored_time_offset, song_id in self.database[hash_value]:
                    time_difference = query_time_offset - stored_time_offset
                    if abs(time_difference) <= settings.match_time_tolerance:
                        if song_id not in matched_songs:
                            matched_songs[song_id] = []
                        matched_songs[song_id].append(stored_time_offset)
        return matched_songs
    


if __name__ == "__main__":
    
    # Loads audio file
    audio_file = "../../../../Samples/test.wav"
    audio = AudioSegment.from_wav(audio_file)

    print(fp.fingerprint_file(audio_file))

#     # Converts audio to raw data
#     audio_raw = audio.raw_data
#     audio_array = np.frombuffer(audio_raw, dtype=np.int16)

#     # Get sample rate
#     sample_rate = audio.frame_rate

#     # Computes spectrogram
#     frequencies, times, Sxx = spectrogram(audio_array, sample_rate)

#     # Creates an instance of the Fingerprinting class
#     fingerprinting = Fingerprinting()

#     # Finds peaks
#     peaks = fingerprinting.find_peaks(Sxx)
    

#     # Generates hashes
#     hashes = fingerprinting.hash_points(peaks, audio_file)


#     print(peaks)
#     print(hashes)

#     fingerprinting.store_hashes(hashes)
#    # fingerprinting.match_query(hashes,5)

