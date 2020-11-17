% Region Growing
% Lab project sample
% Authors: Oscar Tonelli, Paolino Virciglio


clear

% Load image
I = imread ('peppers.jpg');
% Conversion into grayscale, if needed
%I = rgb2gray(I);
% Show the original image
figure; imshow(I); title('Immagine originale');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extract edges
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Compass Operators
s = 50;
NW = [  1  1  0 ;  1  0 -1 ;  0 -1 -1 ] ;  
SW = [  0 -1 -1 ;  1  0 -1 ;  1  1  0 ] ;   
SE = [ -1 -1  0 ; -1  0  1 ;  0  1  1 ] ;   
NE = [  0  1  1 ; -1  0  1 ; -1 -1  0 ] ;   
N  = [  1  1  1 ;  0  0  0 ; -1 -1 -1 ] ;   
S  = [ -1 -1 -1 ;  0  0  0 ;  1  1  1 ] ; 
W  = [  1  0 -1 ;  1  0 -1 ;  1  0 -1 ] ;   
E  = [ -1  0  1 ; -1  0  1 ; -1  0  1 ] ;

contours(:,:,1) = filter2(NW, I)>s;
contours(:,:,2) = filter2(SW, I)>s;
contours(:,:,3) = filter2(SE, I)>s;
contours(:,:,4) = filter2(NE, I)>s;
contours(:,:,5) = filter2(N, I)>s;
contours(:,:,6) = filter2(S, I)>s;
contours(:,:,7) = filter2(E, I)>s;
contours(:,:,8) = filter2(W, I)>s;

% Final edge-compass image
[IF, index] = max( contours, [], 3 );

% Move to black/white image
level = 0.5; 
IF = im2bw(IF,level);

% Apply a median filter to remove standalone edge points
IF = medfilt2(IF,[3 3]); 

% Show the results:
figure; imshow(uint8(IF),[]); title('Edges');

% Extract the dimension of the image
[m,n]=size(IF);

% Zone map
ZM = zeros(m,n); 
% Counter of the space between two differen boundaries
cs = 1; 


%%%%%%%%%%%%%%%%%%%%%%%%%%
% SEEDING
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
l=1;
i=1;
j=1;

% Searching among all the pixel of the image (m X n)
while (i<m)
    j=1;
    while(j<n)
        % Verify not to exceed the dimension of the image summing cs
        while ((j+cs)<n)
            
            % If the pixel is part of an edge, break
            if (IF(i,j) == 1)
                break
            end
            
            % Enlarge cs until I find another edge, then label the zone
            % with 'l' in the center of the zone (in ZM)
            if ((IF(i,j+cs)==1)|| ((j+cs)==(n-1)))
                u = round(((j+cs)+j)/2);
                ZM(i,u)=l;  
                l=l+1;
                break 
            else
                cs =cs+1;
            end
            
        end 
        % Increment the value for searching (manually, it's not a for
        % cycle)
        j = j+cs+1;
        cs =1;
    end
    % Increment the value for searching (manually, it's not a for
    % cycle)
    i = i+1;
end



% Create a matrix of edge starting from ZM
CM  = zeros (m,n);
DN  = im2uint8(I);
DNM = zeros (m,n);
DNM = im2uint8(DNM);
DDIF= 255*ones(m,n);

% Matrix to check if a seed has been processed
PR  = zeros (m,n);

% Matrix that checks if a pixel has been processed in a certain cycle
% (infer uniform enlargment in all directions)
CC  = zeros (m,n);

% Matrix that checks the decimation process
CD = zeros(m,n);


%%%%%%%%%%%%%%%%%%%%%%%
% REMOVING SEED IN EXCESS
%%%%%%%%%%%%%%%%%%%%%%%%

% Removing the seed in vertical direction
for i=1:m
    for j=1:n
        if (ZM(i,j)>0 && CD(i,j)==0)
            c=1;
            di=ZM(i,j);
            while (((i+c)<m) && (ZM(i+c,j)>0))
                c=c+1;
                ZM(i+c-1,j) = 0;
            end
            if (c>1)
                u = round(i+(c/2));
                ZM(u,j)= di;
                CM(u,j)=1;
                CD(u,j)=1;
                DNM (u,j)= DN (i,j);
                ZM(i,j) =0;
            else
             DNM(i,j)=DN(i,j);
             CM(i,j)=1;
            end
        end
    end
end


CD=zeros(m,n);

% Examinating the NE-SW direction
for i=1:m
    for j=1:n
        if (ZM(i,j)>0 && CD(i,j)==0)
            c=1;
            di=ZM(i,j); 
            while ((i+c<m) && (j-c>1) && ZM(i+c,j-c)>0)
                c=c+1;
                ZM(i+c-1,j-c+1) = 0;
                CM(i+c-1,j-c+1) = 0;
            end
            if (c>1)
                u = round(i+(c/2));
                v = round(j-(c/2));
                ZM(u,v)= di;
                CM(u,v)=1;
                CD(u,v)=1;
                DNM (u,v)= DN (i,j);
                ZM(i,j) =0;
                CM(i,j)=0;
            end
        end
    end
end

CD = zeros(m,n);

