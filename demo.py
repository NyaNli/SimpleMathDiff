from simplemathdiff import *

x = UnknownNum('x')

fx = x*Ln(x)
print('f(x)=' + str(fx))
print('f\'(x)=' + str(fx.Diff(x)))
x.setExpr(E)
print('f(e)=' + str(fx.Calc(True)))
x.clear()
print()

shx = (E**x-E**-x)/2
print('shx=' + str(shx))
print('shx\'=' + str(shx.Diff(x)))
print()

chx = (E**x+E**-x)/2
print('chx=' + str(chx))
print('chx\'=' + str(chx.Diff(x)))
print()

y = UnknownNum('y')
gz = x**2*Sin(x*y)
print('g(x,y)=' + str(gz))
print('gx\'(x,y)=' + str(gz.Diff(x)))
print('gy\'(x,y)=' + str(gz.Diff(y)))
x.setExpr(1)
g1y = gz.Calc(True)
print('g(1,y)=' + str(g1y))