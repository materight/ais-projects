# Bio-Inspired Artificial Intelligence - Lab. Notes  

All the experiment have been run with seed = 42

## Lab. 01

## Lab. 02

## Lab. 03

### Exercise 1
- **What happens if you make λ smaller e.g. λ = μ?** \
By decreasing λ (and maintaining the number of evaluations constant by increasing the "max_generations" param accordingly) we obtain a faster convergence speed, while the results in the long run remain quite stable across the different values of λ.

- **What happens if you increase the mixing number ρ?** \
By increasing the mixing number ρ, the overall fitness is better (lower) and the convergence speed is much faster. This is probably because we are using more parents, increasing the variability of the generated offspring.

- **Try out the different strategy modes and observe how they affect the performance of the algorithm** \
The results changes based on the value of ρ. With a ρ=1, between None (no self-adaptation), Global and Individual strategies, Global gives the better results by a factor of 50 w.r.t. the Individual strategy. However, if we increase the value of ρ s.t. ρ>1, e.g. ρ=5, the Individual strategy obtain the best performances overall, by a factor of 10 w.r.t. the Global, while the performance of the None strategy are far behind (fitness = ~143 against ~0.02 of Individual). 

### Exercise 2

- **How does the self-adaptation strategy influence performance on this problem?** \
As mentioned before, None, Global and Individual obtain increasingly better results (in this order) with a ρ>1.

- **Does what you see here confirm what you suspected from the previous exercise?** \
Yes, as mentioned above.

- **How do the values of μ, ρ, and λ influence the performance given a particular self-adaptation strategy and other parameters?** \
With ρ=1, the Global self-adaptation strategy gives the best results, while with ρ>1 the Individual strategy seems to be the best choice.
Regarding the values of λ, with a lower value (e.g. 20) gives better results using the Global strategy, while a higher value (e.g 200) gives better results when using the Individual strategy.

- **Can you come up with any rules of thumb for choosing these parameters?** \
In general, with ρ=1, it may be better to use a Global self-adaptation strategy. In the other cases, with ρ>1, the Individual strategy seems to give the best results. The performance of the None strategy are in every case worse, so it may preferable to not use it.

- **Can you find a choice of parameters that work properly across several problems?** \
After some testing, the parameters that gives the best results across different problems are:
    - μ = 20
    - λ = 120
    - ρ = 10
    - self-adaptation strategy = Individual

### Exercise 3

- **Can CMA-ES find optima to different problems with fewer function evaluations?** \
TODO

- **How do these differences change with different pop. sizes and problem dimensions?** \
TODO

### Questions
- **Do the observations you made while varying μ, ρ, and λ confirm or contradict the conclusions you drew last week?** \
TODO

- **What are the advantages of self-adaptation in evolutionary computation?** \
TODO

- **In what ways might self-adaptation be occurring in biological organisms?** \
TODO

- **Compare the different self-adaptation strategies explored in this exercise. In what ways are certain strategies better than others for optimization? In what ways are certain strategies more biologically plausible than others?** \
TODO

- **Describe what reasons may contribute to better performance of CMA-ES and what can be the conditions when CMA-ES is not better than a basic ES.** \
TODO

## Lab. 04 (Multi-Objective Problems)

### Exercise 1 (Scalarization)
- **What happens when you run the GA with this fitness function (Kursawe)?** \
The GA try to find a solution that go towards the minimum on both objectives. In particular, with both weights set to 0.5, we can clearly see that the GA algorithm find solution that are very close to one of the local minimums of the second objective, in particular to the local minimum that is closer to the global minimum of the first objective.

- **Why do you obtain this result?** \
This is because both objectives are given the same importance. However, since the fitness values of the second objective are much larger outside the local minimum, the GA try to first find solutions that are in that minimum. Therefore the final population displacement resemble a cross, similar to the landscape of the second objective function. Between all the local minimum however, the GA select the one nearer to the global minimum of the second objective.

- **What happens if you give the first (or second) objective all of the weight?** \
By giving all the weights to the first objective, the GA find a best solution only for that objective, therefore we obtain a population centered on its global minimum. The same result is obtained if we assign all the weights to the second objective, with the GA minimizing only that function.

- **Can you find a weighting able to find a solution that approaches the optimum on both objectives?** \
By setting the weights to `[0.7, 0.3]` we find a good compromise between the fitness on the two objectives, i.e. we obtain a fitness of -6.79 for the first and -6.82 for the second.

