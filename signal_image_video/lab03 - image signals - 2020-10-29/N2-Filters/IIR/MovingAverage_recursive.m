close all;
clear all;
clc;

% Load Image
p = imread('baboon.pgm');
subplot(2,2,1);
imshow(p);
title('Original Image');

% Prepare a FILTER (PSF)
L(1:5,1:5) = 1/25;


% Apply  
p55mmr=p;
% For every point of the image (except the last 5 row and 5 columns)
for k=1:size(p55mmr,2)-5 % columns because size(...,2)
    for l=1:size(p55mmr,1)-5 % rows because size(...,1)
        % The center of the filter (l+2,k+2) is equal to the sum of
        % all the 25 points weighted on 25.
        p55mmr(l+2, k+2)=sum(sum((p55mmr(l:l+4, k:k+4)/25)));
    end
end

subplot(2,2,2);
imshow(uint8(p55mmr)); 
title('Image filtered by a recursive moving average 5x5');

% Apply a LPF 5x5 (moving average)
p55=conv2(double(p), L);
subplot(2,2,3);
imshow(uint8(p55)); 
title('Image filtered by a moving average 5x5');


% We left behind the first two row and column (because of the 
% implementation of the filter)
pdiff=uint8(p55(3:514,3:514))-uint8(p55mmr); 
% IMSHOW(I,[LOW HIGH]) displays the grayscale image I, specifying the display
%    range for I in [LOW HIGH]. The value LOW (and any value less than LOW)
%    displays as black, the value HIGH (and any value greater than HIGH) displays
%    as white. Values in between are displayed as intermediate shades of gray,
%    using the default number of gray levels. If you use an empty matrix ([]) for
%    [LOW HIGH], IMSHOW uses [min(I(:)) max(I(:))]; that is, the minimum value in
%    I is displayed as black, and the maximum value is displayed as white.
subplot(2,2,4);
imshow(uint8(pdiff),[]); 
title('difference');

truesize;

% Try to arrange the previous images in an unique image, with all
% the data, in order to compare the figures.
