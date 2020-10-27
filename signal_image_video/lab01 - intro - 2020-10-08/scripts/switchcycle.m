% switch example

shape = 'circle'
%shape = 'dog'

switch shape
    case{'square'}
        disp('squared form')
    case{'circle'}
        disp('circular form')
    otherwise
        disp('Unknown')
end