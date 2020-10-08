import java.util.Random;
import java.util.ArrayList;
import java.util.Collections;

public class Individual{
    
    static final int N = 3; // Sub-square size
    static final int D = N*N; // Columns and rows size
    static final int SIZE = D*D; // Total number of cells

    // Data structure for representing the sudoku
    int[] data = new int[SIZE];
    Double fitness = null;

    // Random initialized
    public Individual(){
        // Random permutations of values [1, ..., 9] for each row
        ArrayList<Integer> values = new ArrayList<>();
        for(int i =0; i<D; i++) values.add(i+1);

        for(int i = 0; i < D; i++){
            Collections.shuffle(values);
            for(int j = 0; j < D; j++){
                data[i * D + j] = values.get(j);
            }
        }
    }

    // Initialized from a crossover
    public Individual(Individual p1, Individual p2, int crossoverPoint){
        for(int i = 0; i < crossoverPoint; i++) data[i] = p1.data[i];
        for(int i = crossoverPoint; i < SIZE; i++) data[i] = p2.data[i];
    }

    public void mutate(int position, int newValue){
        data[position] = newValue;
    }

    public void computeFitness(){
        // Single number in each row, column and subsquare
        fitness = 0.0;
        boolean[] misplaced = computeMisplaced();

        // Count number of misplaced number
        for(int i = 0; i < D; i++){
            for(int j = 0; j < D; j++){
                if(misplaced[i * D + j]) fitness++;
            }
        }
    }

    public Double getFitness() {
        return fitness;
    }

    public boolean[] computeMisplaced(){
        boolean[] misplaced = new boolean[SIZE];
        // Check rows
        for(int i = 0; i < D; i++){
            boolean[] v = new boolean[D + 1]; // Numbers are from 1 to 9 included
            for(int j = 0; j < D; j++){
                int pos = i*D + j;
                if(!v[data[pos]]) v[data[pos]] = true;
                else misplaced[pos] = true;
            }
        }
        // Check columns
        for(int j = 0; j < D; j++){
            boolean[] v = new boolean[D + 1];
            for(int i = 0; i < D; i++){
                int pos = i * D + j;
                if(!v[data[pos]]) v[data[pos]] = true;
                else misplaced[pos] = true;
            }
        }
        // Check squares
        for(int si = 0; si < N; si++){
            for(int sj = 0; sj < N; sj++){
                // For each subsquare
                boolean[] v = new boolean[D + 1];
                for(int i = 0; i < N; i++){
                    for(int j = 0; j < N; j++){
                        // For each cell in the subsquare
                        int pos = (si * N + i) * D + (sj * N + j);
                        if(!v[data[pos]]) v[data[pos]] = true;
                        else misplaced[pos] = true;
                    }
                }
            }
        }
        return misplaced;
    }

    @Override
    public String toString(){
        boolean[] misplaced = computeMisplaced();
        String ret = "";
        for(int i = 0; i < D; i++){
            for(int j = 0; j < D; j++){
                String value = "" + data[i * D + j];
                if(misplaced[i * D + j]) value = "\u001B[31m" + value + "\u001B[0m";
                ret += value + (((j+1) % 3 == 0) ? " | " : " ");
            }
            ret += ((i+1) % 3 == 0) ? "\n-----------------------\n" :"\n";
        }
        return ret;
    }
}