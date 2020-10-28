public interface zeroSumGame {
    int score();

    boolean isGameOver();

    boolean isMaxPlayerTurn();

    zeroSumGame[] newInstances();

    void play(int index);
}
