
% %%%% Fundamentals of Image and Video Processing %%%%
%      
%       Compass operators
%       Last change
%       Jan 2020

I=imread('cameraman.jpg');
subplot (3,3,1);imshow(I,[]);
s = 250;
% Compass Operators
NW = [  1  1  0 ;  
        1  0 -1 ;  
        0 -1 -1 ] ;  


SW = [  0 -1 -1 ;  1  0 -1 ;  1  1  0 ] ;   
SE = [ -1 -1  0 ; -1  0  1 ;  0  1  1 ] ;   
NE = [  0  1  1 ; -1  0  1 ; -1 -1  0 ] ;   
N  = [  1  1  1 ;  0  0  0 ; -1 -1 -1 ] ;   
S  = [ -1 -1 -1 ;  0  0  0 ;  1  1  1 ] ; 
W  = [  1  0 -1 ;  1  0 -1 ;  1  0 -1 ] ;   
E  = [ -1  0  1 ; -1  0  1 ; -1  0  1 ] ;

subplot (3,3,2); imshow(filter2(N , I)>s); title(' N ');
subplot (3,3,3); imshow(filter2(S , I)>s); title(' S ');
subplot (3,3,4); imshow(filter2(E , I)>s); title(' E ');
subplot (3,3,5); imshow(filter2(W , I)>s); title(' W ');
subplot (3,3,6); imshow(filter2(NW, I)>s); title(' NW');
subplot (3,3,7); imshow(filter2(SW, I)>s); title(' SW');
subplot (3,3,8); imshow(filter2(SE, I)>s); title(' SE');
subplot (3,3,9); imshow(filter2(NE, I)>s); title(' NE');

% Ex1: modify the threshold "s"
% Ex2: Try to extract the maximum of each Image and apply a threshold.
% Compare with the other methods.
% Remember that
% C = max(A,[],dim) 
% returns the largest elements along the dimension of A specified by scalar dim. 
% For example, max(A,[],1) produces the maximum values 
% along the first dimension (the rows) of A.















