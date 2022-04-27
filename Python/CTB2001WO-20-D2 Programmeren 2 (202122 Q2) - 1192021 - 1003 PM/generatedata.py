import numpy as np

def hours_programming(houses = 4, persons = 18, weeks = 12):
    """Returns a 3-D array in the shape (houses, persons, weeks)
    
    Example:
    >>> house_data(houses=2, persons=3, weeks=4):
    array([[[ 6., 10.,  6.,  9.],
            [10.,  8.,  7.,  5.],
            [ 1.,  2.,  3.,  1.]],

           [[ 4.,  2.,  6.,  3.],
            [ 3.,  8., 10.,  9.],
            [ 3.,  4.,  3.,  3.]]])
    """
    np.random.seed(124)
    hours = np.zeros((houses, persons, weeks))
    for i in range(np.shape(hours)[0]):
        for pers in range(np.shape(hours)[1]):
            start = np.random.randint(2, 10)
            for week in range(np.shape(hours)[2]):
                std = np.random.randint(0, 4)
                hours[i, pers,week] = start + std + np.random.randint(-3, 3)
                if hours[i, pers, week] < 0:
                    hours[i, pers, week] = 0
    return hours