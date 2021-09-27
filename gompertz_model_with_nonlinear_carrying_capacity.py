# -*- coding: utf-8 -*-
"""Gompertz model with nonlinear carrying capacity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JtEGQNNGFmbxPxZxde11v38U4uOQhC1l
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from scipy.integrate import odeint
from scipy.optimize import fsolve
from shapely.geometry import LineString
plt.style.use('seaborn-darkgrid')

import statistics as st

from scipy.optimize import curve_fit

import pandas as pd
from numpy.linalg import inv

# %matplotlib inline

from scipy import linalg
from scipy.optimize import minimize
import sympy as sp
from sympy import Sum, var, solve, nsolve
from sympy.core.symbol import symbols
from sympy.solvers.solveset import nonlinsolve
from sympy import Matrix
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt

"""Case 1: g(x) = bx+c"""

#Equilbrium point(s)

b = 0.2
c = 0.1

lhs = lambda x: np.log(x)
rhs = lambda x, b, c: np.log(b*x+c)
t = np.linspace(0.01,20, 1000)

point = c/(1-b)

plt.plot(t,lhs(t), label ='ln(x)')
plt.plot(t,rhs(t,b,c), label ='ln(bx+c)')
plt.plot(point, lhs(point), 'o', label = 'equilibrium point %.3f' %(point))
plt.xlabel('x')
plt.ylabel('function')
plt.legend()
plt.show()

#Solution of Gompertz model

a_0 = 0.5
a_1 = 1
a_2 = 1.5

def f1(x,t,a1):
    dxdt = -a1*x*np.log(x/(b*x+c))
    return dxdt

x_0 = 0.1

x0 = odeint(f1,x_0,t,args=(a_0,))
x1 = odeint(f1,x_0,t,args=(a_1,))
x2 = odeint(f1,x_0,t,args=(a_2,))

# plot results
plt.axhline(y=point, color='k', linestyle='--', label = 'equilibrium')
plt.plot(t,x0, label = 'a=0.5, b=0.2, c=0.1')
plt.plot(t,x1, label = 'a=1, b=0.2, c=0.1')
plt.plot(t,x2, label = 'a=1.5, b=0.2, c=0.1')
plt.xlabel('time, t')
plt.ylabel('tumor size, x')
plt.legend()
plt.show()

"""Case 2: g(x) = bx^2+cx+d"""

#Equilbrium point(s)

b = -0.5
d = 0
c = 2*np.sqrt(b*d)+3

lhs1 = lambda x: np.log(x)
rhs1 = lambda x, b, c, d: np.log(b*x**2+c*x+d)
t = np.linspace(0.01,20, 10000)

point1 = (-(c-1)+np.sqrt((c-1)**2-4*b*d))/(2*b)
point2 = (-(c-1)-np.sqrt((c-1)**2-4*b*d))/(2*b)

plt.plot(t,lhs1(t), label ='ln(x)')
plt.plot(t,rhs1(t,b,c,d), label ='ln(bx^2+cx+d)')
plt.plot(point1, lhs1(point1), 'o', label = 'equilibrium point %.d' %(point1))
plt.plot(point2, lhs1(point2), 'o', label = 'equilibrium point %.3f' %(point2))
plt.xlabel('x')
plt.ylabel('function')
plt.legend()
plt.show()

#Solution of Gompertz model

a_0 = 0.5
a_1 = 1
a_2 = 1.5

def f1(x,t,a1):
    dxdt = -a1*x*np.log(x/(b*x**2+c*x+d))
    return dxdt

x_0 = 0.01

x0 = odeint(f1,x_0,t,args=(a_0,))
x1 = odeint(f1,x_0,t,args=(a_1,))
x2 = odeint(f1,x_0,t,args=(a_2,))

# plot results
plt.axhline(y=point2, color='k', linestyle='--', label = 'equilibrium point 1')
plt.axhline(y=point1, color='r', linestyle='--', label = 'equilibrium point 2')
plt.plot(t,x0, label = 'a= %.1f, b= %.1f, c= %.1f, d = %.1f' %(a_0, b, c, d))
plt.plot(t,x1, label = 'a= %.1f, b= %.1f, c= %.1f, d = %.1f' %(a_1, b, c, d))
plt.plot(t,x2, label = 'a= %.1f, b= %.1f, c= %.1f, d = %.1f' %(a_2, b, c, d))
plt.xlabel('time, t')
plt.ylabel('tumor size, x')
plt.legend(loc='best')
plt.show()

"""Case 3: g(x) = bln(cx)"""

b = -2
c = 0.5


lhs2 = lambda x: x
rhs2 = lambda x, b, c: np.log((c*x)**b)
t = np.linspace(0.1,14, 10000)


f = lambda x: np.log((c*x)**b) -x

i_guess = 0.1
point1 = fsolve(f, i_guess)

plt.plot(t,lhs2(t), label ='x')
plt.plot(t,rhs2(t,b,c), label ='bln(cx)')
plt.plot(point1[0], lhs2(point1[0]), 'o', label = 'equilibrium point %.3f' %(point1[0]))

plt.xlabel('x')
plt.ylabel('function')
plt.legend()
plt.show()

#Solution of Gompertz model

a_0 = 0.5
a_1 = 1
a_2 = 1.5

def f1(x,t,a1):
    dxdt = -a1*x*np.log(x/(np.log((c*x)**b)))
    return dxdt

x_0 = 0.01

x0 = odeint(f1,x_0,t,args=(a_0,))
x1 = odeint(f1,x_0,t,args=(a_1,))
x2 = odeint(f1,x_0,t,args=(a_2,))

# plot results
plt.axhline(y=point1[0], color='k', linestyle='--', label = 'equilibrium')
plt.plot(t,x0, label = 'a= %.1f, b= %.1f, c= %.1f' %(a_0, b, c))
plt.plot(t,x1, label = 'a= %.1f, b= %.1f, c= %.1f' %(a_1, b, c))
plt.plot(t,x2, label = 'a= %.1f, b= %.1f, c= %.1f' %(a_2, b, c))
plt.xlabel('time, t')
plt.ylabel('tumor size, x')
plt.legend()
plt.show()

"""Case 4: g(x) = e^-(bx+c)"""

b = 1
c = 0

lhs = lambda x, b, c: b*x + c
rhs = lambda x: -np.log(x)
t = np.linspace(0.01,20, 1000)

plt.plot(t,lhs(t, b, c), label ='b*x + c')
plt.plot(t,rhs(t), label ='-np.log(x)')
#plt.plot(point, lhs(point), 'o', label = 'equilibrium point %.3f' %(point))
plt.xlabel('x')
plt.ylabel('function')
plt.legend()
plt.show()

b1 = -0.004738
b2 = -0.35
b3 = 0.05
c = 0

lhs = lambda x, b, c: b*x + c
rhs = lambda x: -np.log(x)
t = np.linspace(0.01,5, 1000)

plt.plot(t,lhs(t, b1, c), label ='b = %.3f' %(b1))
plt.plot(t,lhs(t, b2, c), label ='b = %.3f' %(b2))
plt.plot(t,lhs(t, b3, c), label ='b = %.3f' %(b3))
plt.plot(t,rhs(t), label ='-np.log(x)')
#plt.plot(point, lhs(point), 'o', label = 'equilibrium point %.3f' %(point))
plt.xlabel('x')
plt.ylabel('function')
plt.legend()
plt.show()

dfA = pd.read_csv('/content/drive/MyDrive/Projects/BioMath research project/A.csv', header=None) 
dfB = pd.read_csv('/content/drive/MyDrive/Projects/BioMath research project/B.csv', header=None)
dfC = pd.read_csv('/content/drive/MyDrive/Projects/BioMath research project/C.csv', header=None)

dfA.columns = ['Time', 'Volume']
dfB.columns = ['Time', 'Volume']
dfC.columns = ['Time', 'Volume']

display(dfA, dfB, dfC)

x1 = dfA['Time']
y1 = dfA['Volume']
x2 = dfB['Time']
y2 = dfB['Volume']
x3 = dfC['Time']
y3 = dfC['Volume']

x1 = x1.drop([6])
y1 = y1.drop([6])

x1 = np.array(x1)
y1 = np.array(y1)

plt.plot(x1,y1, 'o', label = 'Animal A')

plt.legend()
plt.xlabel('Time (days)')
plt.ylabel('Volume (mm^3)')
plt.show()

der1 = []
for i in range(len(x1)-1):
  der1.append((y1[i+1]-y1[i])/((x1[i+1]-x1[i])*y1[i]))
der1.append(0)

plt.plot(y1,der1,'go')
plt.show()

"""#Newton's method"""

