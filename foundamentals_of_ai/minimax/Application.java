
public class Application {

    public static void main(String[] args) {

        aGame game1 = new aGame(true);
        aGame game2 = new aGame(true);

        MiniMax m1 = new MiniMax(game1);
        MiniMax m2 = new MiniMax(game2);

        System.out.println("Minimax:");
        int simpleMiniMax = m1.Start();
        System.out.println(simpleMiniMax);

        System.out.println("\nMinimax with alpha-beta pruning:");
        int alphabeta = m2.StartAlphaBeta();
        System.out.println(alphabeta);
    }

}
