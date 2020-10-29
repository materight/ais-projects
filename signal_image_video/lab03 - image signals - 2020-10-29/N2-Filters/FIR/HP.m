% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       High pass filtes
%       Last change
%       Jan 2020


clear all;
close all;
clc;

% Load the image
p = double(imread('baboon.pgm'));

% Prepare LPF filter
L(1:25,1:25) = 1/625;

% Show the original one
subplot(1,3,1); % Create a matrix of plots, next image inserted in position 1
imshow(uint8(p));
title('Original Image');

% Obtain a LPF image with 25x25
p2525=conv2(p,L,'same');
subplot(1,3,2); 
imshow(uint8(p2525)); 
title('LPF 25x25');

% HPF, as 1-LPF 
subplot(1,3,3);
imshow(uint8(p-p2525),[]); 
title('HP');

% Trying to display images as big as possible
truesize;