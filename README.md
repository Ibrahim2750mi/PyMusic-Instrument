# About
A python library which can generate sounds played by instruments mainly guitar and piano. It uses PyAudio as its
dependency.

# Getting Started
## Pre-requisites 
You just need to know basic python syntax to use this library.

## Installation
If in your machine previously you have never installed PyAudio then do this:<br>

### Unix:<br>
`sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`

### Windows:<br>
Download the binaries from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
<br> Now do this<br>
`pip install PyAudio‑0.2.11‑cp39‑cp39m‑win_amd64.whl`

Then<br>
`python3 -m pip install PyMusic-Instrument`


# Usage

Playing piano notes.
```python
from Instrument import Instrument

piano = Instrument(bit_rate = 44100)
piano.record_key(52, duration=0.3)  # C5
piano.record_chord([(52, 56, 61)])  # C5 E5 A5

piano.play()
piano.close()   # Terminates PyAudio
```

Playing guitar strings.
```python
guitar = Instrument(44100)
guitar.record_key(25, duration=0.5)  # A
guitar.play()
guitar.clear_sample()  # clears the sample
guitar.close()
```

You can look at [here](https://en.wikipedia.org/wiki/Piano_key_frequencies)
the key numbers for corresponding frequency.

Alternatively you can also plot the graph

```python
import matplotlib.pyplot as plt

plt.plot(piano.total_time, piano.sample)
plt.show()
```
Or the spectogram

```python
import librosa.display

amplitude = librosa.stft(piano.sample)
db = librosa.amplitude_to_db(abs(amplitude))
plt.figure(figsize=(14, 5))
librosa.display.specshow(db, sr=44100, x_axis='time', y_axis='hz')
plt.colorbar()
plt.show()
```
