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
video_encoded=VideoWriter('video_encoded_withES.avi','Uncompressed AVI');
video_encoded.FrameRate=29.97;
video_encoded.open;

video_encoded_error=VideoWriter('video_error_ES.avi','Uncompressed AVI');
video_encoded_error.FrameRate=29.97;
video_encoded_error.open;

%COMPENSATION VARIABLES
imgComp_Y_NoError=0;
imgComp_Cb=0;
imgComp_Cr=0;

%Error Variable
error=0;

%FILE, WHICH INCLUDES PSNR OF EACH FRAME
fileID_psnr = fopen('PSNR_WITH_ES.txt','w');
filemad=fopen('MAD_WITH_ES.txt','w');

%FRAME COUNTER
numFrames=1;

%COMPUTATION COSTS
%computation_CostsES=0;

%%%%%%%%%%%%%%%%%%%%%%%
%%% END CONFIGURE %%%%%
%%%%%%%%%%%%%%%%%%%%%%%


while hasFrame(original_video)
    
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
        
        error=0;
        disp("FRAME "+numFrames+" INTRA");
        Y_buffer = Y_rec;
        imgComp_Y_NoError=Y_buffer;
        imgComp_Cb = Cb_resize;
        imgComp_Cr = Cr_resize;
        
    elseif(mod(numFrames,16)==0)  % FRAME INTRA FOR SYNC THE CODEC AND FOR RECOVER THE ERROR
        
        error=0; 
        disp("FRAME "+numFrames+" INTRA");
        Y_buffer = Y_rec;
        imgComp_Y_NoError=Y_buffer;
        imgComp_Cb = Cb_resize;
        imgComp_Cr = Cr_resize;
        
    else
        
        
        disp("FRAME "+numFrames);
        %MOTION ESTIMATION
        [motionVect,EScomputations]=motionEst(Y_rec,Y_buffer);
        %computation_CostsES=computation_CostsES+EScomputations;
        %MOTION COMPENSATION FOR EACH COMPONENT
        imgComp_Y_NoError= motionCompY(Y_buffer, motionVect);
        imgComp_Cb = motionCompC(Cb_resize, motionVect);
        imgComp_Cr = motionCompC(Cr_resize, motionVect);
        
        %IMAGE ERROR
        
        imageSubtract=abs(imsubtract(uint8(imgComp_Y_NoError),Y));
        video_encoded_error.writeVideo(imageSubtract);
     
        %DCT QUANT frame error
        dct_PredictedFrame=round(blkproc(imageSubtract,[8 8],@dct2));
        dct_PredictedFrame_quantized=round(blkproc(dct_PredictedFrame, [8 8], 'x./P1', quant_mat));
        
        block = dct_PredictedFrame(1:8,1:8);
        blockq = dct_PredictedFrame_quantized(1:8,1:8);
        
        %Frame Error IDCT IQUANT
        fun = @(x) round(idct2(x.*quant_mat));
        
        %IMAGE ERROR RESET
        error=0;
        
        error = blkproc(dct_PredictedFrame_quantized,[8 8],fun);
        %bufferImageP_Y=Predicted Image
        bufferImageP_Y=double(imadd(uint8(error),uint8(imgComp_Y_NoError)));
        
        Y_buffer =bufferImageP_Y;
        
    end
    
    %RE-SIZE OF THE ORIGINAL SIZE OF THE COMPONENTS(Cb, Cr)
    imgComp_Cb_resize=imresize(imgComp_Cb,2,'bicubic');
    imgComp_Cr_resize=imresize(imgComp_Cr,2,'bicubic');
    
    %%FROM YCBCR TO RGB
    YCbCr(:,:,1)=Y_buffer;
    YCbCr(:,:,2)=imgComp_Cb_resize;
    YCbCr(:,:,3)=imgComp_Cr_resize;
    
    RGB = ycbcr2rgb(YCbCr);
    video_encoded.writeVideo(RGB);
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%% PSNR calculation  %%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
   
    
    psnr=PSNR(Y, uint8(imgComp_Y_NoError));
    
    
    errormad=0;
    %madcost=  ( abs  (uint8(Y_rec) - uint8(imgComp_Y)) ); NON CONSIDERO
    %ERRORE DI QUANTIZZAZIONE
    madcost=  ( abs  (uint8(Y) - uint8(imgComp_Y_NoError)) );
    errormad=(sum(sum(madcost)))/(288*352);
    
    if(numFrames==1)
        fprintf(fileID_psnr,'%6s %20s %20s \r\n','Frames Number','PSNR');
        fprintf(filemad,'%6s %16s \r\n','Frames Number','MAD_VALUE');
    end
    fprintf(fileID_psnr,'%6i %26f %26f \r\n',numFrames,psnr);
    fprintf(filemad,'%6i %26f \r\n\n',numFrames, errormad);
    
    numFrames=numFrames+1;
    
    %%%%%%%%%%%%%%%%%%%%%%%
    %%% END MAIN CYCLE %%%%%
    %%%%%%%%%%%%%%%%%%%%%%%
    
end
fclose(fileID_psnr);
fclose(filemad);
video_encoded.close;
video_encoded_error.close;