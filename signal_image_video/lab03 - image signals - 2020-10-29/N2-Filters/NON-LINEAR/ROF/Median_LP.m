
% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Median filters
%       Last change
%       Jan 2020


f = imread('micro.jpg'); 
figure(1); 
imshow(f);
title('Original image');
    
% Histogram Equalization
f=histeq(f); 
figure(2); imshow(uint8(f)); title('Equalized image');
figure(3); imhist(uint8(f)); title('Histogram of equalized image');


% Median Filter 3x3
%    Median filtering of the matrix
%    A in two dimensions. Each output pixel contains the median
%    value in the M-by-N neighborhood around the corresponding
%    pixel in the input image. MEDFILT2 pads the image with zeros
%    on the edges, so the median values for the points within 
%    [M N]/2 of the edges may appear distorted.
fm33=medfilt2(double(f),[3 3]);
figure(4); imshow(uint8(fm33)); title('Median filter 3X3');
figure(5); imhist(uint8(fm33)); title('Histogram of median filter 3X3');


% LPF 3x3
L2(1:3,1:3)=1/9;
f33=conv2(double(f),L2,'same');
figure(6); imshow(uint8(f33)); title('Mobile average filter 3X3');
figure(7); imhist(uint8(f33)); title('Histogram of mobile average 3X3');



% Median filter 7X7 
fm77=medfilt2(double(f),[7 7]);
figure(8); imshow(uint8(fm77)); title('Median filter 7x7');
%figure(9); imhist(uint8(fm77)); title('Histogram of mobile average 7x7');

% LPF 7X7
L2(1:7,1:7)=1/49;
f77=conv2(f,L2,'same');
figure(10); imshow(uint8(f77)); title('Mobile average filter 7x7');
%figure(11); imhist(uint8(f77)); title('Histogram of mobile average 7x7');

