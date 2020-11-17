%zig-zag decoding
%
% note: Out=decodezz_a(IN,M,N);
% 
%   where "IN"  row matrix with coefficients
%   dove "Out" matrix with quantized coefficients
%   dove  "M"  number of rows
%   dove  "N"  number of columns
%
function Out=decodezz_a(IN, M, N);
Mat=[];
Mat=blkproc(IN,[1 64],'zigzaginv(x)');
% for j=1:64:M*N
% 
%     Mat(j:j+63)=zigzaginv(IN(j:j+63));
% end

%Out=Mat;
Out=zeros(M,N);
% for k=1:1:M
%     Out(k,:)=Mat(1+N*(k-1):1+N*(k-1)+N-1);
% end

k=0;
h=0;
S=M/8;
for i=1:S
   A=Mat(1:8,k+1:k+N);
   k=k+N;
   Out(i+h:i+h+7,1:N)=A;
   h=h+7;
end