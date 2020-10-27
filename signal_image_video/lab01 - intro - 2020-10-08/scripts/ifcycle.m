% Example of if-then-else control

k=3;
s=3;

if k==s
    A = ones(5,5);
elseif k<s
    A= zeros(5,5);
else 
    A = rand(5,5);
end

%echo
A