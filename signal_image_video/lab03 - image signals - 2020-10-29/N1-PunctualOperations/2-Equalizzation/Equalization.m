% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Equalization
%       Last change
%       Jan 2020

% Closing all
clear all;
close all;
clc;


% Loading the image and converting to grayscale (if necessary)
f = imread('cupola.jpg'); 
f = ind2gray(f,gray(256)); 
    
% Draw the histogram and displaying the original Image
figure; imshow(f); title('Original image cupola.jpg');
figure; imhist(f); title('Histogram of cupola.jpg');

% Histogram equalization
f2=histeq(f); 
figure; imshow(f2); title('Equalized image');
figure; imhist(f2); title('Histogram of equalized image');