- **Does your weighting still work on the new problem (DTLZ7)?** \
If we use DTLZ7 with `num_obj = 2` and weights `[0.7, 0.3]` we obtain a fitness of 0 for the first objective and 4.0 for the second objective. However, if we change the weights to `[0.55, 0.45]`, we obtain finesses of 0.85 and 2.86 respectively, a solution that may preferable based on the context.

- **Can you think of a method for combining the objectives that might work better than using a weighted sum?** \
In the case of DTLZ7, if we want to obtain a better fitness on the second objective, we may want to compute the total fitness as a non-linear combination of the fitnesses, e.g. f = f1^0.5 + f2^2

### Exercise 2 (NSGA-2)
- **How do the solutions you find here compare to those found in Exercise 1?** \
In the case of Kursawe, the results found in the previous exercise, in particular with weights `[0.7, 0.3]`, could still be considered "acceptable" since they will still belong to the Pareto front.

- **Is there a single solution that is clearly the best?** \
No, since the final Pareto front includes all the solutions that are incomparable with each others, i.e. they are all non-dominated. For this reason, there is no single best solution that is clearly best than the others

- **Can you still find good solutions (with DTLZ7)?** \
Yes, the found solutions are still good compared to the ones found in Exercise 1 (still considering num_obj=2 and num_vars=21), i.e. the solution found before could still be part of the Pareto front.

- **What happens if you increase the population size or the number of generations?** \
By increasing the population size (e.g. from 50 to 200), we obtain more solutions on the Pareto front, but the total coverage of the Pareto front remains the same, with more crowded areas. \
By increasing the number of generations (e.g. from 100 to 400), we obtain a better approximation of the real Pareto front, i.e. the solutions are more aligned with the real expected Pareto front. Therefore we obtain better non-dominated solutions.

### Exercise 3

- **Is the algorithm able to find reasonable solutions to this problem?** \
Yes, for example a solution (found with pop_size=10 and max_gen=10) with a weight of 1.17Kg and a brake time of 4.16 seconds seems a reasonable solution for a real brake system. If we increase the pop_size (e.g. to 100), we obtain more solutions to choose from in the Pareto front, but the results are not very different from the previous ones. If we instead increase the maximum number of generations (e.g. to 100), we obtain clearly better solutions, for example 0.62kg and 3.73 seconds.

- **Do you see any patterns in the Pareto-optimal solutions that may help you in designing a well-performing disk-brake in the future?** \
The obtained Pareto front has a clear descending pattern, with an elbow at ~0.62kg that can be identified as shown in the image below. Before the elbow, the stopping time (f1) decrease rapidly with a minimum increase in the total weight (f0). An optimal approach may be to select the nearest solution to this elbow, since after that value the weight increase rapidly without any noteworthy improvement on the stopping time.

<div style="text-align:center">
    <img src="img/lab04_es3_1.png" alt="Pareto front analysis" width="300"/>
</div>

### Questions

- **When do you think it is appropriate to use a multi-objective evolutionary algorithm vs. combining multiple objectives into a single fitness function?** \
When there is a clear relation between the objectives that we want to optimize, it is probably better to exploit this relation and combine the objectives into a single fitness function. In the other cases, or if we want to have a better idea of the kind of optimization problem and possible solutions we are dealing with, it may be better to stick with a multi-objective EA.

- **What can the results of a multi-objective algorithm teach us about exploring the design spaces of engineering problems?** \
It can be useful to understand what kind of trade-off between the objectives we have to deal with in our problem, in order to also have a realistic idea of what are the maximum performance we can achieve in the ideal case.

- **In biological evolution it is possible to think of many phenotypic traits that contribute to the ultimate fitness of an organism (try to enumerate some of these). What (if any) relevance do multi-objective evolutionary algorithms have to biology?** \
Some example of biological phenotypic traits that have an impact on the fitness of an organism include height, wing length, eyesight, and any other characteristic that ultimately give an advantage over the other organisms. In biology, evolution is probably driven by different objectives that can compete with each other, like in a multi-objective EA. For instance, having larger wings may increase the overall stamina and speed of a bird, at the expense of being more easily identifiable by a prey.

## Lab. 05 (Constrained Problems)

### Exercise 1

- **How do your results change from the unconstrained version (from the previous lab)?** \
With respect to the unconstrained solution, the range of the results is much narrower (see image below). In particular, the maximum stopping time (f1) is shorter from (~16 to ~11), and the maximum weight (f0) is lower (from ~2.2 to ~1.5). Moreover, the tradeoff between the two  metrics is less "steep", i.e. it's more difficult to identify an elbow in the trade-off between weight and stopping time w.r.t. the unconstrained version, and therefore it's more difficult to identify the "best" solutions with the best trade-off in the Pareto front.

