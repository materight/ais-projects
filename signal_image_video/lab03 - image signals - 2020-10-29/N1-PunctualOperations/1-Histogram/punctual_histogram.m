% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Histogram and punctual operations
%       Negative, Stretching, Contrast
%       Last change
%       Jan 2020

close all;
clear all;
clc;

% 1: Visualization of the image histogram
f = imread('cupola.jpg'); 
f = ind2gray(f,gray(256)); % The human eye can see just 50 shades of a color
    
figure; imshow(f); title('Original image cupola.jpg');
figure; imhist(f); title('Histogram of cupola.jpg');
     
% 2: Negative
    
neg = imadjust(f,[0 1],[1 0]); % Map the values from [0, 1] to [1, 0]

figure; imshow(neg); title('Negative of cupola.jpg');
figure; imhist(neg); title('Histogram of the negative of cupola.jpg');

 
% 3: Histogram stretching    
f1=imadjust(f,[min(min(f))/255 max(max(f))/255],[0 1]); % Select the histogram from min to max (bit values) and map it over [0, 1]
figure; imshow(f1); title('Modified Image (histogram streched)');
figure; imhist(f1); title('Histogram of the modified image (stretching histogram)');

% 4: Selective contrast
% J = IMADJUST(I,[LOW_IN; HIGH_IN],[LOW_OUT; HIGH_OUT]) maps the values
%    in intensity image I to new values in J such that values between LOW_IN
%    and HIGH_IN map to values between LOW_OUT and HIGH_OUT. Values below
%    LOW_IN and above HIGH_IN are clipped; that is, values below LOW_IN map
%    to LOW_OUT, and those above HIGH_IN map to HIGH_OUT. You can use an
%    empty matrix ([]) for [LOW_IN; HIGH_IN] or for [LOW_OUT; HIGH_OUT] to
%    specify the default of [0 1]. If you omit the argument, [LOW_OUT;
%    HIGH_OUT] defaults to [0 1].
tmp1=imadjust(f,[0 .4],[0 .1]);  % clipping above 0.4 to 0.1
tmp2=imadjust(f,[.4 .7],[0 .8]); % clipping under 0.3 to 0 and above 0.7 to 0.8
tmp3=imadjust(f,[0.7 1],[0 .1]); % clipping under 0.7 to 0
f2 = tmp1+tmp2+tmp3;
figure; imshow(f2); title('Modified image (selective contrast)');
figure; imhist(f2); title('Histogram of the modified image (selective contrast)');
