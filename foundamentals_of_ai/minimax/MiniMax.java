
public class MiniMax {

    // Only for debug, remove in your application
    static int visited = 0;
    static int visited_alphabeta = 0;

    static final int maxLookAhead = 10;
    static final int startAlpha = Integer.MIN_VALUE + 1;
    static final int startBeta = Integer.MAX_VALUE - 1;
    zeroSumGame game;
    int BestMove = -1;

    MiniMax(zeroSumGame Game) {
        game = Game;
    }

    int Start() {
        int v = minimax(game, 0);
        game.play(BestMove);
        return BestMove;
    }

    int StartAlphaBeta() {
        int v = minimax(game, startAlpha, startBeta, 0);
        game.play(BestMove);
        return BestMove;
    }

    // Basic MiniMax
    int minimax(zeroSumGame node, int deep) {
        System.out.println("Step = " + ++visited + ". Node = " + node);
        if (node.isGameOver())
            return node.score();
        if (deep == maxLookAhead)
            return node.score();

        // Index used to store the best move
        int index = -1;
        zeroSumGame c[] = node.newInstances();
        int k = c.length;

        // c[0]...c[k-1] are all the new nodes from current one
        // Moves the player that maximizes
        if (node.isMaxPlayerTurn()) {
            int max = Integer.MIN_VALUE;

            // For each new node in c[i]
            for (int i = 0; i < k; ++i) {
                // Recursively calls minimax
                int v = minimax(c[i], deep + 1);
                // Maximizing the result
                if (v > max) {
                    // Save the best score (the max found so far)
                    max = v;
                    // Stores the index on the best move found so far
                    index = i;
                }
            }
            // Save the best move found
            BestMove = index;

            // Return the best score (for Player Max)
            return max;
        }
        // This code is the same as before but minimizes for Player Min
        else {
            int min = Integer.MAX_VALUE;
            for (int i = 0; i < k; ++i) {
                int v = minimax(c[i], deep + 1);
                // Minimizing the result
                if (v < min) {
                    min = v;
                    index = i;
                }
            }
            BestMove = index;
            return min;
        }
    }

    // MiniMax with alpha/beta pruning optimization
    int minimax(zeroSumGame node, int alpha, int beta, int deep) {
        System.out.println("Step = " + ++visited_alphabeta + ". Node = " + node);
        if (node.isGameOver())
            return node.score();
        if (deep == maxLookAhead)
            return node.score();
        // Index used to store the best move
        int index = -1;
        // c[0]... = all new nodes
        zeroSumGame c[] = node.newInstances();
        if (node.isMaxPlayerTurn()) {
            // For each new node...
            for (int i = 0; i < c.length; ++i) {
                int v = minimax(c[i], alpha, beta, deep + 1);
                // alpha = max(alpha,v);
                if (alpha < v) {
                    alpha = v;
                    index = i;
                    System.out.println("(node " + ((aGame) node).thisNode + ") alpha = " + alpha);
                }
                if (alpha >= beta)
                    break; // alpha/beta pruning
            }
            BestMove = index;
            return alpha;
        } else {
            for (int i = 0; i < c.length; ++i) {
                int v = minimax(c[i], alpha, beta, deep + 1);
                // beta = min(beta,v);
                if (beta > v) {
                    beta = v;
                    index = i;
                    System.out.println("(node " + ((aGame) node).thisNode + ") beta = " + beta);
                }
                if (alpha >= beta)
                    break; // alpha/beta pruning if alpha>=beta
            }
            BestMove = index;
            return beta;
        }
    }
}