<div style="text-align:center">
    <img src="img/lab05_es1_1.png" alt="Pareto front analysis" width="300"/>
</div>

- **Do your previous parameters continue to solve the problem?** \
Yes, the parameters used for the unconstrained version (pop_size=20, max_gen=100) obtain better results than the default ones (pop_size=10, max_gen=10).

- **Try to increase the population size and/or the number of generations to see if you can find better solutions.** \
By increasing the parameters values to pop_size=30 and max_gen=500 we obtain a larger choice of good solutions and the Pareto front become more visible. However, the solutions are not particularly better in terms of dominance with the previous ones. 

<div style="text-align:center">
    <img src="img/lab05_es1_2.png" alt="Pareto front analysis" width="300"/>
</div>

### Exercise 2

- **Do you see any difference in the GA’s behavior (and results) when the penalty is enabled or disabled?** \
When using the RosenbrockDisk problem class with penalties, the best fitness value obtain is usually an order of magnitude lower than the best fitness obtained by the version without penalties. However, the version without penalties is unable to find feasible solutions, as opposed to the penalized version. Moreover the solutions are less sparse w.r.t the version with penalties.

- **Try to modify the penalty functions used in the code of each benchmark function, and/or change the main parameters of the GA. Are you able to find the optimum on all the benchmark functions you tested?** \
With RosenbrockDisk, by setting penalty function to `g(x, y) = x^2 + y^2 - 20` (instead of -2), we obtain a best fitness close to the unconstrained version, with a value (0.0004) an order of magnitude smaller than the one with the original penalty function (0.006). The best results are obtained by also changing the gaussian_stdev to 0.1 and the mutation_rate to 0.8, with a final best fitness of 0.0001.

- **Is the GA able to find the optimal solution lying on the unit circle (with the SphereCircle benchmark)?**
With the default values, no: the optimal solution (with a fitness of 2.02) lies outside the unit circle. The solution closest to the unit circle is obtained with pop_size=50 and gaussian_stdev=0.2, with a total penalty of 0.23. However, this solution is still unfeasible. By increasing the max_gen param to 400, we are able to obtain a solution very close to the unit circle, with a fitness of 1.03.

- **By default, the sphere function is defined in a domain [−5.12, 5.12] along each dimension. Try to increase the search space to progressively increasing boundaries. Is the GA still able to explore the feasible region and find the optimum?** \
Yes, even by increasing the search space to [-10, 10] or [-20, 20], the results are exactly the same as the ones obtained with a domain of [−5.12, 5.12].

- **If not, try to think of a way to guide the GA towards the feasible region. How could you change the penalty function to do so?**
I don't think it is possible to change the penalty function, since it is the penalty function that defines the constraint of having a solution in the unit circle.

- **Try to modify the sphere function problem by adding one or more linear/non-linear constraints, and analyze how the optimum changes depending on the presence of constraints.**
By adding a constraint like `x < 1` (that becomes `0 < 1 - x`) and `y < 1`, we are able to obtain solutions that resides very close to the unit circle, i.e. with a fitness of 1.0008 (better then the previous fitness of 1.03). In this case, we use three constraints in total:
```python
f = x**2 + y**2
# Constraints
g1 = x**2 + y**2 - 1
g2 = 1 - x
g3 = 1 - y
# Penalties
if g1 > 0: f = -1
if g2 > 0: f = f - g2
if g3 > 0: f = f - g3
```

### Questions

- **What do you think is the most efficient way to handle constraints in EAs?**
If we consider computational efficiency, the most efficient way of handling constraints in EAs is probably by penalty, since it does not require additional expensive computations than an unconstrained EA and it is easy to implement. We can also use all the existing EA algorithm by simply changing the fitness function.

- **Do you think that the presence of constraints makes the search always more difficult? Can you think of cases in which the constraints could actually make the search easier?**
in general es, they make the search more difficult because they introduce additional factors that add complexity the objective's fitness landscape, therefore potentially reducing the convergency speed. However, if we have a clear idea of the kind of solution we want to obtain, we can exploit the constraints to direct the search process towards the wanted feasible space. In this case the constraints would be only a way to limit the search space, since they would increase/decrease the fitness according to previous knowledge we have about the problem. They would not be something that we need to trade-off with the actual fitness and that slow down the search space.