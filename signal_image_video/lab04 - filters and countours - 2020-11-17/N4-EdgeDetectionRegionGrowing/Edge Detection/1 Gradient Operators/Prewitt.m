
% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Prewitt
%       Last change
%       Jan 2020

I=rgb2gray(imread('Wrights_walking.jpg'));
figure;imshow(I);

px = [ -1 -1 -1        
        0  0  0
        1  1  1 ];
py = [ -1  0  1
       -1  0  1
       -1  0  1 ];
% Y = FILTER2(B,X) filters the data in X with the 2-D FIR
% filter in the matrix B.  The result, Y, is computed 
% using 2-D correlation and is the same size as X. 
Ix=filter2(px, I);
Iy=filter2(py, I);
% Magnitudine
I_out=abs(Ix)+abs(Iy);
figure; imshow(abs(Ix), []); title('x component');
figure; imshow(abs(Iy),[]); title('y component');
figure; imshow(I_out,[]); title('filtered image');
figure; imshow(I_out>150); title('threshold');

truesize;

%Ex: change the threshold and evaluate the results