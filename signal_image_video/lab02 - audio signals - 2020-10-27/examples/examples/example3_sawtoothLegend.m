% WARNING!
% Communications Toolbox required
% Signal Processing Toolbox required for sawtooth function (replace with a
% sin if you don't want to install it

t = [0:.1:2*pi];
% A sawtooth signal
x = sawtooth(2*t); 

% Plot the sawtooth signal and the decoded signal
plot(t,x, '--')
% Add a legend, in north outside
legend('Sawtooth','Location','NorthOutside');

