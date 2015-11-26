%Create a 128-point real data sequence consisting of unit-amplitude 
%sinusoids at 5 Hz, 15 Hz, and 16 Hz. Let the sampling frequency fs = 64 
%samples/second.
T = 0:1/64:2-(1/64);
fs = 64;
lag1 = 10;
lag2 = 20;
data1 = sin(2*pi*5*T)+sin(2*pi*15*T)+sin(2*pi*16*T);
data2 = data1 + awgn(data1,0);  % add white noise
nfft = 4096;
window = hamming(nfft); 

cov_ele = zeros(1*1);
% for data1 shift = 10 (S1)
for TC = 1:lag1;
    for n = 1:size(T,2)-TC
        cov_ele(n) = data1(n)*data1(n+TC);
    end
    r_tc_Lag1D1(TC) = sum(cov_ele)/(size(T,2) - TC);
end
% for data1 shift = 20 (S2)
for TC = 1:lag2;
    for n = 1:size(T,2)-TC
        cov_ele(n) = data1(n)*data1(n+TC);
    end
    r_tc_Lag2D1(TC) = sum(cov_ele)/(size(T,2) - TC);
end
% for data2 shift = 10 (S1)
for TC = 1:lag1;
    for n = 1:size(T,2)-TC
        cov_ele(n) = data2(n)*data2(n+TC);
    end
    r_tc_Lag1D2(TC) = sum(cov_ele)/(size(T,2) - TC);
end
% for data2 shift = 20 (S2)
for TC = 1:lag2;
    for n = 1:size(T,2)-TC
        cov_ele(n) = data2(n)*data2(n+TC);
    end
    r_tc_Lag2D2(TC) = sum(cov_ele)/(size(T,2) - TC);
end

% calculate frequency
for k = -nfft/2:(nfft/2-1)
    w = k*2*pi/4096;
    f_data(k+nfft/2+1) = [w*fs/(2*pi)];
end

fft_rLag1D1 = fft(r_tc_Lag1D1, 2048);
fft_rLag2D1 = fft(r_tc_Lag2D1, 2048);
fft_rLag1D2 = fft(r_tc_Lag1D2, 2048);
fft_rLag2D2 = fft(r_tc_Lag2D2, 2048);

% Create Hamming window
window_L1 = hamming(2*lag1-1);
window_L2 = hamming(2*lag2-1);

% Create fft(hamming)
fft_w_L1 = fft(window_L1, 2049);
fft_w_L2 = fft(window_L2, 2049);

% Convolution of fft_w with fft_r
est_Lag1D1 = abs(conv(fft_rLag1D1, fft_w_L1));
est_Lag2D1 = abs(conv(fft_rLag2D1, fft_w_L2));
est_Lag1D2 = abs(conv(fft_rLag1D2, fft_w_L1));
est_Lag2D2 = abs(conv(fft_rLag2D2, fft_w_L2));

%abs_est_Lag1D1 = abs(conv(fft_rlag1, fft_w));

figure(1)
plot(f_data, 20*log(est_Lag1D1));
grid on;
title('Blackman-Tukey PSD estimates (Lag = 10 for data set 1)');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');

figure(2)
plot(f_data, 20*log(est_Lag2D1));
grid on;
title('Blackman-Tukey PSD estimates (Lag = 20 for data set 1)');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');

figure(3)
plot(f_data, 20*log(est_Lag1D2));
grid on;
title('Blackman-Tukey PSD estimates (Lag = 10 for data set 2)');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');

figure(4)
plot(f_data, 20*log(est_Lag2D2));
grid on;
title('Blackman-Tukey PSD estimates (Lag = 20 for data set 2)');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');


