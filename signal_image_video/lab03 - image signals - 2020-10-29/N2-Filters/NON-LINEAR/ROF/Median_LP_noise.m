
% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Median filters and noise
%       Last change
%       Jan 2020


clear;
im=imread('cupola_adjusted.jpg');
% J = IMNOISE(I,TYPE,...) Add noise of a given TYPE to the intensity image I.
f=imnoise(im, 'salt & pepper', 0.2);
figure(1);imshow(f);title('Original');

% LPF 3x3
L1(1:3,1:3)=1/9;
f33=conv2(f,L1,'same');
figure(2); imshow(uint8(f33)); title('Mobile average 3x3');

% Median 3x3 
f33=medfilt2(double(f),[3 3]);
figure(3); imshow(uint8(f33)); title('Median 3x3');

% LPF 5x5
L1(1:5,1:5)=1/25;
f55=conv2(f,L1,'same');
figure(4); imshow(uint8(f55)); title('Mobile average 5X5');

% Median 5x5 
f55=medfilt2(double(f),[5 5]);
figure(5); imshow(uint8(f55)); title('Median 5x5');


