import sympy

class UnaryFunction(object):
    def __init__(f):
        x = sympy.symbols('x')
        self.__func = sympy.lambdify(x, f(x))
        self.__diff = simpy.lambdify(x, diff(f(x), x))

    def __call__(self, x):
        return self.__func(x)

    def __diff__(self, index = 0):
        if index == 0: return  self.__diff
        else: raise ValueError("Invalid derivative index for an unary function: ", index)


class BinaryFunction(object):
    def __init__(f):
        x, y = sympy.symols('x, y')
        self.__func = sympy.lambdify((x, y), f(x, y))
        self.__diff0 = sympy.lambdify((x, y), diff(f(x, y), x))
        self.__diff1 = sympy.lambdify((x, y), diff(f(x, y), y))

    def __call__(self, x, y):
        return self.__func(x, y)

    def __diff__(self, index):
        if index == 0: return self.__diff0
        elif index == 1: return self.__diff1
        else: raise ValueError("Invalid derivative index for a binary function: ", index)


def diff(f, index = 0):
    return f.__diff__(index)


cos = UnaryFunction(sympy.cos)
sin = UnaryFunction(sympy.sin)
tan = UnaryFunction(sympy.tan)
sec = UnaryFunction(sympy.sec)
csc = UnaryFunction(sympy.csc)
cot = UnaryFunction(sympy.cot)

acos = UnaryFunction(sympy.acos)
asin = UnaryFunction(sympy.asin)
atan = UnaryFunction(sympy.atan)
asec = UnaryFunction(sympy.asec)
acsc = UnaryFunction(sympy.acsc)
acot = UnaryFunction(sympy.acot)

cosh = UnaryFunction(sympy.cosh)
sinh = UnaryFunction(sympy.sinh)
tanh = UnaryFunction(sympy.tanh)
sech = UnaryFunction(sympy.sech)
csch = UnaryFunction(sympy.csch)
coth = UnaryFunction(sympy.coth)

acosh = UnaryFunction(sympy.acosh)
asinh = UnaryFunction(sympy.asinh)
atanh = UnaryFunction(sympy.atanh)
asech = UnaryFunction(sympy.asech)
acsch = UnaryFunction(sympy.acsch)
acoth = UnaryFunction(sympy.acoth)

sinc = UnaryFunction(sympy.sinc)

exp = UnaryFunction(sympy.exp)
log = UnaryFunction(sympy.log)
sqrt = UnaryFunction(sympy.sqrt)

erf = UnaryFunction(sympy.erf)
erfc = UnaryFunction(sympy.erfc)



add = BinaryFunction(lambda x, y : x+y)
subtract = BinaryFunction(lambda x, y : x-y)
multiply = BinaryFunction(lambda x, y : x*y)
divide = BinaryFunction(lambda x, y : x/y)
pow = BinaryFunction(lambda x, y : x**y)
