
public class aGame implements zeroSumGame {

    public int thisNode;
    private boolean player;
    private int[] list;
    static final int f1[] = { 11, 12, 13 }, f11[] = { 21, 22, 23 }, f12[] = { 24, 25, 26 }, f13[] = { 27, 28, 29 };

    // Default constructor
    aGame(boolean Player) {
        // Initial status
        thisNode = 1;
        // Player who moves first (Max in this case)
        player = Player;
    }

    // Constructor used in newInstances()
    aGame(aGame game, int m) {
        // The move goes to the contender
        player = !game.player;
        // Set the node to the right value
        thisNode = m;
    }

    // Return the score for any final position
    public int score() {
        int p[] = { 9, 8, 7, 6, 5, 4, 3, 2, 1 };
        if (thisNode > 20)
            return p[thisNode - 21];
        else
            return 0;
    }

    // Game over if a node from 21 to 29 is reached
    public boolean isGameOver() {
        return thisNode > 20 && thisNode < 30;
    }

    public boolean isMaxPlayerTurn() {
        return player;
    }

    public zeroSumGame[] newInstances() {
        // Get (privately) a list of k moves
        int k = getList();
        // Generates a k sized array
        zeroSumGame c[] = new zeroSumGame[k];
        for (int i = 0; i < k; ++i)
            c[i] = new aGame(this, list[i]);
        return c;
    }

    public void play(int index) {
        // The new node is the one indexed in the list
        thisNode = list[index];
        // The moves goes to the opponent
        player = !player;
        System.out.println("My move is: " + list[index]); // debug
    }

    public String toString() {
        return "Node: " + thisNode;
    }

    private int getList() {
        switch (thisNode) {
            case 1:
                list = f1;
                break;
            case 11:
                list = f11;
                break;
            case 12:
                list = f12;
                break;
            case 13:
                list = f13;
                break;
        }
        return list.length;
    }
}
