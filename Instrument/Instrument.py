from collections.abc import Iterable
import struct
import sys

import numpy as np
import pyaudio


class PlayerNotInitialisedError(AttributeError):
    pass


class Instrument:
    def __init__(self, bit_rate: int = 44100, no_play: bool = False):
        """
        Can play any piano notes, you have to input the key number for corresponding frequencies.
        :param bit_rate: Generally value of bit rate is 44100 or 48000,
         it is proportional to wavelength of frequency generated.
        :param no_play: Use this if you don't want to play the sample but use it for other purposes.
        """
        self._BITRATE = bit_rate
        self.no_play = no_play

        if not self.no_play:
            self._player = pyaudio.PyAudio()

        self.sample = np.array([])
        self.graphing_sample = []

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
        key_hz = self.get_hz(key)
        reciprocal_hz = 1 / key_hz
        # making sure the wave ends and starts at maxima.
        phase_completer = reciprocal_hz*(round(key_hz*duration) + 0.25) - duration
        t = np.linspace(0.25*reciprocal_hz, duration + phase_completer, round(self._BITRATE * duration))
        # sinusoidal waves are a function of sine with args 2*pi*frequency*t.
        time = t + self.play_time
        wave = np.sin(2 * np.pi * key_hz * t)

        self.graphing_sample.append((key, time, wave))

        self.sample = np.concatenate((self.sample, wave))
        self.total_time = np.concatenate((self.total_time, time))
        self.play_time += duration + phase_completer - 0.25*reciprocal_hz + 1/round(self._BITRATE * duration)

    def record_chord(self, chords: Iterable, duration: float) -> None:
        """
        Adds the given chords in the sample.
        :param chords: The iterable of chords that you want to play at same time.
        :param duration: Duration of each chord.
        """
        sinusoidal_superposition = np.empty((int(self._BITRATE * duration)))
        max_phase_completer = 0
        max_initial_deflection = 0
        for chord in chords:
            for key in chord:
                key_hz = self.get_hz(key)
                reciprocal_hz = 1 / key_hz
                # making sure the wave ends and starts at maxima.
                phase_completer = reciprocal_hz * (round(key_hz * duration) + 0.25) - duration
                initial_deflection = 0.25*reciprocal_hz
                t = np.linspace(initial_deflection, duration + phase_completer, int(self._BITRATE * duration))
                sinusoidal_superposition += np.sin(2 * np.pi * key_hz * t)

                if initial_deflection > max_initial_deflection:
                    max_initial_deflection = initial_deflection
                if phase_completer > max_phase_completer:
                    max_phase_completer = phase_completer

        # keeping it in a range of [-1 , 1]
        sinusoidal_superposition = sinusoidal_superposition / sinusoidal_superposition.max()

        t = np.linspace(max_initial_deflection, duration + max_phase_completer, int(self._BITRATE * duration))
        time = t+self.play_time
        self.graphing_sample.append((tuple(chords), time, sinusoidal_superposition))
        self.sample = np.concatenate((self.sample, sinusoidal_superposition))

        self.total_time = np.concatenate((self.total_time, time))
        self.play_time += duration + max_phase_completer - max_initial_deflection + 1/round(self._BITRATE * duration)

    def play(self) -> None:
        """
        Plays the sample.
        """
        if self.no_play:
            raise PlayerNotInitialisedError("Player not initialised")
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
        if self.no_play:
            return
        self._player.terminate()

    def clear_sample(self) -> None:
        """
        Clears the sample.
        """
        self.sample = np.array([])

    def to_wav(self, path: str) -> None:
        """
        Convert the sample to wav file format.
        :param path: Path of the file where it will be written.
        """
        # headers for wav format http://www.topherlee.com/software/pcm-tut-wavformat.html
        header = b""
        header += b'RIFF'
        # Leaving an empty space which will be left at the end.
        header += b'\x00\x00\x00\x00'
        header += b'WAVE'
        header += b"fmt "
        sample = self.sample.astype(np.float32)

        fmt_chunk = struct.pack("<HHIIHH", 3, 1, self._BITRATE, self._BITRATE*4, 4, 32)
        fmt_chunk += b"\x00\x00"

        header += struct.pack('<I', len(fmt_chunk))
        header += fmt_chunk

        # added this because it is a non-PCM file.
        header += b'fact'
        header += struct.pack('<II', 4, sample.shape[0])

        file = open(path, "wb")
        file.write(header)
        file.write(b"data")
        file.write(struct.pack('<I', sample.nbytes))

        if sample.dtype.byteorder == '=' and sys.byteorder == 'big':
            sample = sample.byteswap()

        file.write(sample.tobytes())
        # filling that empty space.
        size = file.tell()
        file.seek(4)
        file.write(struct.pack('<I', size - 8))
        file.close()
