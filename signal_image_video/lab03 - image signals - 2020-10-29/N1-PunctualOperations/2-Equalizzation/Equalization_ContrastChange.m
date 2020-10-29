% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Equalization
%       Last change
%       Jan 2020

clear all;
close all;
clc;

% Show image histogram 
f = imread('cupola.jpg'); 
f = ind2gray(f,gray(256)); 
    
figure; imshow(f); title('Original image cupola.jpg');
figure; imhist(f); title('Histogram of cupola.jpg');

% Histogram equalization
f1=histeq(f); 
figure; imshow(f1); title('Equalized image');
figure; imhist(f1); title('Histogram of equalized image');

% Selective contrast to see a portion of image
f2=imadjust(f1,[0.45 1],[0 1]); 
figure; imshow(f2); title('Image 2');
figure; imhist(f2); title('Histogram of the original image post-adjust');


f3=imadjust(f1,[0 0.5],[0 1]); 
figure; imshow(f3); title('Image 3');
figure; imhist(f3); title('Histogram of the original image post-adjust');
