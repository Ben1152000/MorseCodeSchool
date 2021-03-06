import math
import numpy
import pyaudio
from matplotlib import pyplot

class MusicBox:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=1, rate=44100, output=1)
        self.speed = 18

    def sine(self, frequency, length, rate):
        length = int(length * rate)
        factor = float(frequency) * (math.pi * 2) / rate
        wavelength = rate / float(frequency)
        length -= length % wavelength # Sine wave must end at a zero
        return numpy.sin(numpy.arange(length) * factor)

    def tone(self, stream, frequency=440, length=1, rate=44100):
        chunks = []
        wave = self.sine(frequency, length, rate)

        #print(wave[-10:-1])
        #pyplot.plot(wave)
        #pyplot.show()

        chunks.append(wave)
        chunk = numpy.concatenate(chunks) * 0.25
        self.stream.write(chunk.astype(numpy.float32).tostring())

    def dot(self, frequency):
        self.tone(self.stream, frequency, (1.2/float(self.speed)))

    def dash(self, frequency):
        self.tone(self.stream, frequency, 3*(1.2/float(self.speed)))

    def rest(self):
        self.tone(self.stream, 1/float(1.2/float(self.speed)), (1.2/float(self.speed)))

    def pause(self, number, FARNS):
        self.tone(self.stream, 1/float(1.2/float(FARNS)), number * (1.2/float(FARNS)))

    def play(self, code, frequency, speed):
        words = code.lower().split()
        for i in range(len(words)):
            for j in range(len(words[i])):
                if words[i][j] == ".":
                    self.dot(frequency)
                elif words[i][j] == "-":
                    self.dash(frequency)
                elif words[i][j] == "/":
                    self.pause(1, speed)
                if j + 1 != len(words[i]):
                    self.rest()
            if i + 1 != len(words):
                self.pause(3, speed)

    def close(self):
        STREAM.close()
        p.terminate()