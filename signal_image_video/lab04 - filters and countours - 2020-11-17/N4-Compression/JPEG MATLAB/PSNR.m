%      PSNR
%      
%      A: first image
%      B: second image


function p = PSNR(A, B)
E=0;
E = A - B;
% E = E.^2;
% mse = (mean2(E))^0.5;
% p=20*log10(255^2/mse);
p = 20*log10(255/(sqrt(mean2(E.^2))));