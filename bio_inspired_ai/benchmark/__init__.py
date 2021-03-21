import sys, os, shutil
import inspect, itertools
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

ROUND_RESULTS = 5

def run_benchmark(run_function, output_path, initial_args, custom_args, problems, combine):
    # Generate folder and delete previous content
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)
    # Run algorithms and save results
    df = pd.DataFrame()

    # Generate params combinations
    if combine:
        keys, values = zip(*custom_args.items())
        params_list = [dict(zip(keys, v)) for v in itertools.product(*values)]
        args_array = [{**initial_args, **args} for args in params_list]
    else: 
        args_array = [{**initial_args, arg: v} for arg, values in custom_args.items() for v in values]

    # Test arguments
    for i, args in enumerate(tqdm(args_array)): 
        result = {}
        
        # Test problems
        for problem in problems:
            # Run function
            args['problem_class'] = problem
            ret = run_function(args, show=False)
            result = {**result, **{f'{k}_{problem.__name__.lower()}': v.round(ROUND_RESULTS) for k, v in ret.items()} }
            plt.tight_layout()
            plt.savefig(f'{output_path}/img{i}_{problem.__name__.lower()}.png', dpi=250)
            plt.close()

        # Remove unwanted keys from the result table and convert to string other variables
        args.pop('fig_title', None)
        for k, v in args.items():
            if inspect.isclass(v): args[k] = v.__name__
            if v is None: args[k] = 'None'
        
        # Add obtained results
        df = df.append({**args, **result}, ignore_index=True)
        df = df[[*args.keys(), *result.keys()]] # Reorder columns
    
    # Save results
    print(df)
    df.to_markdown(f'{output_path}/benchmark.csv', tablefmt='github')
    return df
