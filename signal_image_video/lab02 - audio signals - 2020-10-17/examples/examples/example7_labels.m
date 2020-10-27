t = [0:.01:4*pi];
% A sin signal
x = sin(t); 

% Plot the sin signal
plot(t,x, '--')
% Add a legend, in north outside
legend('Sin','Location','NorthOutside');

grid();
ylabel('Amplitude--->');
xlabel('Time--->');

