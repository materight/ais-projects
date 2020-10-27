% WARNING!
% Communications Toolbox required
% Signal Processing Toolbox required for sawtooth function (replace with a
% sin if you don't want to install it

% t is a row vector, from 0 to 2*pi, with a step of pi/50
t = [0:pi/50:2*pi];
% A sawtooth signal
x = sawtooth(3*t);
% initcodebook is a row vector, from -1 to 1, with a step of .1 
initcodebook = [-1:.1:1];

% Optimize differential pulse code parameters, using initial codebook and order 1.
[predictor,codebook,partition] = dpcmopt(x,1,initcodebook);

% Quantize x using DPCM
% 
% codebook prescribes a value for each partition in the quantization
% The first element of Quantization codebook is the value for the interval 
% between negative infinity and the first element of P
% The second output signal from this block contains the quantization 
% of the input signal based on the quantization indices and prescribed values.
%
% partition is a vector whose entries give the endpoints of the partition intervals
% its entries are in strictly ascending order. 
%
% predictor specifies the predictive transfer function.
encodedx = dpcmenco(x,codebook,partition,predictor);

% Try to recover x from the modulated signal.
decodedx = dpcmdeco(encodedx,codebook,predictor);

% Plot the sawtooth signal and the decoded signal
plot(t,x, t,decodedx,'--')
% Add a legend, in north outside
legend('Original signal','Decoded signal','Location','NorthOutside');

% Mean square error
distor = sum((x-decodedx).^2)/length(x)