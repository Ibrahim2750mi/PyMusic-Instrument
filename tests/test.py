from Instrument import Instrument

if __name__ == '__main__':
    piano = Instrument.Instrument()
    # 40 42 44 45 47
    # C  D  E  F  G

    # Ode to Joy
    for _ in range(2):
        for _ in range(2):
            piano.record_key(44, 0.5)
        piano.record_key(45, 0.5)
        for _ in range(2):
            piano.record_key(47, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(42, 0.5)

        for _ in range(2):
            piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(44, 0.3)
        piano.record_key(42, 0.2)
        piano.record_key(42, 0.8)

        for _ in range(2):
            piano.record_key(44, 0.5)
        piano.record_key(45, 0.5)
        for _ in range(2):
            piano.record_key(47, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(42, 0.5)

        for _ in range(2):
            piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(44, 0.3)
        piano.record_key(40, 0.2)
        piano.record_key(40, 0.8)

        piano.record_key(42, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(40, 0.5)

        piano.record_key(42, 0.5)
        piano.record_key(44, 0.2)
        piano.record_key(45, 0.2)
        piano.record_key(44, 0.5)
        piano.record_key(40, 0.5)

        piano.record_key(42, 0.5)
        piano.record_key(44, 0.25)
        piano.record_key(45, 0.25)
        piano.record_key(44, 0.5)
        piano.record_key(42, 0.5)

        piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(35, 0.5)
        piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)

    # piano.play()
    piano.clear_sample()

    for _ in range(8):
        piano.record_chord([(52, 56, 61)], 0.3)
    for _ in range(3):
        piano.record_chord([(51, 56, 61)], 0.3)
    for _ in range(5):
        piano.record_chord([(51, 56, 59)], 0.3)

    piano.play()
    piano.close()
