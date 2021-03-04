
%Input
%   f1 : The image for which we want to find motion vectors->anchor frame
%   f2 : The reference image->target frame
%   widthxheight: image size; N: block size, R: search range
%   mvx,mvy: store the MV image

function [motionVectors]=motionEst(anchor_frame,target_frame)

[row,col]=size(target_frame);

N=16;
R=16;

vectors = zeros(2,col*row/N^2);

% we start off from the top left of the image
% we will walk in steps of 16
% for every macroblock that we look at we will look for
% a close match 16 pixels on the left, right, top and bottom of it
mbCount = 1;

for i=1:N:row-N+1
    for j=1:N:col-N+1
        
        %for every block in the anchor frame
        MAD_min = 256*N*N;
        mvx=0;
        mvy=0;
        %condizioni al bordo
        %{
        if (i==1)
            starty = 0;
        else
            starty = -R;
        end
        
        if (i==row-N)
            endy = 0;
        else
            endy = R;
        end
        
        if (j==1)
            startx = 0;
        else
            startx = -R;
        end
        
        if (j==col - N)
            endx = 0;
        else
            endx = R;
        end
        %}
        
        for k=-R:1:R
            for l=-R:1:R
                refBlkVer = i + k;   % row/Vert co-ordinate for ref block
                refBlkHor = j + l;   % col/Horizontal co-ordinate
                %condizioni di bordo
                if ( refBlkVer < 1 || refBlkVer+16-1 > row ...
                        || refBlkHor < 1 || refBlkHor+16-1 > col)
                    continue;
                end
                MAD=costFunctionMAD(anchor_frame(i:i+16-1,j:j+16-1), ...
                    target_frame(refBlkVer:refBlkVer+16-1, refBlkHor:refBlkHor+16-1), 16);
                if MAD<MAD_min
                    MAD_min=MAD;
                    dx=k;
                    dy=l;
                end
                
            end
        end
        
        %fp(i:i+N-1,j:j+N-1)=target_frame(i+dy:i+dy+N-1,j+dx:j+dx+N-1);
        %put the best matching block in the predicted image
        iblk = floor((i-1)/N+1);
        jblk=floor((j-1)/N+1); %blockindex
        mvx(iblk,jblk)=dx;
        mvy(iblk,jblk)=dy; %record the estimated MV
        
        vectors(1,mbCount)=mvx(iblk,jblk);
        vectors(2,mbCount)=mvy(iblk,jblk);
        mbCount = mbCount + 1;
        
        %disegno le freccie
        %arrow([i,j],[i+dy,j+dx], 3);
        
    end
end

motionVectors=vectors

end





