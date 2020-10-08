import java.util.ArrayList;
import java.util.Comparator;
import java.util.Random;

// Genetic algorithm to solve a Sudoku
public class App{

    int numberOfGenerations = 2000; // Number iterations
    int numberOfIndividuals = 200; // Number of individuals
    int tournamentSize = 8; // Number of best individuals to be selected at each iteration
    double mutationProbability = 0.5; // Probability of executing a mutation

    ArrayList<Individual> individuals;

    public static void main(String[] args) { new App(); }

    public App(){
        individuals = new ArrayList<>();
        
        // Generation of initial population
        for(int i = 0; i < numberOfIndividuals; i++) {
            individuals.add(new Individual());
        }

        double bestFitness = Individual.SIZE;
        int bestFitnessGeneration = 0;
        int generation = 0;
        for(generation = 0; generation < numberOfGenerations + 1; generation++){
            // Compute and sort by fitness value (lower fitness ==)
            for(Individual i : individuals) i.computeFitness();
            individuals.sort(Comparator.comparing(Individual::getFitness));

            Individual best = individuals.get(0);
            System.out.println("Gen #" + generation + " best: " + (best.getFitness()));
             
            // If a individual with fitness = 0 is found, stop because we found a solution
            if(best.getFitness() == 0) break;
            
            // If there are no advancements, restart with a new random population 
            if(best.getFitness() >= bestFitness && generation - bestFitnessGeneration > 200){ 
                for(int i = 0; i < numberOfIndividuals; i++) individuals.add(new Individual());
                for(Individual i : individuals)i.computeFitness();
                individuals.sort(Comparator.comparing(Individual::getFitness));
            } else if(best.getFitness() < bestFitness){
                bestFitness = best.getFitness();
                bestFitnessGeneration = generation;
            }

            if(generation < numberOfGenerations){
                // Evolution process:
                // 1) Selection
                ArrayList<Individual> parents = selection(individuals);

                // 2) Crossover
                ArrayList<Individual> offsprings = crossover(parents);
                
                // 3) Mutation
                offsprings = mutation(offsprings);
                individuals = offsprings;
            }
        }

        Individual best = individuals.get(0);
        System.out.println("\n\nBEST FITNESS: " + best.getFitness() + ", GEN: #" + (generation - 1) + " \n");
        System.out.println(best);
    }

    // Select best K = tournamentSize individuals
    public ArrayList<Individual> selection(ArrayList<Individual> individuals){
        ArrayList<Individual> best = new ArrayList<>();
        for (int i=0; i < tournamentSize; i++) best.add(individuals.get(i));
        return best;
    }

    public ArrayList<Individual> crossover(ArrayList<Individual> parents){
        ArrayList<Individual> offsprings = new ArrayList<>();
        offsprings.addAll(parents); // Keep the best in the new generation
        Random random = new Random();
        for(int i = parents.size(); i < numberOfIndividuals; i++){
            // Select two random parents
            Individual p1 = parents.get(random.nextInt(parents.size()));
            Individual p2 = parents.get(random.nextInt(parents.size()));
            // Select a random crossover point, i.e. a row (exluding row 0 and 8)
            int crossoverPoint = (random.nextInt(Individual.D - 2) + 1) * Individual.D; // Or random.nextInt(Individual.SIZE); for a random point 
            // Execute crossover
            Individual newChild = new Individual(p1, p2, crossoverPoint);
            offsprings.add(newChild);
        }
        return offsprings;
    }

    public ArrayList<Individual> mutation(ArrayList<Individual> individuals){
        Random random = new Random();
        for(Individual individual : individuals){
            if(random.nextDouble() < mutationProbability){
                // individual.mutateRow(random.nextInt(Individual.D)); // Shuffle a row
                // individual.mutateMisplacedCell(random.nextInt(Individual.D) + 1); // Mutate a misplaced cell
                individual.mutateCell(random.nextInt(Individual.SIZE), random.nextInt(Individual.D) + 1); // Mutate a single cell
            }
        }
        return individuals;
    }
}