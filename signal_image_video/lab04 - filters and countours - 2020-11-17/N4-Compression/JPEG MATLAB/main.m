% JPEG Simulator. Encoder and Decoder. 
% last update 27-05-07
% Author: Nicola Conci

% NOTE: this implementation is only for learning purposes. It is therefore
% not optimized and does not provide a JPG file as output. Only the data
% path is simulated. No JPG header are considered.

clear

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONFIGURE %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%


%File to process
SOURCE= 'lena';
DEST  = 'lena_comp';
% File extension
SOURCE_EXT='tif';
DEST_EXT='tif';


%JPEG QUALITY FACTOR
Qf=89;

%%%%%%%%%%%%%%%%%%%%%%%
%%% END CONFIGURE %%%%%
%%%%%%%%%%%%%%%%%%%%%%%

% JPEG QUANT. MATRIX
quant_mat=	[16 11 10 16 24 40 51 61 
             12 12 14 19 26 58 60 55 
             14 13 16 24 40 57 69 56 
             14 17 22 29 51 87 80 62 
             18 22 37 56 68 109 103 77 
             24 35 55 64 81 104 113 92 
             49 64 78 87 103 121 120 101 
             72 92 95 98 112 100 103 99];
         
             
%*******************
%   QUANTIZATION
%*******************



if(Qf < 1)
    Qf = 1;
else if (Qf > 100 )
        Qf = 100;
    end
end
        

quant = 101-Qf;


quant_mat= quant_mat*quant;      

% read the source file
I = imread( [sprintf(SOURCE) '.' SOURCE_EXT], SOURCE_EXT);
[DIMX, DIMY]=size(I);
if(I)
    disp('Image loaded!');
end

disp('Apply DCT');
dct_I=round(blkproc(I,[8 8],@dct2));

disp('Quantize');
dct_Iq=round(blkproc(dct_I, [8 8], 'x./P1', quant_mat));

disp('Zig zag scanning');
[dct_Iq_zz]=codezz(dct_Iq);

disp('Encode (RLE+Huffman)');
[CODED_h CODED_rle]=encode(dct_Iq_zz);
size_coded=size(CODED_h,2)/8;

disp('Decode');
DECODED_rle=rleinv(CODED_rle, DIMX*DIMY/64);

disp('Inverse Zig zag');
zz_inv=decodezz(DECODED_rle, DIMX, DIMY);


%calculate block-based IDCT & IQUANT
disp('IDCT and inverse quantization');
fun = @(x) round(idct2(x.*quant_mat));
idct_I=blkproc(zz_inv,[8 8],fun);


disp('Writing on file');
DEST_FILE=[DEST '.' DEST_EXT];
imwrite(uint8(idct_I),DEST_FILE, DEST_EXT);


%%%%%%% Statistics %%%%%%%
disp('Compression Ratio:');
DIMX*DIMY/size_coded


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% PSNR & WPSNR calculation  %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
disp('PSNR and WPSNR of original quantized image');
psnr=PSNR(I, uint8(idct_I));
% Normalizzare su (0,1) per il WPSNR
wpsnr=WPSNR(I/255, uint8(idct_I)/255);

disp(psnr);
disp(wpsnr);









