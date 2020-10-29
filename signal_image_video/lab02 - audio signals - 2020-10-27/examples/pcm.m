% WARNING!
% Communications Toolbox required


% General clear
clc;
close all;
clear all;

% Requires the n-bit and number of samples in a period
n=input('Enter n value for n-bit PCM system :  ');
n1=input('Enter number of samples in a period : ');
L=2^n;

% =================
% The message
% =================

% Analog message signal --> 8*sin(x)
% From 0 to 4*pi
x=0:2*pi/n1:4*pi;
signal=8*sin(x);

% =================
% Quantization Process
% =================

% Scalar quantization is a process that maps all inputs
% within a specified range to a common value.
%
% Two parameters determine a quantization: a partition and a codebook.
% A quantization partition defines several contiguous,
% nonoverlapping ranges of values within the set of real numbers.
% To specify a partition in the MATLAB® environment,
% list the distinct endpoints of the different ranges in a vector.
%
% For example, if the partition separates the real number line into the four sets
%
%   {x: x ? 0}
%   {x: 0< x ? 1}
%   {x: 1 < x ? 3}
%   {x: 3 < x}
% then you can represent the partition as the three-element vector
% partition = [0,1,3];
% Length of the partition vector is one less than the number of partition intervals.
%
% A codebook tells the quantizer which common value to assign to inputs
% that fall into each range of the partition.
% Represent a codebook as a vector whose length is the same
% as the number of partition intervals. For example, the vector
% codebook = [-1, 0.5, 2, 3];
% is one possible codebook for the partition [0,1,3].

%  Sin max value = 1 --> vmax=8
vmax=8;
vmin=-vmax;
delta=(vmax-vmin)/L;
% level are between vmin and vmax with difference of delta
partition=vmin:delta:vmax;
% Quantized values 
codebook=vmin-(delta/2):delta:vmax+(delta/2); 
% Produce quantization index of the signal and quantized output value
%
% ind contain index number and quants contain quantized  values
% quants is a row vector whose length is the same as the length of sig.
[ind,quants]=quantiz(signal,partition,codebook);
                                                                      
lengthInd=length(ind);
lenghtQuants=length(quants);
% To make index as binary decimal, from 0 to N-1
for i=1:lengthInd
    if(ind(i)~=0)                   
        ind(i)=ind(i)-1;
    end 
	i=i+1;
end   
% To make quantize value inbetween the levels
for i=1:lenghtQuants
	if(quants(i)==vmin-(delta/2))	
        quants(i)=vmin+(delta/2);
    end
end    

% =================
% Encoding Process
% =================

% Convert the decimal to binary
% The most significant digit is the leftmost element
binaryCode=de2bi(ind,'left-msb');             

% convert code matrix to a coded row vector
k=1;
for i=1:lengthInd
	for j=1:n
        pcmEncoded(k)=binaryCode(i,j);                  
        j=j+1;
        k=k+1;
    end
	i=i+1;
end


% =================
% Decoding Process
% =================

% Reshape the pcmEncoded array in a matrix; each column is a sample
received=reshape(pcmEncoded,n,length(pcmEncoded)/n);
% Getback the index in decimal form
index=bi2de(received','left-msb');

% getback Quantized values
quants=delta*index+vmin+(delta/2);                       



% =================
% Plot
% =================
subplot(3,1,1);
plot(signal);
% The legend
legend('Analog Signal');
% A grid
grid;
% X and Y labels
ylabel('Amplitude--->');
xlabel('Time--->');

% Plot discrete sequence data
subplot(3,1,2);
stem(signal);
grid on;
legend('Sampled Signal');
ylabel('Amplitude--->');
xlabel('Time--->');

% Plot the Quantize values
subplot(3,1,3);
stem(quants);
grid on;	
legend('Quantized Signal');
ylabel('Amplitude--->');
xlabel('Time--->');


% A new Figure
figure
% Plot Encoded signal
subplot(2,1,1);
grid on;
% Stairstep graph
stairs(pcmEncoded);                                
% Display the encoded signal
axis([0 300 -0.1 1.1]);
legend('Encoded Signal', 'Location','NorthOutside');
ylabel('Amplitude--->');
xlabel('Time--->');

% Plot Decoded signal
subplot(2,1,2);
grid on;
% Plot Demodulated signal
plot(quants);                                                        
legend('Demodulated Signal', 'Location','NorthOutside');
ylabel('Amplitude--->');
xlabel('Time--->');
