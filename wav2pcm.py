import os
import numpy as np
# f = open("/Users/twt/Documents/pcm/far.wav")
# f.seek(0)
# f.read(44)
# data = np.fromfile(f, dtype=np.int16)
# data.tofile("/Users/twt/Documents/pcm/far.pcm")
# f.close()
f = open("/Users/twt/Documents/pcm/near_far.wav")
f.seek(0)
f.read(44)
data = np.fromfile(f, dtype=np.int16)
data.tofile("/Users/twt/Documents/pcm/near_far.pcm")
f.close()