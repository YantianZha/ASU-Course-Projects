close all;
%Create a 128-point real data sequence consisting of unit-amplitude 
%sinusoids at 5 Hz, 15 Hz, and 16 Hz. Let the sampling frequency fs = 64 
%samples/second.
T = 0:1/64:2-(1/64);
data1 = sin(2*pi*5*T)+sin(2*pi*15*T)+sin(2*pi*16*T);
wn = awgn(data1,0);
data2 = data1 + wn;
% plot(T,data_a,T,wn)
% plot(T,data_b) 

fs = 64
D = 32; % length of each segment
S1 = 10; % shift 
S2 = 20;

total_len = size(data2, 2);

nfft = 4096;
window = hamming(D);

% divide data
num_seg = floor((size(T,2)-D)/(D-S1)+1);
% for data1 shift = 10 (S1)
for i = 1:num_seg
    seg(i,:) = data1((i-1)*(D-S1)+1:(i-1)*(D-S1)+D);
    seg_d1_s1(i,:) = seg(i,:);
end
% for data1 shift = 20 (S2)
for i = 1:num_seg
    seg(i,:) = data1((i-1)*(D-S2)+1:(i-1)*(D-S2)+D);
    seg_d1_s2(i,:) = seg(i,:);
end
% for data2 shift = 10 (S1)
for i = 1:num_seg
    seg(i,:) = data2((i-1)*(D-S1)+1:(i-1)*(D-S1)+D);
    seg_d2_s1(i,:) = seg(i,:);
end
% for data2 shift = 20 (S2)
for i = 1:num_seg
    seg(i,:) = data2((i-1)*(D-S2)+1:(i-1)*(D-S2)+D);
    seg_d2_s2(i,:) = seg(i,:).*window';
end

%window_2 = window .* window;

% average energy of window data1
U = sum(window)/D;
% average energy of window data2
U = sum(window)/size(data2, 2);


S_w_d1s1 = zeros(1,4096);
S_w_d1s2 = zeros(1,4096);
S_w_d2s1 = zeros(1,4096);
S_w_d2s2 = zeros(1,4096);
%S_w_d1s1_0 = zeros(1,4096);
for k = -nfft/2:(nfft/2-1)
        w = k*2*pi/4096;
        f_data(k+nfft/2+1) = [w*fs/(2*pi)];
end

for i = 1:num_seg

% calculate frequency
    x_w_d1s1 = seg_d1_s1(i,:).*window';
    x_w_d1s2 = seg_d1_s2(i,:).*window';
    x_w_d2s1 = seg_d2_s1(i,:).*window';
    x_w_d2s2 = seg_d2_s2(i,:).*window';
    S_w_d1s1_u = abs(fftshift(fft(x_w_d1s1,4096))); 
    S_w_d1s2_u = abs(fftshift(fft(x_w_d1s2,4096))); 
    S_w_d2s1_u = abs(fftshift(fft(x_w_d2s1,4096))); 
    S_w_d2s2_u = abs(fftshift(fft(x_w_d2s2,4096))); 
    S_w_d1s1 = S_w_d1s1 + abs(S_w_d1s1_u);
    S_w_d1s2 = S_w_d1s2 + abs(S_w_d1s2_u);
    S_w_d2s1 = S_w_d2s1 + abs(S_w_d2s1_u);
    S_w_d2s2 = S_w_d2s2 + abs(S_w_d2s2_u);
end 

% testing with plots
figure(1)
plot(f_data, 10*log(S_w_d1s1));
grid on;
title('Welch PSD estimate with dataset 1 shift 10');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');
figure(2)
plot(f_data, 10*log(S_w_d1s2));
grid on;
title('Welch PSD estimate with dataset 1 shift 20');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');
figure(3)
plot(f_data, 10*log(S_w_d2s1));
grid on;
title('Welch PSD estimate with dataset 2 shift 10');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');
figure(4)
plot(f_data, 10*log(S_w_d2s2));
grid on;
title('Welch PSD estimate with dataset 2 shift 20');
xlabel('Frequency(Hz)');
ylabel('PSD estimates as Power(dB)');


    


