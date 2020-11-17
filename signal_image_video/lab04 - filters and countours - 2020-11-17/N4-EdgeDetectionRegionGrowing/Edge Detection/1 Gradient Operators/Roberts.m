
% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Roberts filter
%       Last change
%       Jan 2020

I=rgb2gray(imread('Wrights_walking.jpg'));
figure;imshow(I);

rx = [ 1  0
       0 -1 ];
ry = [ 0  1
      -1  0 ];

% Y = FILTER2(B,X) filters the data in X with the 2-D FIR
% filter in the matrix B.  The result, Y, is computed 
% using 2-D correlation and is the same size as X. 
Ix=filter2(rx, I);
Iy=filter2(ry, I);
% Magnitudine
I_out=abs(Ix)+abs(Iy);
figure; imshow(abs(Ix),[]); title('x component');
figure; imshow(abs(Iy),[]); title('y component');
figure; imshow(I_out,[]); title('filtered image');
figure; imshow(I_out>60); title('threshold')

truesize;

%Ex: change the threshold and evaluate the result