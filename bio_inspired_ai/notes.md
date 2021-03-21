# Bio-Inspired Artificial Intelligence - Lab. Notes  

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

- **How do these differences change with different pop. sizes and problem dimensions?** \

### Questions
- **Do the observations you made while varying μ, ρ, and λ confirm or contradict the conclusions you drew last week?** \

- **What are the advantages of self-adaptation in evolutionary computation?** \

- **In what ways might self-adaptation be occurring in biological organisms?** \

- **Compare the different self-adaptation strategies explored in this exercise. In what ways are certain strategies better than others for optimization? In what ways are certain strategies more biologically plausible than others?** \

- **Describe what reasons may contribute to better performance of CMA-ES and what can be the conditions when CMA-ES is not better than a basic ES.** \

