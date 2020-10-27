function [t, newm]= mydownsample (M, N, factor)
% Downsample function
% created by MMLAb
% instruction
% subsample (M, N, factor)
% M and N are matrix dimensions
% factor is the downsampling factor
% the function mydownsample gives a matrix with M/factor, N/factor dimensions 
% 

% check that the dimensions of the image are multiple of factor
if rem(M,factor)~=0 | rem(N,factor)~=0
    disp('factor is not ok with matrix dimensions');
    return;
end

% to check processing time I can use tic/toc or clock/etime
t=0;
tic; % timer started

matrix= 20*rand(M,N); %random matrix MxN
newm=[]; % matrix to save result
% block processing of the image 
for h=1:factor:M
    for k=1:factor:N
        newm(ceil(h/factor),ceil(k/factor))= mean_calculus(matrix(h:h+factor-1, k:k+factor-1));
    end
end
t=toc*1000; % in t you find the execution time
