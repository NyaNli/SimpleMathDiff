import math as _math

# 基础定义
class _BaseMathItem:
    __ops = {
        'add': None,
        'sub': None,
        'mul': None,
        'div': None,
        'pow': None,
        'neg': None,
        'convert': None
    }

    @staticmethod
    def regOperate(op, func):
        if op in _BaseMathItem.__ops:
            _BaseMathItem.__ops[op] = func
        else:
            raise Exception('No Such Operate.')

    @staticmethod
    def prepareParam(args):
        if _BaseMathItem.__ops['convert'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['convert'](args)

    def __add__(self,rhs):
        if _BaseMathItem.__ops['add'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['add'](self, rhs)
    def __radd__(self,lhs):
        if _BaseMathItem.__ops['add'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['add'](lhs, self)

    def __sub__(self,rhs):
        if _BaseMathItem.__ops['sub'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['sub'](self, rhs)
    def __rsub__(self,lhs):
        if _BaseMathItem.__ops['sub'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['sub'](lhs, self)

    def __mul__(self,rhs):
        if _BaseMathItem.__ops['mul'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['mul'](self, rhs)
    def __rmul__(self,lhs):
        if _BaseMathItem.__ops['mul'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['mul'](lhs, self)

    def __truediv__(self,rhs):
        if _BaseMathItem.__ops['div'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['div'](self, rhs)
    def __rtruediv__(self,lhs):
        if _BaseMathItem.__ops['div'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['div'](lhs, self)

    def __pow__(self,rhs):
        if _BaseMathItem.__ops['pow'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['pow'](self, rhs)
    def __rpow__(self,lhs):
        if _BaseMathItem.__ops['pow'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['pow'](lhs, self)

    def __neg__(self):
        if _BaseMathItem.__ops['neg'] is None:
            raise Exception('Please register the function before call it.')
        else:
            return _BaseMathItem.__ops['neg'](self)

    def __init__(self):
        raise NotImplementedError

    # 求导
    def _Diff(self, dx):
        raise NotImplementedError

    def Diff(self, dx):
        return _BaseMathItem.prepareParam(self._Diff(dx)._Calc()) # 返回_BaseMathItem

    # 化简或求值
    def _Calc(self, calcVal=False):
        raise NotImplementedError

    def Calc(self, calcVal=False):
        return _BaseMathItem.prepareParam(self._Calc(calcVal)) # 返回_BaseMathItem

    def __repr__(self):
        raise NotImplementedError

    def __float__(self):
        raise NotImplementedError


# 运算符重载等（写外面是因为直接写父类调用子类总有种 父 慈 子 孝 的感觉）
def _doAdd(a, b):
    return MathCalc(a, False, b)

def _doSub(a, b):
    return MathCalc(a, False, -b)
    
def _doMul(a, b):
    return MathCalc(a, True, b)

def _doDiv(a, b):
    return MathCalc(a, True, Pow(b, -1))

def _doPow(a, b):
    return Pow(a, b) # 这是什么Power！
    
def _doNeg(a):
    return MathCalc(-1, True, a)

def __doConv(arg):
    if not isinstance(arg, _BaseMathItem):
        return MathNum(arg)
    else:
        return arg

def _doConvert(args):
    if type(args) is not tuple:
        if not isinstance(args, _BaseMathItem):
            return MathNum(args)
        else:
            return args
    rtn = ()
    for i in args:
        if not isinstance(i, _BaseMathItem):
            rtn += (MathNum(i),)
        else:
            rtn += (i,)
    return rtn

_BaseMathItem.regOperate('add', _doAdd)
_BaseMathItem.regOperate('sub', _doSub)
_BaseMathItem.regOperate('mul', _doMul)
_BaseMathItem.regOperate('div', _doDiv)
_BaseMathItem.regOperate('pow', _doPow)
_BaseMathItem.regOperate('neg', _doNeg)
_BaseMathItem.regOperate('convert', _doConvert)

# 常数
class MathNum(_BaseMathItem):
    def __init__(self, num):
        if isinstance(num, _BaseMathItem):
            raise TypeError('MathNum only accept a Number parameter.')
        self.__num = float(num)

    def _Diff(self, dx):
        return MathNum(0)

    def _Calc(self, calcVal=False):
        return self.__num

    def __repr__(self):
        if self.__num == _math.e:
            return 'e'
        elif self.__num == _math.pi:
            return 'π'
        else:
            return str(self.__num)

    def __float__(self):
        return self.__num

E = MathNum(_math.e)
PI = MathNum(_math.pi)

# 未知数（可以是u=f(x)这种玩法的未知数）
class UnknownNum(_BaseMathItem):
    def __init__(self, name):
        self.__name = name
        self.__expr = None

    def setExpr(self, expr):
        self.__expr = _BaseMathItem.prepareParam(expr)
    
    def clear(self):
        self.__expr = None

    def _Diff(self, dx):
        if self.__expr is None:
            if self == dx:
                return MathNum(1)
            else:
                return MathNum(0)
        else:
            return self.__expr._Diff(dx)

    def _Calc(self, calcVal=False):
        if self.__expr is None:
            return self
        elif type(self.__expr) is MathNum and not calcVal:
            return self
        else:
            return self.__expr._Calc(calcVal)
            # if type(val) is str:
            #     return '[%s]' % val
            # else:
            #     return val

    def __repr__(self):
        return '[%s]' % self.__name

    def __float__(self):
        if self.__expr is None:
            raise ValueError('Unknown number %s has no value.' % self.__name)
        else:
            return float(self.__expr)

# E = UnknownNum('e')
# E.setExpr(_math.e)
# PI = UnknownNum('π')
# PI.setExpr(_math.pi)

# 基础运算
class MathCalc(_BaseMathItem):
    def __init__(self, a, isMul, b):
        self.__a, self.__b = _BaseMathItem.prepareParam((a,b))
        self.__isMul = isMul

    def _Diff(self, dx):
        if self.__isMul:
            return self.__a._Diff(dx) * self.__b + self.__a * self.__b._Diff(dx)
        else:
            return self.__a._Diff(dx) + self.__b._Diff(dx)

    def _Calc(self, calcVal=False):
        valA = self.__a._Calc(calcVal)
        valB = self.__b._Calc(calcVal)
        # doPrint = type(valA) is str or type(valB) is str
        if self.__isMul:
            if valA == 0 or valB == 0:
                return 0
            elif valA == 1:
                return valB
            elif valB == 1:
                return valA
            elif not calcVal and (valA == _math.e or valB == _math.e or valA == _math.pi or valB == _math.pi):
                return MathCalc(valA, self.__isMul, valB)
            else:
                return valA * valB
            # if doPrint:
            #     if type(self.__a) is MathCalc and not self.__a.__isMul:
            #         valA = '(%s)' % str(valA)
            #     if type(self.__b) is MathCalc and not self.__b.__isMul:
            #         valB = '(%s)' % str(valB)
            #     return '%s * %s' % (str(valA), str(valB))
            # else:
            #     return valA * valB
        else:
            if valA == 0:
                return valB
            elif valB == 0:
                return valA
            elif not calcVal and (valA == _math.e or valB == _math.e or valA == _math.pi or valB == _math.pi):
                return MathCalc(valA, self.__isMul, valB)
            else:
                return valA + valB
            # if doPrint:
            #     if valA == 0: # 另一个必为str
            #         return valB
            #     elif valB == 0:
            #         return valA
            #     return '%s + %s' % (str(valA), str(valB))
            # else:
            #     return valA + valB

    def __repr__(self):
        valA = str(self.__a)
        valB = str(self.__b)
        if self.__isMul:
            # if type(self.__a) is MathNum and self.__a._Calc() == 1: # 处理减法字符串后就有可能走这里了
            #     return valB
            # if type(self.__b) is MathNum and self.__b._Calc() == 1:
            #     return valA

            if type(self.__a) is MathCalc and not self.__a.__isMul:
                valA = '(%s)' % valA
            if type(self.__b) is MathCalc and not self.__b.__isMul:
                valB = '(%s)' % valB

            # if valB[:4] == '1 / ': # 由Pow转换的除法字符串
            #     return '%s%s' % (valA, valB[1:])
            # else:
            return '%s * %s' % (valA, valB)
        else:
            # if type(self.__b) is MathCalc and self.__b.__isMul:
            #     if type(self.__b.__a) is MathNum and self.__b.__a._Calc() < 0:
            #         return '%s - %s' % (valA, str((-1 * self.__b.__a)._Calc() * self.__b.__b))
            #     elif type(self.__b.__b) is MathNum and self.__b.__b._Calc() < 0:
            #         return '%s - %s' % (valA, str((-1 * self.__b.__b)._Calc() * self.__b.__a))
            #     else:
            #         return '%s + %s' % (valA, valB)
            return '%s + %s' % (valA, valB)

    def __float__(self):
        valA = float(self.__a)
        valB = float(self.__b)
        if self.__isMul:
            return valA * valB
        else:
            return valA + valB

# 各种其他基础运算
class Pow(_BaseMathItem):
    def __init__(self, x, y):
        self.__x, self.__y = _BaseMathItem.prepareParam((x,y))

    def _Diff(self, dx):
        # if type(self.__x) is MathNum and type(self.__y) is MathNum:
        #     return MathNum(0)
        # elif type(self.__x) is not MathNum and type(self.__y) is MathNum:
        #     return self.__y * Pow(self.__x, self.__y - 1)
        # elif type(self.__x) is MathNum and type(self.__y) is not MathNum:
        #     return self.__y._Diff(dx) * Pow(self.__x, self.__y) * Log(_math.e, self.__x)
        # else:
        #     return Pow(_math.e, self.__y * Log(_math.e, self.__x))._Diff(dx)
        return self * (self.__y * Log(_math.e, self.__x))._Diff(dx)

    def _Calc(self, calcVal=False):
        valA = self.__x._Calc(calcVal)
        valB = self.__y._Calc(calcVal)
        # doPrint = type(valA) is str or type(valB) is str
        if valA == 0:
            return 0
        elif valB == 0:
            return 1
        elif valA == 1:
            return 1
        elif valB == 1:
            return valA
        elif not isinstance(valA, _BaseMathItem) and not isinstance(valB, _BaseMathItem):
            return pow(valA, valB)
        else:
            return Pow(valA, valB)
        # if doPrint:
        #     return 'pow(%s, %s)' % (str(valA), str(valB))
        # else:
        #     return pow(valA, valB)

    def __repr__(self):
        # if type(self.__y) is MathNum:
        #     val = self.__y._Calc()
        #     # if val < 0:
        #     #     return '1 / %s' % str(Pow(self.__x, -1 * val))
        #     if val == 0:
        #         return '1'
        #     elif val == 1:
        #         if type(self.__x) is MathCalc:
        #             return '(%s)' % str(self.__x)
        #         else:
        #             return str(self.__x)
        #     else:
        #         return 'pow(%s, %s)' % (str(self.__x), str(val))
        # else:
        return 'pow(%s, %s)' % (str(self.__x), str(self.__y))

    def __float__(self):
        return pow(float(self.__x), float(self.__y))

def Sqrt(x):
    return Pow(x, 0.5)

class Log(_BaseMathItem):
    def __init__(self, base, x):
        self.__base, self.__x = _BaseMathItem.prepareParam((base,x))

    def _Diff(self, dx):
        if type(self.__base) is not MathNum:
            return (Ln(self.__x) / Ln(self.__base))._Diff(dx)
        else:
            return Pow(self.__x * Ln(self.__base), -1) * self.__x._Diff(dx)

    def _Calc(self, calcVal=False):
        valA = self.__base._Calc(calcVal)
        valB = self.__x._Calc(calcVal)
        if not isinstance(valA, _BaseMathItem) and not isinstance(valB, _BaseMathItem) and calcVal:
            return _math.log(valB, valA)
        elif valA == 0:
            raise ValueError('The base of Log cannot be zero.')
        elif valB == 1:
            return 0
        elif valA == valB:
            return 1
        else:
            return Log(valA, valB)

    def __repr__(self):
        if type(self.__base) is MathNum:
            base = self.__base._Calc(False)
            if base == _math.e: # 怎么看都不靠谱的判断条件
                return 'ln(%s)' % str(self.__x)
            elif base == 2:
                return 'log2(%s)' % str(self.__x)
            elif base == 10:
                return 'log10(%s)' % str(self.__x)
            else:
                return 'log{%s}(%s)' % (str(base), str(self.__x))
        else:
            return 'log{%s}(%s)' % (str(self.__base), str(self.__x))

    def __float__(self):
        return _math.log(float(self.__x), float(self.__base))

def Ln(x):
    return Log(_math.e, x)

def Log2(x):
    return Log(2, x)

def Log10(x):
    return Log(10, x)

class Sin(_BaseMathItem):
    def __init__(self, x):
        self.__x = _BaseMathItem.prepareParam(x)

    def _Diff(self, dx):
        return Cos(self.__x) * self.__x.Diff(dx)

    def _Calc(self, calcVal=False):
        val = self.__x._Calc(calcVal)
        if not isinstance(val, _BaseMathItem) and calcVal:
            return _math.sin(val)
        else:
            return Sin(val)

    def __repr__(self):
        return 'sin(%s)' % str(self.__x)

    def __float__(self):
        return _math.sin(float(self.__x))

class Cos(_BaseMathItem):
    def __init__(self, x):
        self.__x = _BaseMathItem.prepareParam(x)

    def _Diff(self, dx):
        return -Sin(self.__x) * self.__x.Diff(dx)

    def _Calc(self, calcVal=False):
        val = self.__x._Calc(calcVal)
        if not isinstance(val, _BaseMathItem) and calcVal:
            return _math.cos(val)
        else:
            return Cos(val)

    def __repr__(self):
        return 'cos(%s)' % str(self.__x)

    def __float__(self):
        return _math.cos(float(self.__x))

class Tan(_BaseMathItem):
    def __init__(self, x):
        self.__x = _BaseMathItem.prepareParam(x)

    def _Diff(self, dx):
        return 1 / Pow(Cos(self.__x), 2) * self.__x.Diff(dx)

    def _Calc(self, calcVal=False):
        val = self.__x._Calc(calcVal)
        if not isinstance(val, _BaseMathItem) and calcVal:
            return _math.tan(val)
        else:
            return Tan(val)

    def __repr__(self):
        return 'tan(%s)' % str(self.__x)

    def __float__(self):
        return _math.tan(float(self.__x))

def Cot(x):
    return 1 / Tan(x)

def Sec(x):
    return 1 / Cos(x)

def Csc(x):
    return 1 / Sin(x)
    
class ASin(_BaseMathItem):
    def __init__(self, x):
        self.__x = _BaseMathItem.prepareParam(x)

    def _Diff(self, dx):
        return 1 / Sqrt(1 - self.__x**2) * self.__x.Diff(dx)

    def _Calc(self, calcVal=False):
        val = self.__x._Calc(calcVal)
        if not isinstance(val, _BaseMathItem) and calcVal:
            return _math.asin(val)
        else:
            return ASin(val)

    def __repr__(self):
        return 'arcsin(%s)' % str(self.__x)

    def __float__(self):
        return _math.asin(float(self.__x))
    
class ACos(_BaseMathItem):
    def __init__(self, x):
        self.__x = _BaseMathItem.prepareParam(x)

    def _Diff(self, dx):
        return -1 / Sqrt(1 - self.__x**2) * self.__x.Diff(dx)

    def _Calc(self, calcVal=False):
        val = self.__x._Calc(calcVal)
        if not isinstance(val, _BaseMathItem) and calcVal:
            return _math.acos(val)
        else:
            return ACos(val)

    def __repr__(self):
        return 'arccos(%s)' % str(self.__x)

    def __float__(self):
        return _math.acos(float(self.__x))
    
class ATan(_BaseMathItem):
    def __init__(self, x):
        self.__x = _BaseMathItem.prepareParam(x)

    def _Diff(self, dx):
        return 1 / (1 + self.__x**2) * self.__x.Diff(dx)

    def _Calc(self, calcVal=False):
        val = self.__x._Calc(calcVal)
        if not isinstance(val, _BaseMathItem) and calcVal:
            return _math.atan(val)
        else:
            return ATan(val)

    def __repr__(self):
        return 'arctan(%s)' % str(self.__x)

    def __float__(self):
        return _math.asin(float(self.__x))

def ACot(x):
    return ATan(1 / x)

def ASec(x):
    return ACos(1 / x)

def ACsc(x):
    return ASin(1 / x)

if __name__ == "__main__":
    raise Exception('Unable to execute a module.')

# 代码结构可能要优化
# 内存泄漏肯定一堆一堆的，随着Calc与Diff执行次数逐渐翻倍balabala
# 不保证结果正确（笑）