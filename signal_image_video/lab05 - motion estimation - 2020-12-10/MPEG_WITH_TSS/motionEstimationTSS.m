%{
                            MAIN IDEA

    Start with search location at center
    Set step size ?stepSize? = 4 and search parameter ?p? = 7
    Search 8 locations +/- S pixels around location (0,0) and the location (0,0)
    Pick among the 9 locations searched, the one with minimum cost function
    Set the new search origin to the above picked location
    Set the new step size as stepSize = stepSize/2
    Repeat the search procedure until stepSize = 1
    The resulting location for stepSize=1 is the one with minimum cost function and the macro block at this location is the best match.

    There is a reduction in computation by a factor of 9 in this algorithm.
    For p=7, while ES evaluates cost for 225 macro-blocks, TSS evaluates only for 25 macro blocks
%}

% Computes motion vectors using Three Step Search method
%
% Input
%   anchor_frame : The image for which we want to find motion vectors
%   target_frame : The reference image
%   mbSize : Size of the macroblock --> 16
%   p : Search parameter = 7
%
% Ouput
%   motionVect : the motion vectors for each integral macroblock in imgP

function [motionVect,TSScomputations] = motionEstimationTSS(anchor_frame, target_frame, mbSize, p)

[row,col] = size(target_frame);
vectors = zeros(2,row*col/mbSize^2);

costs = ones(3, 3) * 65537;

computations = 0;

% we now take effectively log to the base 2 of p
% this will give us the number of steps required

L = floor(log10(p+1)/log10(2));
stepMax = 2^(L-1);

% START SEARCHING FROM THE TOP LEFT OF THE IMAGE
% WE WILL WALK IN STEPS OF MBSIZE
% for every marcoblock that we look at we will look for
% a close match p pixels on the left, right, top and bottom of it

mbCount = 1;
for i = 1 : mbSize : row-mbSize+1
    for j = 1 : mbSize : col-mbSize+1
        
        % STARTING POINT:
        % we will evaluate 9 elements at every step
        
        x = j;
        y = i;
        
        % In order to avoid calculating the center point of the search
        % again and again we always store the value for it from the
        % previous run. For the first iteration we store this value outside
        % the for loop, but for subsequent iterations we store the cost at
        % the point where we are going to shift our root.
        
        costs(2,2) = costFunctionMAD(anchor_frame(i:i+mbSize-1,j:j+mbSize-1), ...
            target_frame(i:i+mbSize-1,j:j+mbSize-1),mbSize);
        
        computations = computations + 1;
        
        stepSize = stepMax;
        while(stepSize >= 1)
            
            % m is row(vertical) index
            % n is col(horizontal) index
            % this means we are scanning in raster order
            
            for m = -stepSize : stepSize : stepSize
                for n = -stepSize : stepSize : stepSize
                    
                    refBlkVer = y + m;   % row/Vert co-ordinate for ref block
                    refBlkHor = x + n;   % col/Horizontal co-ordinate
                    
                    %bound condition
                    if ( refBlkVer < 1 | refBlkVer+mbSize-1 > row ...
                            | refBlkHor < 1 | refBlkHor+mbSize-1 > col)
                        continue;
                    end
                    
                    %we don't wanna to save the center point we have
                    %already done 
                    
                    costRow = m/stepSize + 2;
                    costCol = n/stepSize + 2;
                    
                    if (costRow == 2 & costCol == 2)
                        continue
                    end
                    
                    costs(costRow, costCol ) = costFunctionMAD(anchor_frame(i:i+mbSize-1,j:j+mbSize-1), ...
                        target_frame(refBlkVer:refBlkVer+mbSize-1, refBlkHor:refBlkHor+mbSize-1), mbSize);
                    computations = computations + 1;
                    
                end
            end
            
            % Now we find the vector where the cost is minimum
            % and store it ... this is what will be passed back.
            
            [dx, dy, min] = minCost(costs);      % finds which macroblock in imgI gave us min Cost
            
            
            % shift the root for search window to new minima point
            
            x = x + (dx-2)*stepSize;
            y = y + (dy-2)*stepSize;
            
            % Arohs thought: At this point we can check and see if the
            % shifted co-ordinates are exactly the same as the root
            % co-ordinates of the last step, then we check them against a
            % preset threshold, and ifthe cost is less then that, than we
            % can exit from teh loop right here. This way we can save more
            % computations. However, as this is not implemented in the
            % paper I am modeling, I am not incorporating this test.
            % May be later...as my own addition to the algorithm
            
            stepSize = stepSize / 2;
            costs(2,2) = costs(dy,dx);
            
        end
        vectors(1,mbCount) = y - i;    % row co-ordinate for the vector
        vectors(2,mbCount) = x - j;    % col co-ordinate for the vector
        mbCount = mbCount + 1;
        costs = ones(3,3) * 65537;
        
        %arrow([i,j],[i+dy,j+dx], 3);
        
        
    end
end

motionVect = vectors;
TSScomputations = computations/(mbCount - 1);