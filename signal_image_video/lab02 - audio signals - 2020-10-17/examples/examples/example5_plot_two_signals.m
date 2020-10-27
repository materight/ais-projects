% WARNING!
% Communications Toolbox required
% Signal Processing Toolbox required for sawtooth function (replace with a
% sin if you don't want to install it

t = [0:.01:4*pi];
% A sawtooth signal
x = sawtooth(2*t); 

u = [0:.01:4*pi];
% A sin signal
y = sin(u); 

% Plot the two signals
plot(t,x, '--', u, y, ':')
% Add a legend, in north outside
legend('Sawtooth','Sin','Location','NorthOutside');



