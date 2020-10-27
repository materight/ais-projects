%Function: sum of 3 numbers

function[out] = mmSum(first, second, third )

out =   0;

if isnumeric(first) == false
    disp( first ) 
    disp('not a number')
    return
end
    
if isnumeric(second) == false
    disp( second )
    disp('not a number')
    return
end

if isnumeric(third) == false
    disp( third )
    disp('not a number')
     return
end
   
out = first + second + third;