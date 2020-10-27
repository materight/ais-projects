% For cycle: every spot in a NxN matrix ise the sequential
% number of the iteration

N=5;
count = 0;

for k=1:N
    for s=1:N
        A(k,s) = count;
        count = count+1;
    end
end

%echo
A