from numpy import fft, random,frombuffer, mean, zeros, exp, ones

class ThunderDetector:
    def __init__(self, chunklen):
        self.intensity = 0
        self.old_intensity = 0
        self.ledindex = 0
        self.time_since_thunder = 0
        self.minfbin = 0    #thunder is expected between these two frequencies
        self.maxfbin = int(4000/(44100 / chunklen)) + 1
        self.noisebuflen = int(200*4096/chunklen) #empirically determined from MATLAB tests
        self.noisebuf = ones((self.noisebuflen))
        self.noiseindex = 0
        self.prev_max = 1
        self.initflag = 1
        self.chunklen = chunklen


    def detect(self, chunk, onthreshold, offthreshold, tc):
        data = frombuffer(chunk, dtype='<i2')
        fcontent = abs(fft.fft(data))
        ctime = self.chunklen/44100
        
        #mean signal level in freq range of interest
        levels = mean(fcontent[self.minfbin:self.maxfbin]) 
#        print "Levels: {}".format(levels)
#        print "PrevMax: {}".format(self.prev_max)
#        print "Noise min: {}".format(min(self.noisebuf))
#        print "Noise max: {}".format(max(self.noisebuf))
#        print "Noise mean: {}".format(mean(self.noisebuf))
#        print "Noise index: {}".format(self.noiseindex)

        if self.initflag == 1:
        
            self.initflag=0
            #fill the whole noise buffer with the current signal level - it will take a while to converge
            self.noisebuf[0] = mean(fcontent[self.minfbin:self.maxfbin])
            new_prev_max =max(fcontent[self.minfbin:self.maxfbin]) 
            self.prev_max=max(new_prev_max,1)
            self.index_since_init=0;
            
        else:
        
            if (self.time_since_thunder == 0 and levels > (offthreshold * self.noisebuf[self.noiseindex])):
                #continuing old thunder
                self.intensity = min(255, int(255 * levels / self.prev_max)) #normalize max brightness to 255
                if self.intensity == 255:
                    self.prev_max=max(levels,1)
                self.time_since_thunder = 0
                
            elif levels > (onthreshold * self.noisebuf[self.noiseindex]): 
            	#new thunder
                self.intensity = min(255, int(255 * levels / self.prev_max)) #normalize max brightness to 255
                self.prev_max = max(levels,1)
                self.time_since_thunder = 0
                
            else: 
            	#no thunder
                self.intensity = 0
                self.time_since_thunder = self.time_since_thunder + 1
                
            if (self.old_intensity!=0):
                # some basic low pass filtering for persistence
                self.intensity = min(self.intensity, int(self.old_intensity * exp(-ctime/tc)))
        
        
                
        #update the noise buffer indices to the next value
        self.noiseindex = (self.noiseindex+1) % self.noisebuflen
        self.index_since_init = self.index_since_init + 1
        
        if self.index_since_init < self.noisebuflen:
        	self.noisebuf[self.noiseindex] = levels
        	self.noisebuf[self.noiseindex] = mean(self.noisebuf[0:self.noiseindex+1])
        else:
        	#put a new value in the next noise buffer index bin
        	self.noisebuf[self.noiseindex] = levels
        	self.noisebuf[self.noiseindex] = mean(self.noisebuf)

        self.old_intensity = self.intensity
        return self.intensity

    def setindex(self):
        self.ledindex = int(random.uniform(0, 256)) #this is correct because uniform uses the open interval not the closed
