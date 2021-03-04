% Computes the Mean Absolute Difference (MAD) for the given two blocks
% Input
%       currentBlk : The block for which we are finding the MAD
%       refBlk : the block w.r.t. which the MAD is being computed
%       mbSize : the side of the two square blocks

function cost = costFunctionMAD(anchor_frame,target_frame, mbSize)

err = 0;
for i = 1:mbSize
    for j = 1:mbSize
        err = err + abs((anchor_frame(i,j) - target_frame(i,j)));
    end
end
cost = err / (mbSize*mbSize);

