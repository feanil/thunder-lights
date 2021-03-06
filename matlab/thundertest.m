clear all
close all
set(0,'defaultAxesFontSize',7)
chunk = 4096;
cutoff=4000;
nfilterbins = floor(cutoff/(1/(chunk/44100)));
noiselevels=1;
thunderlevel=17;
postthunder = 3;
thunderalpha=-0.05;
[m, Fs] = audioread('../../personal/thunder.mp3',[1 44100*180]);


for ii = 1:(floor(length(m)/chunk)-1)
    freqL(:,ii) = fft(m((chunk*ii):(chunk*(ii+1)),1));
    freqR(:,ii) = fft(m((chunk*ii):(chunk*(ii+1)),2));
    %    chunkavg(ii) = mean(sum(abs(m((chunk*ii):(chunk*(ii+1)),:))));
    testL(ii) = mean(abs([freqL(1:nfilterbins,ii).' freqL((end-nfilterbins+1):end,ii).']));
    testR(ii) = mean(abs([freqR(1:nfilterbins,ii).' freqR((end-nfilterbins+1):end,ii).']));
    freqL(:,ii)=fftshift(freqL(:,ii));
    freqR(:,ii) =fftshift(freqR(:,ii));
    var=(testL(ii)+testR(ii))/2;
    if ii>1&& var>thunderlevel*noiselevels(ii-1)
        thunder(ii)=1;
    elseif ii>1 &&thunder(ii-1)>=0 && var>postthunder*noiselevels(ii-1)
        thunder(ii) = thunder(ii-1)*exp(thunderalpha);
    else
        thunder(ii)=0;
    end
    
    if ii==1
        noiselevels(ii)=var;
    else
        noiselevels(ii) = mean([noiselevels(1:(ii-1)) var]);
    end
end

chunktime = chunk/Fs;
figure;
imagesc((1:size(freqL,2))*chunk/Fs, ((1:size(freqL,2))-chunk/2), 20*log10(abs(freqL)))
colorbar
set(gca, 'CLim', [-30 50])
title(sprintf('Frequency content vs. time, chunk size = %.0f (channel 1)',chunk))
figure;
imagesc((1:size(freqL,2))*chunk/Fs, ((1:size(freqL,2))-chunk/2),20*log10(abs(freqR)))
colorbar
set(gca, 'CLim', [-30 50])
title(sprintf('Frequency content vs. time, chunk size = %.0f (channel 2)',chunk))

% figure;
% plot((1:size(freqL,2))*chunk/Fs,20*log10(mean(abs(freqL)+abs(freqR),1)))
% xlabel('Time (s)')
% ylabel('Average total signal power (dB)')
% ylim([-20 20])
% title(sprintf('Signal power vs. time, chunk size = %.0f',chunk))
% 
% 
% figure;
% plot((1:size(freqL,2))*chunk/Fs,20*log10(chunkavg))
% xlabel('Time (s)')
% ylabel('Average total signal power (dB)')
% title(sprintf('Signal power vs. time, chunk size = %.0f',chunk))
% 

figure;
plot((1:size(freqL,2))*chunk/Fs, 20*log10(testL), (1:size(freqL,2))*chunk/Fs, 20*log10(testR))
xlabel('Time (s)')
ylabel('Average signal level below cutoff freq (dB)')
title(sprintf('Signal level below cutoff freq vs. time, cutoff = %.0f',cutoff))

figure;
plot(1:length(noiselevels), 20*log10(noiselevels))

figure
plot(1:length(thunder), thunder)
% figure;
% plot((1:size(m))/Fs, 20*log10(abs(m(:,1)+m(:,2))))
% xlabel('Time (s)')
% ylabel('Signal power (dB) - no chunk averaging')