def N(xdata, ydata, iv, tol, max):

  m = len(xdata)

  def fc(x, p):
    return np.log(1/(x**p[0]*np.exp(p[0]*p[1]*x))) 

  def rms(y, yfit):
    return np.sqrt(np.sum((y-yfit)**2)/m)

  a,b = symbols('a b', real = True)

  eq1 = Matrix([sp.Add(*[(sp.log(1/(xdata[i]**a*sp.exp(a*b*xdata[i])))-ydata[i])**2 for i in range(m)])])
  params = Matrix([a, b])

  grad = eq1.jacobian(params)
  
  vector_f = Matrix([grad[0], grad[1]])
  H = vector_f.jacobian(params)

  it = 0
  itlist = [0]
  grad_norm = []

  def fceval(ivn):
    return sum([(np.log(1/(x**ivn[0]*np.exp(ivn[0]*ivn[1]*x)))-h)**2 for x in xdata for h in ydata])


  diff = fceval(iv)
  for i in range(max):
    f = np.array(vector_f.subs({a:iv[0], b:iv[1]})).astype('float').ravel()
    grad_norm.append(np.linalg.norm(f))
    print(diff)
    if diff < tol:
      aprlist = [np.log(1/(x**iv[0]*np.exp(iv[0]*(iv[1]*x)))) for x in xdata]
      print('Convergence was reached at tolerance = %f and %d iterations' %(tol, it))
      print('Solution = {a = %f, b = %f}' %(iv[0], iv[1]))
      print('RMSE is %f' %(rms(y1, fc(xdata,iv))))
      plt.fill_between(xdata, lower(aprlist, ydata,len(xdata)-len(iv)), upper(aprlist, ydata,len(xdata)-len(iv)), color='b', alpha=.1)
      plt.plot(xdata,ydata, 'mo', label = ' Exp data')
      plt.plot(xdata,aprlist, color = 'k', label = 'Fit')
      plt.xlabel('Volume (x)')
      plt.ylabel('1/x dx/dt')
      plt.legend()
      plt.draw()
      print(grad_norm)
      plt.figure() 
      plt.plot(itlist, grad_norm, 'g')
      plt.axhline(y=tol, color='y', linestyle='--', label = 'Tolerance level')
      plt.legend()
      plt.xlabel('Iterations')
      plt.ylabel('2-norm of grad')
      plt.draw() 
      break

    else:
      it += 1
      itlist.append(int(it))
      A = H.subs({a:iv[0], b:iv[1]})
      A = np.array(A).astype('float')
      h = inv(A).dot(-f)
      ivnew = iv + h
      
      diff = abs(fceval(ivnew) - fceval(iv))

      iv = ivnew

      if i == int(max-1):
        aprlist = [np.log(1/(x**iv[0]*np.exp(iv[0]*(iv[1]*x)))) for x in xdata]
        print('Maximum number of %d iterations is reached' %(it))
        print('Parameters = {a = %f, b = %f}' %(iv[0], iv[1]))
        plt.plot(xdata,ydata, 'mo', label = ' Exp data')
        plt.plot(xdata,aprlist, color = 'k', label = 'Approximation')
        plt.xlabel('Volume (x)')
        plt.ylabel('1/x dx/dt')
        plt.legend()
        plt.draw()
        print(grad_norm)
        plt.figure() 
        plt.plot(itlist[:-1], grad_norm, color = 'g')
        plt.axhline(y=tol, color='y', linestyle='--', label = 'Tolerance level')
        plt.legend()
        plt.xlabel('Iterations')
        plt.ylabel('2-norm of grad')
        plt.draw() 
        break
  a = iv[0]
  b = iv[1]

  def f1(x,t,a1,b):
      dxdt = -a1*x*np.log(x*np.exp(b*x))
      return dxdt

  x_0 = y1[0]
  t = x1
  x0 = odeint(f1,x_0,t,args=(a, b))

  # plot results
  #plt.axhline(y=, color='k', linestyle='--', label = 'equilibrium')
  plt.figure()
  #plt.fill_between(xdata, lower(x0, ydata,len(xdata)-len(iv)), upper(x0, ydata,len(xdata)-len(iv)), color='b', alpha=.1)
  plt.plot(t,x0, label = 'r= %f, b= %f' %(a, b))
  plt.plot(x1, y1, 's', label = 'Animal A')
  plt.xlabel('time, t')
  plt.ylabel('tumor size, x')
  plt.legend(loc = 'best')
  plt.draw() 
  plt.show()

