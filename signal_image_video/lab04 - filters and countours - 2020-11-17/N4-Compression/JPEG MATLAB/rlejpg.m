%This function creates the (Size, Amplitude) pairs for the DC coefficient
% and (Runlength, Size)(Amplitude) for AC coefficients
%in a single 64 elements block
%HUFFMAN strings are then created


function [huff, u, DC]=rlejpg(IN, DC);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% load Huffman table
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

hufftab;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% extracting no zero coefficients 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
values=[];

% estrazione dei valori AC che sono diversi da zero
values(2,:)=find(IN~=0);

if(size(values,2)~=0)
    values(1,:)=IN(values(2,:));
    values(3,:)=sign(IN(values(2,:)));

    %verifico se manca la continua e in caso la aggiungo
    if(values(2,1)~=1)
        DCadd=[];
        DCadd(2,:)=1;
        DCadd(1,:)=0;
        DCadd(3,:)=sign(IN(1));
        values=[DCadd values];
    end
end

% first coefficient is DC

u=dec2bin(IN(1),11);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DC coding
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DCdiff=IN(1)-DC;
DC=IN(1);
[cat, prec]=ampl_a(DCdiff);
DCcat=hufftabDC(cat, 1:9);
DCcat= strrep(DCcat,' ','');
huff=[DCcat dec2bin(prec, cat)];

i=2;

byte='';

while i<=size(values,2)
    
    %in z we store the number of zeros
    z=values(2,i)-values(2,i-1)-1; 
    
        
    %if zeros are >=16 
    while (z>=16)
        u=strcat(u, dec2bin(240, 8));
        huff=strcat(huff, '11111111001');
        z=z-16;
        
    end
    
    [cat, prec]=ampl_a(values(1,i));

    %RLE string
    u=strcat(u, dec2bin(z,4), dec2bin(cat,4), dec2bin(prec, cat));
    if(cat>10)
        disp('uuuhhhhh');
    end
    %Huffman string
    index=(z*10)+cat;
    code=hufftabjpg(index, 1:16);
    code=strrep(code,' ','');
    
    huff=strcat(huff, code, dec2bin(prec, cat));

    i=i+1;
    
    
    
end

% inserting EOB. 00000000

u=strcat(u, '00000000');
huff=strcat(huff, '1010');

