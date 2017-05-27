from numpy import fft, random,frombuffer, mean, zeros

class ThunderDetector:
    def __init__(self, chunk):
        self.intensity=0
        self.ledindex=0
        self.time_since_thunder=0
        self.minfbin=0    #thunder is expected between these two frequencies
        self.maxfbin = int(2500/(44100 / chunk))
        self.prev_avg=zeros((1, chunk))
        self.prev_max=1
        self.initflag=1;


    def detect(self, chunk, onthreshold, offthreshold):
        data = frombuffer(chunk, dtype='<i2')
        fcontent = abs(fft.fft(data))
        levels = fcontent[self.minfbin:self.maxfbin]
        if self.initflag==1:
            self.initflag=0
            self.prev_avg = fcontent[self.minfbin:self.maxfbin]
            self.prev_max=max(self.prev_avg)
        else:
            if (self.time_since_thunder==0 and any(levels >offthreshold*self.prev_avg)):
                #continuing old thunder
                self.intensity = min(255, 255 * max(levels) / self.prev_max) # normalize max brightness to 255
                if self.intensity==255:
                    self.prev_max=max(levels)
                self.time_since_thunder = 0
            elif any(levels > onthreshold*self.prev_avg): #new thunder
                self.intensity= 255 #normalize max brightness to 255
                self.prev_max=max(levels)
                self.time_since_thunder=0
            else: #no thunder
                self.intensity=0
                self.prev_avg = (fcontent[self.minfbin:self.maxfbin]+self.prev_avg)/2
                self.time_since_thunder=self.time_since_thunder+1
            return self.intensity

    def setindex(self):
        self.ledindex = random.uniform(0,256)
