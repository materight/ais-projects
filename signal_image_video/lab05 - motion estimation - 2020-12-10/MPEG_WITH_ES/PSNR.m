% %%%% Laboratorio di Elaborazione e Trasmissione delle Immagini %%%%
%      
%      PSNR
%      
%      A: prima immagine
%      B: seconda immagine
%      3-19 maggio 2004
%      Revisioni:
%      09/05/2005


function p = PSNR(A, B)
E=0;
E = A - B;
% E = E.^2;
% mse = (mean2(E))^0.5;
% p=20*log10(255^2/mse);
p = 20*log10(255/(sqrt(mean2(E.^2))));