from numpy import fft, random,frombuffer, mean

class ThunderDetector:
    def __init__(self, chunk):
        self.intensity=0
        self.ledindex=0
        self.time_since_thunder=0
        self.minfbin=int(100/(44100/chunk))     #thunder is expected between these two frequencies
        self.maxfbin = int(1000/(44100 / chunk))
        self.prev_avg=1
        self.prev_max=0


    def detect(self, chunk, threshold):
        data = frombuffer(chunk, dtype='<i2')
        fcontent = abs(fft.fft(data - mean(data)))
        if self.prev_avg==0:
            self.prev_avg = mean(fcontent[self.minfbin:self.maxfbin])
        else:
            if mean(fcontent[self.minfbin:self.maxfbin])/self.prev_avg>threshold: #new thunder
                self.intensity= 255 #normalize max brightness to 255
                self.prev_max=mean(fcontent[self.minfbin:self.maxfbin])
                self.time_since_thunder=0
            elif (self.time_since_thunder==0 and mean(fcontent[self.minfbin:self.maxfbin])/self.prev_avg>threshold/10):
                #continuing old thunder
                self.intensity = 255 * mean(fcontent[self.minfbin:self.maxfbin]) / self.prev_max # normalize max brightness to 255
                self.time_since_thunder = 0
            else: #no thunder
                self.intensity=0
                self.prev_avg = mean(fcontent[self.minfbin:self.maxfbin])
                self.time_since_thunder=self.time_since_thunder+1
            return self.intensity

    def setindex(self):
        self.ledindex = random.uniform(0,256)
