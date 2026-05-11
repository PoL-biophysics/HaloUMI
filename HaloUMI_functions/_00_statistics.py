import numpy as np

def statistics(values, sigma_range):

    if len(values) == 0:
        return 0, 0, 0, 0
    mean = np.mean(values)
    stdev = np.std(values)
    lower_bound = mean - (int(sigma_range) * stdev)
    upper_bound = mean + (int(sigma_range) * stdev)
        
    return mean, stdev, lower_bound, upper_bound