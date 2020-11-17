% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Sobel
%       Last change
%       Jan 2020

I=rgb2gray(imread('Wrights_walking.jpg'));
sy = [ -1 -2 -1        
        0  0  0
        1  2  1 ];
sx = [ -1  0  1
       -2  0  2
       -1  0  1 ];

Ix=filter2(sx, I);
Iy=filter2(sy, I);

% Magnitudine
If=sqrt(Ix.^2+Iy.^2);

 figure; imshow(abs(Ix),[]); title('x component');
 figure; imshow(abs(Iy),[]); title('y component');
 figure; imshow(If,[]); title('filtered image');
figure; imshow(If>150); title('threshold');

%Ex: change the threshold