ig = np.array([0.2, -0.001])
N(xdata = y1, ydata = der1, iv = ig, tol = 1E-15, max = 100)

def CI(est, fit, x, n, m):
  return est - 2.306*np.sqrt(sum([(i-j)**2/n for i in x for j in fit])*m), est + 2.306*np.sqrt(sum([(i-j)**2/n for i in x for j in fit])*m)

def AIC(fit, x):
  return len(x)*np.log(sum([(i-j)**2 for i in x for j in fit])/len(x)) - len(x)*np.log(len(x)) + 4

def Rsquared(fit, x):
  return 1 - (sum([(i-j)**2 for i in x for j in fit])/sum([(k - st.mean(x))**2 for k in x]))

def adjRsquared(fit, x):
  return 1 - (1 - Rsquared(fit, x))*(len(x)-1)/(len(x)-2)

n = len(x1)
t = x1

K = y1[-1]
xnode = y1[0]

def rms(y, yfit):
    return np.sqrt(np.sum((y-yfit)**2)/(n-2))

def fitfunc(t, r, b):
  def myode(y, t):
    return -r*y*np.log(y*np.exp(b*y))

  y0 = y1[0]
  ysol = odeint(myode, y0, t)
  return ysol[:,0]

def explicitf(t, r):
  return K**(1-np.exp(-r*t))*xnode**(np.exp(-r*t))

