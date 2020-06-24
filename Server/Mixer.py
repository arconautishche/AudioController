import platform
if platform.system=="Linux":
    import alsaaudio

class DummyMixer:
    pass

_dummy_mixer=DummyMixer()

def get_mixer():
    if platform.system=="Linux":
        return alsaaudio.Mixer(alsaaudio.mixers()[0])
    else:
        return _dummy_mixer

