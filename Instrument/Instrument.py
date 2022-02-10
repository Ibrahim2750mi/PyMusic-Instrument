from collections.abc import Iterable

import numpy as np
import pyaudio


class Instrument:
    def __init__(self, bit_rate: int = 44100):
        self._BITRATE = bit_rate
        self._player = pyaudio.PyAudio()

        self.sample = np.array([])
        self.total_time = np.array([])
        self.play_time = 0

    @staticmethod
    def get_hz(key_number: int) -> float:
        """
        Get frequency of the key via its key number.
        :return: frequency of the key.
        """
        return 2 ** ((key_number - 49) / 12) * 440

    def record_key(self, key: int, duration: float) -> None:
        """
        Adds the key in the sample.
        :param key: The key number of the key's name.
        :param duration: Time for which the key it to be played.
        :return: None
        """
        # diving t from 0 to duration in int(self._BITRATE * duration) divisions.
        key_hz = self.get_hz(key)
        # making sure the wave ends at zero.
        phase_completer = round(key_hz * 2 * duration)/(2*key_hz) - duration
        t = np.linspace(0, duration + phase_completer, int(self._BITRATE * duration))
        # sinusoidal waves are a function of sine with args 2*pi*frequency*t.
        self.sample = np.concatenate((self.sample, np.sin(2 * np.pi * key_hz * t)))
        self.total_time = np.concatenate((self.total_time, t + self.play_time))
        self.play_time += duration

    def record_chord(self, chords: Iterable, duration: float) -> None:
        """
        Adds the given chords in the sample.
        :param chords: The iterable of chords that you want to play at same time.
        :param duration: Duration of each chord.
        """
        sinusoidal_superposition = np.empty((int(self._BITRATE * duration)))
        for chord in chords:
            for key in chord:
                key_hz = self.get_hz(key)
                phase_completer = round(key_hz * 2 * duration)/(2*key_hz) - duration
                t = np.linspace(0, duration + phase_completer, int(self._BITRATE * duration))
                sinusoidal_superposition += np.sin(2 * np.pi * key_hz * t)

        # keeping it in a range of [-1 , 1]
        sinusoidal_superposition = sinusoidal_superposition / sinusoidal_superposition.max()
        self.sample = np.concatenate((self.sample, sinusoidal_superposition))

        t = np.linspace(0, duration, int(self._BITRATE * duration))
        self.total_time = np.concatenate((self.total_time, t + self.play_time))
        self.play_time += duration

    def play(self) -> None:
        """
        Plays the sample.
        """
        parsed_sample = self.sample.astype(np.float32)
        stream = self._player.open(format=pyaudio.paFloat32,
                                   channels=1,
                                   rate=self._BITRATE,
                                   output=True,
                                   frames_per_buffer=512)

        stream.write(parsed_sample.tobytes())

        stream.stop_stream()
        stream.close()

    def close(self) -> None:
        """
        Terminates PyAudio.
        """
        self._player.terminate()

    def clear_sample(self) -> None:
        self.sample = np.array([])
