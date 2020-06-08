

from numbers import Real
from numpy import ndarray, array
import specfun as sf



def applyUnary(fun, val):
    if isinstance(val, Real): return fun(val)
    elif isinstance(val, ndarray): return array([applyUnary(fun, x) for x in val])
    elif hasattr(val, '__apply_unary__'): return val.__apply_unary__(fun)
    else: raise ValueError('applyUnary is not defined for type ', type(val))

def applyBinary(fun, val0, val1):
    if isinstance(val0, Real) and isinstance(val1, Real): return fun(val0, val1)
    elif isinstance(val0, np.ndarray) and isinstance(val1, np.ndarray):
        return (np.array([applyBinary(fun, val0[i], val1[i]) for i in range(len(val0))]) if len(val0) == len(val1) else
                raise ValueError('Incompatible array sizes: ', len(val0), len(val1)))
    elif isinstance(val0, np.ndarray) and isinstance(val1, Real): return fun(val0, val1)
    elif isinstance(val0, Real) and isinstance(val1, np.ndarray):
        return np.array([apply
    
    

    
    elif isinstance(val, ndarray): return array([applyUnary(fun, x) for x in val])
    elif hasattr(val, '__apply_unary__'): return val.__apply_unary__(fun)
    else: raise ValueError('applyBinary is not defined for types ', type(val0), type(val1))
    
