from numpy import fft, random,frombuffer, mean, zeros, exp

class ThunderDetector:
    def __init__(self, chunklen):
        self.intensity=0
        self.old_intensity=0
        self.ledindex=0
        self.time_since_thunder=0
        self.minfbin=0    #thunder is expected between these two frequencies
        self.maxfbin = int(2500/(44100 / chunklen))
        self.prev_avg=zeros((1, chunklen))
        self.prev_max=1
        self.initflag=1;


    def detect(self, chunk, onthreshold, offthreshold, tc):
        data = frombuffer(chunk, dtype='<i2')
        fcontent = abs(fft.fft(data))
        levels = fcontent[self.minfbin:self.maxfbin]
        ctime = chunklen/44100
        if self.initflag==1:
            self.initflag=0
            self.prev_avg = fcontent[self.minfbin:self.maxfbin]
            self.prev_max=max(self.prev_avg)
        else:
            if (self.time_since_thunder==0 and any(levels >offthreshold*self.prev_avg)):
                #continuing old thunder
                self.intensity = min(255, int(255 * max(levels) / self.prev_max)) #normalize max brightness to 255
                if self.intensity==255:
                    self.prev_max=max(levels)
                self.time_since_thunder = 0
            elif any(levels > onthreshold*self.prev_avg): #new thunder
                self.intensity= min(255, int(255 * max(levels) / self.prev_max)) #normalize max brightness to 255
                self.prev_max=max(levels)
                self.time_since_thunder=0
            else: #no thunder
                self.intensity=0
                self.prev_avg = (levels+self.prev_avg)/2 #running average with 2^n weighting
                self.time_since_thunder=self.time_since_thunder+1
            if (self.old_intensity!=0):
                # some basic low pass filtering for persistence
                self.intensity = max(self.intensity, int(self.old_intensity*exp(-tc*ctime)))
        self.old_intensity=self.intensity
        return self.intensity

    def setindex(self):
        self.ledindex = int(random.uniform(0,256)) #this is correct because uniform uses the open interval not the closed
