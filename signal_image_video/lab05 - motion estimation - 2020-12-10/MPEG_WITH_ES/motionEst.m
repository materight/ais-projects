%{
                            MAIN IDEA
 This algorithm calculates the cost function at each possible location in the search window. 
 This leads to the best possible match of the macro-block in the reference frame with a block in another frame.
 The resulting motion compensated image has highest peak signal-to-noise ratio as compared to any other block matching algorithm.
 However this is the most computationally extensive block matching algorithm among all.
 A larger search window requires greater number of computations.
%}

%Input
%   anchor frame : The image for which we want to find motion vectors
%   target_frame : The reference image
%   widthxheight: image size; N: block size, R: search range
%   mvx,mvy: store the MV image

function [motionVectors,EScomputations]=motionEst(anchor_frame,target_frame)

[row,col]=size(target_frame);

%block size
MBsize=16;

%serarch range
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%|--------------------|%%%%%
%%%%%||-------|%%%%%%%%%%%|%%%%%
%%%%%||%%%%%%%|%%%%%%%%%%%|%%%%%
%%%%%||%%%%%%%|------->%%%|%%%%%
%%%%%||%%%%%%%|%%%%%%%%%%%|%%%%%
%%%%%||-------|%%%%%%%%%%%|%%%%%
%%%%%|%%%%|%%%%%%%%%%%%%%%|%%%%%
%%%%%|%%%%|%%%%%%%%%%%%%%%|%%%%%
%%%%%|%%%%|%%%%%%%%%%%%%%%|%%%%%
%%%%%|%%%%v%%%%%%%%%%%%%%%|%%%%%
%%%%%|%%%%%%%%%%%%%%%%%%%%|%%%%%
%%%%%|--------------------|%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
search_Range=16;

%matrix where the MV are memorized
vectors = zeros(2,col*row/MBsize^2);

%computational cost
computations = 0;

% we start off from the top left of the image
% we will walk in steps of 16
% for every macroblock that we look at we will look for
% a close match 16 pixels on the left, right, top and bottom of it

mbCount = 1;

for i=1:MBsize:row-MBsize+1
    for j=1:MBsize:col-MBsize+1
        
        %for every block in the anchor frame
        MAD_min = 256*MBsize*MBsize;
        mvx=0;
        mvy=0;
        
        for k=-search_Range:1:search_Range
            for l=-search_Range:1:search_Range
                refBlkVer = i + k;   % row/Vert co-ordinate for ref block
                refBlkHor = j + l;   % col/Horizontal co-ordinate
                %border conditions
                if ( refBlkVer < 1 || refBlkVer+16-1 > row ...
                        || refBlkHor < 1 || refBlkHor+16-1 > col)
                    continue;
                end
                MAD=costFunctionMAD(anchor_frame(i:i+16-1,j:j+16-1), ...
                    target_frame(refBlkVer:refBlkVer+16-1, refBlkHor:refBlkHor+16-1), 16);
                computations = computations + 1;
                if MAD<MAD_min
                    MAD_min=MAD;
                    dy=k;
                    dx=l;
                end
                
            end
        end

        iblk=floor((i-1)/MBsize+1);
        jblk=floor((j-1)/MBsize+1); 
        mvx(iblk,jblk)=dx;
        mvy(iblk,jblk)=dy; 
        
        vectors(1,mbCount)=mvy(iblk,jblk);
        vectors(2,mbCount)=mvx(iblk,jblk);
        mbCount = mbCount + 1;
        
        %disegno le freccie
        %arrow([i,j],[mvy(iblk,jblk),mvx(iblk,jblk)], 3);
        
    end
end

motionVectors=vectors;
EScomputations = computations/(mbCount - 1);

end





