%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MPEG Simulator. Estimation and Compensation.                                             %
% last update ...                                                                          %
% Author: Stefano Artuso, Lisanna Canton, Lucrezia Ruggieri, Francesco Salani              %
% NOTE: this implementation is only for learning purposes.                                 %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear;
clc;


%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONFIGURE %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%


Qf=100;

% MPEG QUANT. MATRIX
quant_mat=[8  16 19 22 26 27 29 34
    16 16 22 24 27 29 34 37
    19 22 26 27 29 34 34 38
    22 22 26 27 29 34 37 40
    22 26 27 29 32 35 40 48
    26 27 29 32 35 40 48 58
    26 27 29 34 38 46 56 69
    27 29 35 38 46 56 69 83];


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
%QUALITY SELECTOR
quant_mat= quant_mat*quant;


%READ VIDEO
original_video = VideoReader('mobile_cif .mov');

%WRITE VIDEO
%video_encoded=VideoWriter('video_encoded_withES.avi');
video_encoded=VideoWriter('video_encoded_withES.avi','Uncompressed AVI');
video_encoded.FrameRate=29.97;
%video_encoded.Quality=100;
video_encoded.open;

%COMPENSATION VARIABLES
imgComp_Y=0;
imgComp_Cb=0;
imgComp_Cr=0;

%FILE, WHICH INCLUDES PSNR OF EACH FRAME
fileID = fopen('PSNR_WITH_ES.txt','w');
filemad=fopen('FILEMAD.txt','w');

%FRAME COUNTER
numFrames=1;

%COMPUTATION COSTS
computation_CostsES=0;



%%%%%%%%%%%%%%%%%%%%%%%
%%% END CONFIGURE %%%%%
%%%%%%%%%%%%%%%%%%%%%%%


while (numFrames<17)% hasFrame(original_video)
    
    %%%%%%%%%%%%%%%%%%%%%%%
    %%% MAIN CYCLE    %%%%%
    %%%%%%%%%%%%%%%%%%%%%%%
    
    video_frame = readFrame(original_video);
    
    %FROM RGB TO YCBCR
    YCbCr = rgb2ycbcr(video_frame);
    Y = YCbCr(:,:,1);
    Cb = YCbCr(:,:,2);
    Cr = YCbCr(:,:,3);
    
    %LINEAR INTERPOLATION OF CB AND CR
    Cb_resize=imresize(Cb,0.5,'bicubic');
    Cr_resize=imresize(Cr,0.5,'bicubic');
    
    %%Y DCT QUANT
    dct_Y=round(blkproc(Y,[8 8],@dct2));
    dct_Y_quantized=round(blkproc(dct_Y, [8 8], 'x./P1', quant_mat));
    
    block = dct_Y(1:8,1:8);
    blockq = dct_Y_quantized(1:8,1:8);
    
    %Y IDCT IQUANT
    fun = @(x) round(idct2(x.*quant_mat));
    Y_rec = blkproc(dct_Y_quantized,[8 8],fun);
    
    if(numFrames==1) %FIRST FRAME - INTRA - SIMPLE JPEG
        
        %Y_buffer "THE MEMORY OF THE CODEC" , which contains the frame for each iteration
        
        disp("FRAME "+numFrames+" INTRA");
        Y_buffer = Y_rec;
        imgComp_Y=Y_buffer;
        imgComp_Cb = Cb_resize;
        imgComp_Cr = Cr_resize;
        
    elseif(mod(numFrames,16)==0)  % FRAME INTRA FOR SYNC THE CODEC AND FOR RECOVER THE ERROR
        
        disp("FRAME "+numFrames+" INTRA");
        Y_buffer = Y_rec;
        imgComp_Y=Y_buffer;
        imgComp_Cb = Cb_resize;
        imgComp_Cr = Cr_resize;
        
    else
        
        disp("FRAME "+numFrames);
        %MOTION ESTIMATION
        [motionVect]=motionEstimationTSS(Y_rec,Y_buffer,16,7);
        %MOTION COMPENSATION FOR EACH COMPONENT
        imgComp_Y = motionCompY(Y_buffer, motionVect);
        imgComp_Cb = motionCompC(Cb_resize, motionVect);
        imgComp_Cr = motionCompC(Cr_resize, motionVect);
        
        %video_encoded.writeVideo(RGB)
        Y_buffer =imgComp_Y;
    end
    
    %RE-SIZE OF THE ORIGINAL SIZE OF THE COMPONENTS(Cb, Cr)
    imgComp_Cb_resize=imresize(imgComp_Cb,2,'bicubic');
    imgComp_Cr_resize=imresize(imgComp_Cr,2,'bicubic');
    
    %%FROM YCBCR TO RGB
    YCbCr_s(:,:,1)=imgComp_Y;
    YCbCr_s(:,:,2)=imgComp_Cb_resize;
    YCbCr_s(:,:,3)=imgComp_Cr_resize;
    
    
    errormad=0;
    madcost=  ( abs  (uint8(Y) - uint8(imgComp_Y)) );
    errormad=(sum(sum(madcost)))/(288*352);
    
    RGB = ycbcr2rgb(YCbCr_s);
    video_encoded.writeVideo(RGB);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%% PSNR calculation  %%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    psnr=PSNR(Y, uint8(imgComp_Y));
    
    psnrALL=PSNR(YCbCr, uint8(YCbCr_s));
    
    if(numFrames==1)
        fprintf(fileID,'%6s %16s %20s \r\n','Frames Number','PSNR','COSTS ES');
        fprintf(filemad,'%6s %16s \r\n','Frames Number','MAD_VALUE');
    end
    fprintf(fileID,'%6i %26f %20i \r\n\n',numFrames, psnr,computation_CostsES);
    fprintf(filemad,'%6i %26f \r\n\n',numFrames, errormad);
    
    numFrames=numFrames+1;
    
    %%%%%%%%%%%%%%%%%%%%%%%
    %%% END MAIN CYCLE %%%%%
    %%%%%%%%%%%%%%%%%%%%%%%
    
end
fclose(fileID);
fclose(filemad);
video_encoded.close;