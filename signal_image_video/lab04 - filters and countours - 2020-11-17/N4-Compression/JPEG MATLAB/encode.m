%Run-Length of quantized DCT
%
% note : Out=encode(IN);
%
%   dove "IN"   row matrix with quantized coefficients from zig-zag scan
%   dove "Out"  row matrix with run-length. The first two components are the
%               dimension of the input matrix "IN"
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function [huff, rle]=encode(run);

DC=0;
Nblocchi=size(run, 2)/64;
I=run(1:64);
[Y, X, DC]=rlejpg(I, DC);
for i=2:Nblocchi
    I=run((((i-1)*64)+1):(i*64));
    [huff, I, DC]=rlejpg(I, DC); 
    
    X=strcat(X, I);
    Y=strcat(Y, huff);
end

rle=X;
huff=Y;