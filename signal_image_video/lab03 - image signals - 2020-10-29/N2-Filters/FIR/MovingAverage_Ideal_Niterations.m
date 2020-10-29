% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Moving Average
%       Last change
%       Jan 2020


clear all;
close all;
clc;

% Load the image and show the original
p = imread('baboon.pgm');
figure;imshow(p); title('Original Image');

% LPF 7x7
L(1:7,1:7) = 1/49

% Filtro a media mobile 7X7
p1=conv2(double(p),L,'same');
figure; imshow(uint8(p1)); 
title('Filtered image - iteration 1');

% Filtro a media mobile 7X7
p2=conv2(double(p1),L,'same');
figure; imshow(uint8(p2)); 
title('Filtered image - iteration 2');

% Filtro a media mobile 7X7
p3=conv2(double(p2),L,'same');
figure; imshow(uint8(p3)); 
title('Filtered image - iteration 3');

% Filtro a media mobile 7X7
p4=conv2(double(p3),L,'same');
figure; imshow(uint8(p4)); 
title('Filtered image - iteration 4');
