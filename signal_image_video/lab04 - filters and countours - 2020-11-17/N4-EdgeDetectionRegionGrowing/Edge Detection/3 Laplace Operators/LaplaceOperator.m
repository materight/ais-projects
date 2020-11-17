% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Laplace operators
%       Last change
%       Jan 2020

I=rgb2gray(imread('Wrights_walking.jpg'));
s=170;

L1 = [  0 -1  0
       -1  4 -1
        0 -1  0 ];

L2 = [ -1 -1 -1
       -1  8 -1
       -1 -1 -1];

L3 = [  1 -2  1
       -2  4 -2
        1 -2  1];



figure; imshow(I); title('original image');
figure; imshow(filter2(L2, I),[]); title('filtered image');
figure; imshow(filter2(L2, I)>s);  title('threshold');
figure; imshow(abs(filter2(L2, I))>s);  title('Absolute value after thresholding');


% Automatic edge extraction
figure; imshow(edge(I,'log'));









