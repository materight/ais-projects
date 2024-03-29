
% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       LP filters
%       Last change
%       Jan 2020

clear all;
close all;
clc;

% Load the image and show the original
p = imread('baboon.pgm');
figure;imshow(p); title('Original image');

% LPF 7x7
L(1:7,1:7) = 1/49; % Average window

% Mobile average filter 7X7
% C = CONV2(A, B) performs the 2-D convolution of matrices A and B.
% C = CONV2(..., SHAPE) returns a subsection of the 2-D
%    convolution with size specified by SHAPE:
%      'same'  - returns the central part of the convolution
%                that is the same size as A.
p77=conv2(double(p),L,'same');
figure; imshow(uint8(p77)); % Convert the doubles in int and show the image
title('Filtered image with a moving average 7x7');

% simil-gaussian
M=[0 0 1 2 1 0 0; 0 1 2 3 2 1 0 ; 1 2 3 4 3 2 1 ; 2 3 4 100 4 3 2 ; 1 2 3 4 3 2 1 ; 0 1 2 3 2 1 0; 0 0 1 2 1 0 0];
G=M/max(max(M));

q77=conv2(double(p),G,'same');
figure; imshow(uint8(q77)); 
title('Image filtered by the gaussian filter 7x7');



% impulsive gaussian mask
% This is a sample matrix, produced by sampling the Gaussian filter kernel (with ?? = 0.84089642) 
% at the midpoints of each pixel and then normalizing. Note that the center element (at [0, 0]) 
% has the largest value, decreasing symmetrically as distance from the center increases.
% Note that 0.22508352 (the central one) is 1177 times larger than 0.00019117 which is just outside 3??.

n1=[0.00000067 	0.00002292 	0.00019117 	0.00038771 	0.00019117 	0.00002292 	0.00000067];
n2=[0.00002292 	0.00078633 	0.00655965 	0.01330373 	0.00655965 	0.00078633 	0.00002292];
n3=[0.00019117 	0.00655965 	0.05472157 	0.11098164 	0.05472157 	0.00655965 	0.00019117];
n4=[0.00038771 	0.01330373 	0.11098164 	0.22508352 	0.11098164 	0.01330373 	0.00038771];
n5=[0.00019117 	0.00655965 	0.05472157 	0.11098164 	0.05472157 	0.00655965 	0.00019117];
n6=[0.00002292 	0.00078633 	0.00655965 	0.01330373 	0.00655965 	0.00078633 	0.00002292];
n7=[0.00000067 	0.00002292 	0.00019117 	0.00038771 	0.00019117 	0.00002292 	0.00000067];
% 
N=[n1;n2;n3;n4;n5;n6;n7];
% 
% % Blur filter
r77=conv2(double(p),N,'same');
figure; imshow(uint8(r77)); 
title('Image filtered by a mask 7x7 Gaussian Blur');
