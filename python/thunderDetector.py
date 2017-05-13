from numpy import fft, random,frombuffer, mean

class ThunderDetector:
    def __init__(self, chunk):
        self.intensity=0
        self.ledindex=0
        self.time_since_thunder=0

    def detect(self, chunk, threshold):
        # print type(signal)
        # print type(self.delay_line)
        data = frombuffer(chunk, dtype='<i2')
        #print(max(data))
        fcontent = abs(fft.fft(data-mean(data)))
        if fcontent[4]>threshold or (self.time_since_thunder==0 and fcontent[4]>threshold/10):
            self.intensity= 255 * fcontent[4] / max(abs(fcontent)) #normalize max brightness to 255
            self.time_since_thunder=0
        else:
            self.intensity=0
            self.time_since_thunder+1
        return self.intensity

    def setindex(self):
        self.ledindex = random.uniform(0,256)
