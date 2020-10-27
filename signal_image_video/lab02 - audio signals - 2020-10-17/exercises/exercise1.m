% WARNING!
% Communications Toolbox required
% Signal Processing Toolbox required for sawtooth function (replace with a
% sin if you don't want to install it

predictor = [0 1]; % y(k)=x(k-1)
% partition is a row vector, from -1 to .9, with a step of .1
partition = [-1:.1:.9];
% codebook is a row vector, from -1 to 1, with a step of .1 
% its length exceeds the length of partition by one
codebook = [-1:.1:1];
% t is a row vector, from 0 to 2*pi, with a step of pi/50
t = [0:pi/50:2*pi];
% A sawtooth signal
x = sawtooth(3*t); % Original signal


% Quantize x using DPCM
% 
% partition is a vector whose entries give the endpoints of the
% partition intervals; its entries are in strictly ascending order. 
%
% codebook tells the quantizer which common value to assign to inputs
% that fall into each range of the partition
% The first element of codebook is the value for the interval 
% between negative infinity and the first element of P
%
% predictor specifies the predictive transfer function.
encodedx = dpcmenco(x,codebook,partition,predictor);

% Try to recover x from the modulated signal
decodedx = dpcmdeco(encodedx,codebook,predictor);

% Plot the sawtooth signal and the decoded signal
plot(t,x, t,decodedx,'--')
% Add a legend, in north outside
legend('Original signal','Decoded signal','Location','NorthOutside');

% Mean square error
distor = sum((x-decodedx).^2)/length(x)