% Examinating the NW-SE direction
for i=1:m
    for j=1:n
        if (ZM(i,j)>0 && CD(i,j)==0)
            c=1;
            di=ZM(i,j); 
            while ((i+c<m) && (j+c<n) && ZM(i+c,j+c)>0)
                c=c+1;
                ZM(i+c-1,j+c-1) = 0;
                CM(i+c-1,j+c-1) = 0;
            end
            if (c>1)
                u = round(i+(c/2));
                v = round(j+(c/2));
                ZM(u,v)= di;
                CM(u,v)=1;
                CD(u,v)=1;
                DNM (u,v)= DN (i,j);
                ZM(i,j) =0;
                CM(i,j)=0;
            end
        end
    end
end

% Removing seeds 2px-away from existing one
for i=1:m
    for j=1:n
        if (CM(i,j)==1 && i<(m-2) && j<(n-2)&& i>2 && j>2)
            CM(i-2,j-2)=0;
            CM(i-2,j-1)=0;
            CM(i-2,j)=0;
            CM(i-2,j+1)=0;
            CM(i-2,j+2)=0;
            CM(i-1,j-2)=0;
            CM(i-1,j-1)=0;
            CM(i-1,j)=0;
            CM(i-1,j+1)=0;
            CM(i-1,j+2)=0;
            CM(i,j-2)=0;
            CM(i,j-1)=0;
            CM(i,j+1)=0;
            CM(i,j+2)=0;
            CM(i+1,j-2)=0;
            CM(i+1,j-1)=0;
            CM(i+1,j)=0;
            CM(i+1,j+1)=0;
            CM(i+1,j+2)=0;
            CM(i+2,j-2)=0;
            CM(i+2,j-1)=0;
            CM(i+2,j)=0;
            CM(i+2,j+1)=0;
            CM(i+2,j+2)=0;
            
        end
    end
end


figure; imshow(CM); title('Seeds'); 

dnt =2;
totc =0;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Growing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
while totc < 300
 % 4-Connected growing
     for i = 1:m
        for j = 1:n
            if (PR(i,j) == 0 && CM(i,j)==1&& CC(i,j)==0)
                if (j>1)
                    dsx =abs(DNM(i,j)-DN(i,j-1));
                end
                if (j<n)
                    ddx =abs(DNM(i,j)-DN(i,j+1));
                end
                if (i>1)
                    dup =abs(DNM(i,j)-DN(i-1,j));
                end
                if (i<m)
                    ddown=abs(DNM(i,j)-DN(i+1,j));
                end
                % Growing to SX
                if (j>1   && dsx<dnt && (DDIF(i,j-1)>dsx))
                    
                    ZM(i,j-1) = ZM (i,j);
                    CM(i,j-1)= 1;
                    DNM(i,j-1) = DNM (i,j);
                    CC(i,j-1) = 1;
                    DDIF(i,j-1) = dsx;
                  
              
                end
                 % Growing to DX
                if (j<n  && (ddx)<dnt && (DDIF(i,j+1)>ddx))
                     
                    ZM(i,j+1) = ZM (i,j);
                    CM(i,j+1) =1;
                    DNM(i,j+1) = DNM (i,j);
                    CC(i,j+1) = 1;
                    DDIF(i,j+1)= ddx;
                   
                    
                end
                
                 % Growing to N
                if (i>1   && (dup)<dnt &&  (DDIF(i-1,j)>dup))
                   
                    ZM(i-1,j) = ZM (i,j);
                    CM(i-1,j) =1;
                    DNM(i-1,j) = DNM (i,j);
                    CC(i-1,j) = 1;
                    DDIF(i-1,j) = dup;
                    
                end
               
                % Growing to S
                if (i<m && (ddown)<dnt && (DDIF(i+1,j)>ddown))
                    ZM(i+1,j) = ZM (i,j);
                    CM(i+1,j) =1;
                    DNM(i+1,j) = DNM (i,j);
                    CC(i+1,j) = 1;
                    DDIF(i+1,j) = ddown;
                
                end
                
               CM(i,j)=0; 
               PR (i,j) =1;
            end
        end
     end
     CC= zeros(m,n);
  totc = totc+1;

end

% Not Processed pixels: using 4-connected growing some pixels are left
% behind==> fill them.

totc =0;
while totc<50
    for i=1:m
        for j=1:n
            if(ZM(i,j)==0)
                cs=1;
                cw=1;
                while(cw<100)
                    
                if((j-cs)>0 &&(ZM(i,j-cs)>0) )
                    ZM(i,j)=ZM(i,j-cs);
                    DNM(i,j)=DNM(i,j-cs);
                    PR(i,j)=1;
                    break
                end
                if((j+cs)<n &&(ZM(i,j+cs)>0))
                    ZM(i,j)=ZM(i,j+cs);
                    DNM(i,j)=DNM(i,j+cs);
                    PR(i,j)=1;
                    break
                end
                if( (i-cs)>0 &&(ZM(i-cs,j)>0))
                    ZM(i,j)=ZM(i-cs,j);
                    DNM(i,j)=DNM(i-cs,j);
                    PR(i,j)=1;
                    break
                end
                if( (i+cs<m) && (ZM(i+cs,j)>0))
                    ZM(i,j)=ZM(i+cs,j);
                    DNM(i,j)=DNM(i+cs,j);
                    PR(i,j)=1;
                    break
                end
                cw = cw+1;
                cs=cs+1;
                end
            end
        end
    end
    totc= totc+1;
end


figure; imshow(DNM); title('Result');