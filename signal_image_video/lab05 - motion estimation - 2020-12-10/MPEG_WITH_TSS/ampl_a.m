%Questa funzione restituisce la categoria alla quale i coefficienti
%appartengono e la precisione
function [out, prec]=ampl_a(IN);

sIN=sign(IN);
IN=abs(IN);

if (IN <= 1)
   out=1;
   prec=1-IN;
   if(sIN > 0)
       %prec=2^out-prec-1;
       prec=IN;
   end
elseif (IN <= 3)
   out=2;
   prec=3-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif (IN <= 7)
   out=3;
   prec=7-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif (IN <= 15)
   out=4;
   prec=15-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif (IN <= 31)
   out=5;
   prec=31-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif(IN <= 63) 
   out=6;
   prec=63-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif (IN <= 127) 
   out=7;
   prec=127-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif(IN <= 255) 
   out=8;
   prec=255-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif(IN <= 511) 
   out=9;
   prec=511-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif (IN <=1023)
   out=10;
   prec=1023-IN;
   if(sIN > 0)
       prec=IN;
   end
elseif (IN <=2047)
    out=11; % chiamato solo per la DC
    prec=2048-IN;
   if(sIN > 0)
       prec=IN;
   end

end

