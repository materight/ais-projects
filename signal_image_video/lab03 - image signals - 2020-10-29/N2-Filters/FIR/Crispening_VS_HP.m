% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       High pass vs Crispening
%       Last change
%       Jan 2020

clear all;
close all;
clc;

% Load the image
p = imread('baboon.pgm');

% HPF 3x3, sum of coefficient 0
L=[-1 -1 -1; -1 8 -1; -1 -1 -1];

% HPF image
pHP=conv2(p,L,'same');
figure; imshow(uint8(pHP)); 
title('Image filtered by HP');

% Crispening filter, sum of coefficient 1
Crisp=[-1 -1 -1; -1 9 -1; -1 -1 -1];

% Mobile mean filter 7X7
pCrisp=conv2(p,Crisp,'same');
figure; imshow(uint8(pCrisp)); 
title('Image filtered by Crispening');
