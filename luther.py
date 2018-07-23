import numpy as np
import pandas as pd
import os


def get_polynomial_features(degree, x_values):
    return PolynomialFeatures(degree=degree).fit_transform(x_values)


def MSE(a,b):
    try:
        a=a.values
    except(AttributeError):
        pass
    try:
        b=b.values
    except(AttributeError):
        pass
    try:
        res=(sum([(a[i]-b[i])**2 for i in range(len(a))])/len(a))[0]
        return res
    except:
        return (sum([(a[i]-b[i])**2 for i in range(len(a))])/len(a))



def R2(a,b):
    try:
        a=a.values
    except(AttributeError):
        pass
    try:
        b=b.values
    except(AttributeError):
        pass
    mean_pred=[np.mean(b) for i in range(len(b))]
    return 1-MSE(a,b)/MSE(mean_pred,b)


def make_vals(a, n):
    a=sorted(a)
    big=max(a)
    small=min(a)
    spacing=np.linspace(small,big,n)
    vals=[]
    N=len(a)
    for i in spacing:
        vals.append(len([x for x in a if x<i])/N)
    return [vals, small, big, n]


al=[10**(float(i)/10) for i in np.arange(-100,10,1)]
def get_model_stats(X_train,y_train,model,max_degree=7,cv=4,alphas=al):
    results=[]
    for deg in range(1,max_degree+1):
        pipeline=make_pipeline(StandardScaler(),PolynomialFeatures(deg),model)
        #pipeline=make_pipeline(PolynomialFeatures(deg),model)
        fit=pipeline.fit(X_train, y_train)
        y_predict=fit.predict(X_train)
        naive_score=fit.score(X_train,y_train)
        scores = cross_val_score(fit, X_train, y_train, cv=cv, scoring='mean_squared_error')
        cross_val=np.mean(scores)
        features=X_train.shape[1]-1
        mse_adj=R2_adj(y_predict,y_train,features)
        results.append([deg,naive_score,cross_val,mse_adj])
        print("Degree{}Naive Score{} CV {} Adj R2{}".format(deg, round(naive_score,3),\
        round(cross_val,2), round(mse_adj,3)))
    return results






def make_cdf(valset,y):
    big=valset[2]
    small=valset[1]
    spacing=np.linspace(small,big,valset[3])

    if (y<small) or y==small:
        return 0
    elif y>big or y==big:
        return 1
    else:
        index=bisect.bisect(spacing,y)
        return vals[0][index]

def var(a):
    n=len(a)
    m=np.mean(a)
    z=np.array([a[i]-m for i in range(n)])
    return ((sum(z**2))/(n-1))**(1/2)

def make_ppf(a,perc):
    a=sorted(a)
    N=len(a)
    index=int(N*perc)
    if perc==1 or perc>1:
        return max(a)
    elif perc==0 or perc<0:
        return min(a)
    else:
        return a[index]

def R2_adj(a,b,p):
    n=len(a)
    return (R2(a,b)-1)*(n-1)/(n-1-p)+1

def square(x):
    return x**2

def make_baseline(df):
    df['pics_squared']=df['pics'].apply(square)
    df['desLength_squared']=df['desLength'].apply(square)
    df['descriptors_squared']=df['descriptors'].apply(square)
    df['stars_squared']=df['stars'].apply(square)
    return df

def test_fun(a,b):
    return a+2*b
