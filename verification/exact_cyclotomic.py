#!/usr/bin/env python3
"""Exact known 20-term cubic decomposition in Q[z]/Phi_10(z).

The lower bound is a written proof; this checks a regression and its moment
spaces only. Standard library, explicit rejection, and negative controls.
"""
from fractions import Fraction as Q
from itertools import product
import json

def need(ok, label):
    if not ok:
        raise ValueError(label)

ZERO=(Q(0),)*4
ONE=(Q(1),Q(0),Q(0),Q(0))
Z=(Q(0),Q(1),Q(0),Q(0))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(c,a): return tuple(Q(c)*x for x in a)
def mul(a,b):
    c=[Q(0)]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    for j in range(6,3,-1):
        v=c[j]
        for t,u in enumerate((-1,1,-1,1)): c[j-4+t]+=u*v
    return tuple(c[:4])
def power(a,n):
    need(n>=0,'negative exponent')
    out=ONE
    while n:
        if n&1: out=mul(out,a)
        a=mul(a,a);n//=2
    return out
def inv(a):
    need(a!=ZERO,'zero inverse')
    columns=[mul(a,tuple(Q(i==j) for i in range(4))) for j in range(4)]
    mat=[[columns[j][i] for j in range(4)]+[Q(i==0)] for i in range(4)]
    for j in range(4):
        pivot=next((i for i in range(j,4) if mat[i][j]),None)
        need(pivot is not None,'field inverse singular')
        mat[j],mat[pivot]=mat[pivot],mat[j]
        v=mat[j][j];mat[j]=[x/v for x in mat[j]]
        for i in range(4):
            if i!=j:
                v=mat[i][j];mat[i]=[x-v*y for x,y in zip(mat[i],mat[j])]
    return tuple(mat[i][-1] for i in range(4))

def rank(rows):
    a=[list(row) for row in rows]
    if not a:return 0
    p=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(p,len(a)) if a[i][j]!=ZERO),None)
        if pivot is None:continue
        a[p],a[pivot]=a[pivot],a[p]
        v=inv(a[p][j]);a[p]=[mul(x,v) for x in a[p]]
        for i in range(p+1,len(a)):
            v=a[i][j]
            if v!=ZERO:a[i]=[sub(x,mul(v,y)) for x,y in zip(a[i],a[p])]
        p+=1
        if p==len(a):break
    return p

def total(values):
    out=ZERO
    for v in values:out=add(out,v)
    return out
def mult(values):
    out=ONE
    for v in values:out=mul(out,v)
    return out

def nodes():
    result=[]
    for e2,e3 in product((-1,1),repeat=2):
        parity=0 if e2*e3==1 else 1
        for j in range(parity,10,2):
            t=power(Z,j)
            result.append({'a':[t,scale(e2,t),scale(e3,t)],
                           'alpha':scale(Q(e2*e3,540),power(Z,(-j)%10)),
                           'z':[power(Z,(-j)%10),scale(e2,power(Z,(-j)%10)),
                                scale(e3,power(Z,(-j)%10))],
                           'weight':scale(Q(1,540),power(Z,(8*j)%10))})
    return result

def coefficients(ns):
    choose=(1,3,3,1)
    for a in product(range(4),repeat=3):
        coefficient=total(mul(row['alpha'],mult(power(row['a'][i],a[i]) for i in range(3))) for row in ns)
        coefficient=scale(choose[a[0]]*choose[a[1]]*choose[a[2]],coefficient)
        need(coefficient==(ONE if a==(2,2,2) else ZERO),'coefficient '+str(a))

def evals(ns,exponents):
    return [[mult(power(row['z'][i],e[i]) for i in range(3)) for e in exponents] for row in ns]
def box(a):return list(product(*(range(d+1) for d in a)))
def concat(*matrices):return [sum((list(m[i]) for m in matrices),[]) for i in range(len(matrices[0]))]
def gram(a,b,weights):
    return [[total(mul(weights[i],mul(a[i][j],b[i][k])) for i in range(len(a)))
             for k in range(len(b[0]))] for j in range(len(a[0]))]

def main():
    need(power(Z,5)==neg(ONE) and power(Z,10)==ONE,'cyclotomic arithmetic')
    ns=nodes();need(len(ns)==20,'node count')
    coefficients(ns)
    for e in product(range(4),repeat=3):
        moment=total(mul(row['weight'],mult(power(row['z'][i],e[i]) for i in range(3))) for row in ns)
        need(moment==(scale(Q(1,27),ONE) if e==(1,1,1) else ZERO),'moment '+str(e))
    hilbert={str(a):rank(evals(ns,box(a))) for a in ((1,1,1),(2,1,1),(1,2,2),(2,2,2))}
    need(list(hilbert.values())==[8,12,16,20],'regression Hilbert ranks')
    U=evals(ns,box((1,1,1)))
    W=[evals(ns,[e for e in box((2,2,2)) if e[i]==2 and all(e[j]<=1 for j in range(3) if i!=j)]) for i in range(3)]
    weights=[row['weight'] for row in ns]
    need(rank(gram(U,U,weights))==8,'nondegenerate U')
    for i in range(3):
        need(rank(W[i])==4,'W dimension')
        need(rank(gram(U,W[i],weights))==0,'U-W orthogonality')
        for j in range(i):need(rank(gram(W[i],W[j],weights))==0,'cross W orthogonality')
    pairs=[8-rank(concat(W[i],W[j])) for i in range(3) for j in range(i)]
    S=concat(*W)
    # Kernel of [W1,-W2,0; W1,0,-W3] parametrizes the triple intersection
    # since each Wi evaluation matrix has independent columns.
    triple_matrix=[W[0][i]+[neg(v) for v in W[1][i]]+[ZERO]*4 for i in range(20)]
    triple_matrix += [W[0][i]+[ZERO]*4+[neg(v) for v in W[2][i]] for i in range(20)]
    triple=12-rank(triple_matrix)
    need(pairs==[2,2,2] and triple==1,'intersection ranks')
    controls=[]
    for label,mutate in [('omit one summand',lambda r:r.pop()),
                         ('wrong summand coefficient',lambda r:r[0].__setitem__('alpha',scale(2,r[0]['alpha'])))]:
        altered=nodes();mutate(altered)
        try:coefficients(altered)
        except ValueError as exc:
            need(str(exc).startswith('coefficient '),'wrong control reason')
            controls.append({'label':label,'rejection':str(exc)})
        else:raise ValueError('negative control accepted '+label)
    print(json.dumps({'status':'PASS','field':'Q[z]/(z^4-z^3+z^2-z+1)','summands':20,
                      'coefficients_checked':64,'moments_checked':64,'hilbert_ranks':hilbert,
                      'pair_intersections':pairs,'triple_intersection':triple,'sum_W_dimension':rank(S),
                      'sum_W_Gram_rank':rank(gram(S,S,weights)),'negative_controls':controls},indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,ZeroDivisionError) as exc:
        raise SystemExit('REJECT: '+str(exc))
