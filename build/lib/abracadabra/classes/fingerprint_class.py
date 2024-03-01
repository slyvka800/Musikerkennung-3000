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

# Importing modules "from" the scripts package
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import settings


class Fingerprinting:
    def __init__(self):
            self.database = {}  # ...database to store hashes

    @staticmethod
    def my_spectrogram(audio):
        """Helper function that performs a spectrogram with the values in settings."""
        nperseg = int(settings.SAMPLE_RATE * settings.FFT_WINDOW_SIZE)
        return spectrogram(audio, settings.SAMPLE_RATE, nperseg=nperseg)

    @staticmethod
    def file_to_spectrogram(filename):
        """Calculates the spectrogram of a file.

        Converts a file to mono and resamples to :data:`~abracadabra.settings.SAMPLE_RATE` before
        calculating. Uses :data:`~abracadabra.settings.FFT_WINDOW_SIZE` for the window size.

        :param filename: Path to the file to spectrogram.
        :returns: * f - list of frequencies
                * t - list of times
                * Sxx - Power value for each time/frequency pair
        """
        a = AudioSegment.from_file(filename).set_channels(1).set_frame_rate(settings.SAMPLE_RATE)
        audio = np.frombuffer(a.raw_data, np.int16)
        return Fingerprinting.my_spectrogram(audio)

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
    def hash_point_pair(p1, p2):
        """Helper function to generate a hash from two time/frequency points."""
        return hash((p1[0], p2[0], p2[1]-p2[1]))

    @staticmethod
    def target_zone(anchor, points, width, height, t):
  
        x_min = anchor[1] + t
        x_max = x_min + width
        y_min = anchor[0] - (height*0.5)
        y_max = y_min + height
        for point in points:
            if point[0] < y_min or point[0] > y_max:
                continue
            if point[1] < x_min or point[1] > x_max:
                continue
            yield point

    
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
            for target in Fingerprinting.target_zone(
                anchor, points, settings.TARGET_T, settings.TARGET_F, settings.TARGET_START
            ):
                hashes.append((
                    Fingerprinting.hash_point_pair(anchor, target),
                    anchor[1],
                    str(song_id)
                ))
        return hashes

    #@staticmethod
    # def match_query(self, query_hashes, match_time_tolerance):
    #     """
    #     Matches query hashes against stored hashes in the database.
    #     Args -> query_hashes (list)-> List of query hashes.
    #     Returns -> dict-> Dictionary containing matched song IDs and their matched time offsets.
    #     """
    #     matched_songs = {}
    #     for hash_value, query_time_offset in query_hashes:
    #         if hash_value in self.database:
    #             for stored_time_offset, song_id in self.database[hash_value]:
    #                 time_difference = query_time_offset - stored_time_offset
    #                 if abs(time_difference) <= settings.match_time_tolerance:
    #                     if song_id not in matched_songs:
    #                         matched_songs[song_id] = []
    #                     matched_songs[song_id].append(stored_time_offset)
    #     return matched_songs
    

    @staticmethod
    def fingerprint_file(filename):
        """Generate hashes for a file.

        Given a file, runs it through the fingerprint process to produce a list of hashes from it.

        :param filename: The path to the file.
        :returns: The output of :func:`hash_points`.
        """
        f, t, Sxx = Fingerprinting.file_to_spectrogram(filename)
        peaks = Fingerprinting.find_peaks(Sxx)
        peaks = Fingerprinting.idxs_to_tf_pairs(peaks, t, f)
        return Fingerprinting.hash_points(peaks, filename)
    


if __name__ == "__main__":
    
    # #####Loads audio file
    audio_file = "../../../../Samples/test.wav"
    audio = AudioSegment.from_wav(audio_file)

    print(Fingerprinting.fingerprint_file(audio_file))
    print("our function:")
    print(Fingerprinting.fingerprint_file(audio_file))

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

