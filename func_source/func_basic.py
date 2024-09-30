import polars as pl


# ------------------------------------------------------------------------------ #
# Transfer a continuous series into specific number of categories
def continuous_mean_grouping(x: pl.Series, n_group: int, high_to_low_name: list[str] = None) -> pl.Series:
    
    if high_to_low_name is not None and len(high_to_low_name) != n_group:
        raise ValueError("The length of high_to_low_name must be equal to n_group!")
        
    N = n_group    
    m0 = x.min() - 1
    
    if high_to_low_name is None:
        names = [j+1 for j in range(N)]
        y = pl.Series([N] * len(x))
    elif high_to_low_name is not None: 
        names = high_to_low_name
        y = pl.Series([names[-1]] * len(x))
    
    for i in range(N-1):
        m1 = x.filter(x > m0).mean()
        y = y.set(x > m1, names[-i-2])
        m0 = m1

    if high_to_low_name is not None: 
        cate_enum = pl.Enum(names)
        return pl.Series(y, dtype = cate_enum)
    else:
        return y
    
