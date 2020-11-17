%RLE decoding
%
% note: Out=RLEinv(IN);
% 
% 
function frame=rleinv(IN, Bs);

frame=[];
EOB='00000000'; %EOB
Z='11110000'; %16 zeros

val=[];

%parsing untill the last block Bs
i=1;

for k=1:Bs
    %k
    B=zeros(1,64);
    B(1)=bin2dec(IN(i:i+10)); 
   
    i=i+11;

    c=1;

    s=size(IN,2);

    if(i<=s-7)
        while (strcmp(IN(i:i+7), EOB)~=1)
            if(strcmp(IN(i:i+7), Z)~=1)
                nZ=bin2dec(IN(i:i+3)); %number of zeros NNNN | SSSS from first 4 bits
                cat=bin2dec(IN(i+4:i+7)); %cat
                prec=bin2dec(IN(i+8:i+7+cat)); % precision
                i=i+8+cat; %pointer
                c=c+nZ+1; %after zeros         
                if(prec < 2^cat/2)
                  B(c)= -(2^cat-1)+prec;
                else
                  B(c)= prec;
                end
            else
                i=i+8;
            end
           
        end
        i=i+8;    
        frame=[frame B];
    end

       

end