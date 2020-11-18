import numpy as np

def _gen_break_points_(n0, num_seg, overlap = 0):
    """
    Generates the break point indices to split a 1-d array of size n0 into 
    equispaced (and overlapping) segments of equal length.
    """
      
    # gauge approximate difference
    dif = np.ceil(n0 / (num_seg - 1))
    
    # starting break points for each axis segment
    a0 = np.round(np.linspace(0, n0 - dif - overlap, num_seg - 1))
    
    # return complete set of start-end break points for each axis segment
    return list(zip(a0[:-1], a0[:-1] + dif + overlap)) + \
        [(n0 - dif - overlap, n0)]
    