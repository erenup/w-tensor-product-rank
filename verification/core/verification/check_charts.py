#!/usr/bin/env python3
"""Exact regressions for the generic-chart proof; not an all-parameter proof."""
import copy
from fractions import Fraction as Q
from itertools import product
from math import comb
import json
import sys
sys.dont_write_bytecode=True
import exact_cyclotomic as e

def rational_rank(matrix):
    rows=[[Q(x) for x in row] for row in matrix]
    p=0
    for j in range(len(rows[0]) if rows else 0):
        pivot=next((i for i in range(p,len(rows)) if rows[i][j]),None)
        if pivot is None:continue
        rows[p],rows[pivot]=rows[pivot],rows[p]
        v=rows[p][j];rows[p]=[x/v for x in rows[p]]
        for i in range(p+1,len(rows)):
            v=rows[i][j];rows[i]=[x-v*y for x,y in zip(rows[i],rows[p])]
        p+=1
        if p==len(rows):break
    return p

def univariate_cases():
    results=[]
    for d in range(2,10):
        z=list(range(1,d+1))
        w=[Q((-1)**(j-1)*comb(d,j),j) for j in z]
        gamma=sum(Q(1,j) for j in z)
        moments=[sum(wi*zi**s for zi,wi in zip(z,w)) for s in range(d+1)]
        e.need(moments==[gamma,Q(1)]+[Q(0)]*(d-1),'univariate moment identity')
        c=Q(2)
        H=sum(wi*Q(zi**(d+1),1+c*zi) for zi,wi in zip(z,w))
        e.need(H!=0,'univariate anti-diagonal block')
        if d>=3:
            G=[[sum(wi*zi**(s+t)*(1+c*zi)**(d-s-t) for zi,wi in zip(z,w))
                for t in range(2,d)] for s in range(2,d)]
            e.need(all(G[s-2][t-2]==0 for s in range(2,d) for t in range(2,d) if s+t<=d),
                   'anti-triangular zeros')
            e.need(all(G[s-2][t-2]==H for s in range(2,d) for t in range(2,d) if s+t==d+1),
                   'anti-diagonal identity')
            e.need(rational_rank(G)==d-2,'univariate block rank')
        results.append({'d':d,'gamma':str(gamma),'H_at_2':str(H),'block_rank':d-2})
    return results

def cubic_chart(chart, corrupt_weight=False):
    rows=e.nodes()
    if corrupt_weight:rows[0]['alpha']=e.scale(2,rows[0]['alpha'])
    U=[];W=[[],[],[]];weights=[]
    for row in rows:
        a=row['a'];h=[e.add(a[j],e.scale(chart[j],e.ONE)) for j in range(3)]
        e.need(all(v!=e.ZERO for v in h),'chart pole')
        # Multiply every basis vector by product(h_j^2), and divide its
        # pairing weight by the square of this common multiplier.
        weights.append(e.mul(row['alpha'],e.inv(e.mult(h))))
        U.append([e.mult(h+[a[j] if eps[j] else e.ONE for j in range(3)])
                  for eps in product((0,1),repeat=3)])
        for i in range(3):
            js=[j for j in range(3) if j!=i]
            W[i].append([e.mult([h[j] for j in js]+[a[j] if bit else e.ONE for j,bit in zip(js,eps)])
                         for eps in product((0,1),repeat=2)])
    e.need(e.rank(e.gram(U,U,weights))==8,'U rank')
    for i in range(3):
        e.need(e.rank(e.gram(U,W[i],weights))==0,'U-W orthogonality')
        for j in range(i):
            e.need(e.rank(e.gram(W[i],W[j],weights))==0,'W-W orthogonality')
    block_ranks=[e.rank(e.gram(w,w,weights)) for w in W]
    e.need(block_ranks==[4,4,4],'chart block nondegeneracy')
    all_vectors=e.concat(U,*W)
    e.need(e.rank(e.gram(all_vectors,all_vectors,weights))==20,'full Gram rank')
    return {'chart':chart,'U_rank':8,'V_Gram_ranks':block_ranks,'full_Gram_rank':20}

def main():
    cases=univariate_cases()
    chart=cubic_chart((2,3,4))
    controls=[]
    for label,c,bad,expected in [
        ('change one upper-decomposition coefficient',(2,3,4),True,'U-W orthogonality'),
        ('choose a chart with a pole',(1,3,4),False,'chart pole'),
        ('incorrectly presume every chart is good',(0,0,0),False,'chart block nondegeneracy')]:
        try:cubic_chart(c,bad)
        except ValueError as exc:
            e.need(str(exc)==expected,'unexpected rejection: '+label+': '+str(exc))
            controls.append({'label':label,'rejection':str(exc)})
        else:raise ValueError('control accepted '+label)
    print(json.dumps({'status':'PASS','univariate':cases,'cubic_triple':chart,'controls':controls,
                     'scope':'finite exact regressions only; universal lower bound is PROOF.md'},indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,ZeroDivisionError) as exc:
        raise SystemExit('REJECT: '+str(exc))
