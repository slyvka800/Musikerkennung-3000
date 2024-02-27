import pyaudio
import wave


def recording_function(filename, duration:int):
        CHUNK = 1024	
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = duration

        p = pyaudio.PyAudio()
        audiostream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = audiostream.read(CHUNK)
            frames.append(data)

        audiostream.stop_stream()
        audiostream.close()
        p.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))

        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()