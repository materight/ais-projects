% JPEG Simulator. Encoder and Decoder. 
% Author: MMLab

% NOTE: this implementation is only for learning purposes. It is therefore
% not optimized and does not provide a JPG file as output. Only the data
% path is simulated. No JPG header are considered.

clear
close all;

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONFIGURE %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%


%File to process
SOURCE= 'barbara';
DEST  = 'barbara_comp';
% File extension
SOURCE_EXT='tif';
DEST_EXT='tif';


%JPEG QUALITY FACTOR
Qf=4;



% JPEG QUANT. MATRIX
% quant_mat=	[16 11 10 16 24 40 51 61 
%              12 12 14 19 26 58 60 55 
%              14 13 16 24 40 57 69 56 
%              14 17 22 29 51 87 80 62 
%              18 22 37 56 68 109 103 77 
%              24 35 55 64 81 104 113 92 
%              49 64 78 87 103 121 120 101 
%              72 92 95 98 112 100 103 99];
% JPEG QUANT. MATRIX
 quant_mat=	[50 10 10 10 10 10 10 10 
              10 10 10 10 10 10 10 10 
              10 10 10 10 10 10 10 10  
             10 10 10 10 10 10 10 10 
              10 10 10 10 10 10 10 10 
              10 10 10 10 10 10 10 10  
              10 10 10 10 10 10 10 10
              10 10 10 10 10 10 10 10];
%quant_mat=	[16 10 10 10 10 10 10 10 
%             10 10 10 19 26 58 60 55 
%             10 10 10 24 40 57 69 56 
%             10 17 22 10 51 87 80 62 
%             10 22 37 56 10 109 103 77 
%             10 35 55 64 81 10 113 92 
%             10 64 78 87 103 121 10 101 
%             10 92 95 98 112 100 103 99];
         
%%%%%%%%%%%%%%%%%%%%%%%
%%% END CONFIGURE %%%%%
%%%%%%%%%%%%%%%%%%%%%%%
         
         
if(Qf>50)
     quant = 2-Qf/50;
else
     quant = 50/Qf;
end
     
quant_mat= quant_mat*quant;      

% read the source file
I = imread( [sprintf(SOURCE) '.' SOURCE_EXT], SOURCE_EXT);
[DIMX, DIMY]=size(I);

if(I)
    disp('Image loaded!');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% application of Sobel filtering before compression
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sy = [ -1 -2 -1        
        0  0  0
        1  2  1 ];
sx = [ -1  0  1
       -2  0  2
       -1  0  1 ];

Ix=filter2(sx, I);
Iy=filter2(sy, I);

I_filtered=sqrt(Ix.^2+Iy.^2)>250;
figure; imshow(I_filtered); title('Before compression');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dctq = @(x) round(dct2(x)./quant_mat);
I_dctq=round(blkproc(I,[8 8], dctq));
I_zz=codezz(I_dctq);

% disp('Encode (RLE+Huffman)');
[CODED_h CODED_rle]=encode(I_zz);
size_coded=size(CODED_h,2)/8;

% disp('Decode');
DECODED_rle=rleinv(CODED_rle, DIMX*DIMY/64);

% disp('Inverse Zig zag');
I_zzinv=decodezz(DECODED_rle, DIMX, DIMY);


%calculate block-based IDCT & IQUANT
disp('IDCT and inverse quantization');
idctq = @(x) round(idct2(x.*quant_mat));
I_idct=blkproc(I_zzinv,[8 8],idctq);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% application of Sobel filtering before compression
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Ix=filter2(sx, I_idct);
Iy=filter2(sy, I_idct);
I_idct_filtered=sqrt(Ix.^2+Iy.^2)>250;
figure; imshow(I_idct_filtered); title('After Compression');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

disp('Writing on file');
DEST_FILE=[DEST '.' DEST_EXT];
imwrite(uint8(I_idct),DEST_FILE, DEST_EXT);


%%%%%%% Statistics %%%%%%%
disp('Compression Ratio:');
DIMX*DIMY/size_coded


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% PSNR & WPSNR calculation  %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
disp('PSNR and WPSNR of original quantized image');
psnr=PSNR(I, uint8(I_idct));
wpsnr=WPSNR(I/255, uint8(I_idct)/255);

disp('MSE of image after Sobel');

E = I_filtered - I_idct_filtered;
E = E.^2;
mse = (mean2(E))^0.5;



disp(psnr);
disp(wpsnr)
disp(mse);