p0 = -0.05, -0.007
p0lin = 0.01

fit1, cov = curve_fit(fitfunc, t, y1, p0, method= 'lm')
yfit = fitfunc(x1, *fit1)
print(fit1)
a1,b1 = CI(fit1[0], y1, yfit, len(x1)-2, cov[0][0])
a2,b2 = CI(fit1[1], y1, yfit, len(x1)-2, cov[1][1])
print('CI for r is (%f, %f)' %(a1,b1))
print('CI for b is (%f, %f)' %(a2,b2))
tspace = np.linspace(t[0], t[len(x1)-1])
fit = fitfunc(tspace, *fit1)
fit11 = fitfunc(x1, *fit1)

fitw, covw = curve_fit(explicitf, t, y1, p0lin)
yfitw = explicitf(x1, *fitw)
print(fitw)
a1,b1 = CI(fitw[0], y1, yfitw, len(x1)-2, covw[0][0])
print('CI for r is (%.10f, %.10f)' %(a1,b1))
fitw1 = explicitf(tspace, *fitw)

fitw11 = explicitf(x1, *fitw)

plt.plot(t, y1, 'mo', label='data')
plt.plot(tspace, fit, 'g-', label='exponential K (AIC: %.3f)' %(AIC(fitw11, y1)))
plt.plot(tspace, fitw1, label='constant K (AIC: %.3f)' %(AIC(fit11, y1)))
plt.ylabel('Tumor size, x')
plt.xlabel('Time, t')
plt.legend(loc='best')
plt.show()

n = len(x1)
t = x1
y1log = np.log10(y1)

K = y1[-1]
xnode = y1[0]

def rms(y, yfit):
    return np.sqrt(np.sum((y-yfit)**2)/(n-2))

def fitfunc(t, r, b):
  def myode(y, t):
    return -r*np.log(10**y*np.exp(b*10**y))/np.log(10)

  y0 = y1log[0]
  ysol = odeint(myode, y0, t)
  return ysol[:,0]


def explicitf(t, r):
  return np.log10(K**(1-np.exp(-r*t))*xnode**(np.exp(-r*t)))

p0 = -0.05, -0.02
p0lin = 0
fit1, cov = curve_fit(fitfunc, t, y1log, p0)
yfit = fitfunc(x1, *fit1)
print(fit1)
a1,b1 = CI(fit1[0], y1, yfit, len(x1)-2, cov[0][0])
a2,b2 = CI(fit1[1], y1, yfit, len(x1)-2, cov[1][1])
print('CI for r is (%f, %f)' %(a1,b1))
print('CI for b is (%f, %f)' %(a2,b2))
tspace = np.linspace(t[0], t[len(x1)-1])
fit = fitfunc(tspace, *fit1)

fitw, covw = curve_fit(explicitf, t, y1log, p0lin)
yfitw = explicitf(x1, *fitw)
print(fitw)
a1,b1 = CI(fitw[0], y1, yfitw, len(x1)-2, covw[0][0])
print('CI for r is (%f, %f)' %(a1,b1))
fitw = explicitf(tspace, *fitw)

plt.plot(t, y1log, 'mo', label='data')
plt.plot(tspace, fit, 'g-', label='exponential K (AIC: %.3f)' %(AIC(yfitw, y1log)))
plt.plot(tspace, fitw, label='constant K (AIC: %.3f)' %(AIC(yfit, y1log)))
plt.ylabel('Transformed tumor size')
plt.xlabel('Time, t')
plt.legend(loc='best')
plt.show()
