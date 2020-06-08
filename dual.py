

from collections import namedtuple

import specfun as sf



DualBase = namedtuple('Dual', ['re', 'du'])
class Dual(DualBase):
    def __apply_unary__(self, f):
        return Dual(
            f(re(self)),
            du(self)*diff(f)(re(self)))

    def __apply_binary__(self, f, other):
        return Dual(
            f(re(self), re(other)),
            du(self)*diff(f, 0)(re(self), re(other))+
            du(other)*diff(f, 1)(re(self), re(other)))

    def __rapply_binary__(self, f, other):
        return Dual(
            f(re(other), re(self)),
            du(other)*diff(f, 0)(re(other), re(self))+
            du(self)*diff(f, 1)(re(other), re(self)))

    def __add__(self, other):
        return applyBinary(sf.add, self, other)

    def __radd__(self, other):
        return applyBinary(sf.add, other, self)

    def __sub__(self, other):
        return applyBinary(sf.subtract, self, other)

    def __rsub__(self, other):
        return applyBinary(sf.subtract, other, self)

    def __mul__(self, other):
        return applyBinary(sf.multiply, self, other)

    def __rmul__(self, other):
        return applyBinary(sf.multiply, other, self)

    def __truediv__(self, other):
        return applyBinary(sf.divide, self, other)

    def __rtruediv__(self, other):
        return applyBinary(sf.divide, other, self)

    def __pow__(self, other):
        return applyBinary(sf.pow, self, other)

    def __rpow__(self, other):
        return applyBinary(sf.pow, other, self)
            
    
        
            
            
    
