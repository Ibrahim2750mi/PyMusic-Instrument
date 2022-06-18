Usage
======

Piano
------

This is how piano can be supposedly played.

.. code:: py

   from Instrument import Instrument

   piano = Instrument(bit_rate = 44100)
   piano.record_key(52, duration=0.3)  # C5
   piano.record_chord([(52, 56, 61)], duration=0.3)  # C5 E5 A5

   piano.play()
   piano.close()   # Terminates PyAudio

You can look at `here <https://en.wikipedia.org/wiki/Piano_key_frequencies>`_
the key numbers for corresponding frequency.

Plotting Graph
---------------

.. code:: py

   import matplotlib.pyplot as plt

   key_colors = {40: ["red", 1], 42: ["blue", 1], 44: ["green", 1], 45: ["gray", 1],
                     47: ["orange", 1], 35: ["purple", 1], ((51, 56, 61),): ['black', 1]}

   # piano.graphing sample contains key, time take as an array, wave equation as an array.
   for key, time, wave in piano.graphing_sample:
       if key_colors[key][1]:
           plt.plot(time, wave, label=key, color=key_colors[key][0])
           key_colors[key][1] = 0
       else:
           plt.plot(time, wave, color=key_colors[key][0])

   plt.show()

Plotting Spectogram
--------------------

.. code:: py

   import librosa.display

   amplitude = librosa.stft(piano.sample)
   db = librosa.amplitude_to_db(abs(amplitude))
   plt.figure(figsize=(14, 5))
   librosa.display.specshow(db, sr=44100, x_axis='time', y_axis='hz')
   plt.colorbar()
   plt.show()
