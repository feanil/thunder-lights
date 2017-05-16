from numpy import fft, random,frombuffer, mean

class ThunderDetector:
    def __init__(self, chunk):
        self.intensity=0
        self.ledindex=0
        self.time_since_thunder=0
        self.minfbin=int(50/(44100/chunk))     #thunder is expected between these two frequencies
        self.maxfbin = int(700/(44100 / chunk))
        self.prev_avg=1
        self.prev_max=1


    def detect(self, chunk, onthreshold, offthreshold):
        data = frombuffer(chunk, dtype='<i2')
        fcontent = abs(fft.fft(data - mean(data)))
        level=mean(fcontent[self.minfbin:self.maxfbin])
        if self.prev_avg==1:
            self.prev_avg=level
        else:
            if (self.time_since_thunder==0 and level/self.prev_avg>offthreshold and level<self.prev_max):
                #continuing old thunder
                self.intensity = 255 * level / self.prev_max # normalize max brightness to 255
                self.time_since_thunder = 0
            elif level/self.prev_avg > onthreshold: #new thunder
                self.intensity= 255 #normalize max brightness to 255
                self.prev_max=level
                self.time_since_thunder=0
            else: #no thunder
                self.intensity=0
                self.prev_avg = mean(fcontent[self.minfbin:self.maxfbin])
                self.time_since_thunder=self.time_since_thunder+1
            return self.intensity

    def setindex(self):
        self.ledindex = random.uniform(0,256)
