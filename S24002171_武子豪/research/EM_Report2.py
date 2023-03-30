##各正規分布の平均と分散
##各正規分布の重み
from matplotlib import pyplot
import pandas as pd
import numpy as np
import sys
import scipy.stats
from sklearn import preprocessing

mm=preprocessing.MinMaxScaler()

filename = 'data10000.txt'
f = np.loadtxt(filename,delimiter=',')
f1 = np.std(f[:,0])
f2 = np.std(f[:,1])
#print('f1,f2:-----',f1,f2)
# f1 = f[:,0]
# f2 = f[:,1]
# f1 = preprocessing.minmax_scale(f1)
# f2 = preprocessing.minmax_scale(f2)
# f = np.array([f1,f2])
# f = f.T
data1 = f[:,0]#データ一列目
data2 = f[:,1]#データ二列目
#print(data1)
#print(f)

def create_data(f):
    X, mu_star, sigma_star = [], [], []
    X = np.append(X,data1)
    X = np.append(X,data2)
    loc = np.mean(f, axis=0) #平均
    print(loc)
    #print(loc) 
    scale = np.std(f,axis=0) #標準偏差
    print(scale)
    #print(X)
    mu_star = loc
    sigma_star = scale
           
    return (X, mu_star, sigma_star)

def gaussian(mu,sigma):
    def g(x):
        return np.exp(-0.5 * (x - mu) ** 2 / sigma) / np.sqrt(2 * np.pi * sigma)
    return g

def estimate_posterior_likelihood(X, pi, gf):
    l = np.zeros((X.size, pi.size))
    for (i, x) in enumerate(X):
        l[i, :] = gf(x)
        # print('y',lambda y:1/y)
        # print(np.vectorize(lambda y: 1 / y))
    return pi * l * np.vectorize(lambda y: 1 / y)(l.sum(axis = 1).reshape(-1, 1))

def estimate_gmm_parameter(X,gamma):
    N = gamma.sum(axis = 0 )
    mu = (gamma * X.reshape((-1,1))).sum(axis = 0 )/N
    sigma = (gamma * (X.reshape(-1,1) - mu) ** 2).sum(axis = 0) / N
    pi = N / X.size
    return (mu ,sigma ,pi)

def calc_Q(X,mu,sigma,pi,gamma):
    Q = (gamma * (np.log(pi* (2 * np.pi * sigma) ** (-0.5)))).sum()
    for (i,x) in enumerate(X):
        Q += (gamma[i,:] * (-0.5 * (x - mu) ** 2 /sigma)).sum()
        return Q
    
if __name__ == '__main__':

    K = 2
    N = 10000 * K
    X, mu_star, sigma_star = create_data(f)
    
    #print(X, mu_star, sigma_star)

    #termination condition
    epsilon = 0.01

    #initial parameter
    # D = X.shape[0]
    # mu = np.random.randn(1, D)
    # sigma = np.array([np.eye(D) for i in range(2)])
    # pi = np.array([1/2 for i in range(2)])

    #pi = np.random.rand(K)

    # mu = np.random.randn(K)
    # sigma = np.abs(np.random.randn(K))
    pi = np.array([0.5,0.5])
    mu = np.array([110,1150])
    sigma =  np.array([3.4,34])
    print('initial pi, mu ,sigma:',pi,mu,sigma)

    """
    mu_1 = np.random.randn(K)
    sigma_1 = np.abs(np.random.randn(K))
    mu_2 = np.random.randn(K)
    sigma_2 = np.abs(np.random.randn(K))
    """    
    Q = -sys.float_info.max 

    delta = None

    #EM algorithm
    while delta == None or delta >= epsilon:
        """
        gf_1 = gaussian(mu_1,sigma_1)#初期値が異なる必要がある？理由？
        gf_2 = gaussian(mu_2,sigma_2)
        """
        gf = gaussian(mu, sigma)
        print('平均_f1,f2---分散_sigma1,sigma2---重み_pi1,pi2')
        print(mu,sigma,pi)
        #print('重み_pi1,pi2',pi)
        #E step
        gamma = estimate_posterior_likelihood(X,pi,gf)#除数ゼロ
        #M step
        mu,sigma,pi = estimate_gmm_parameter(X,gamma)
        #cal Q function
        Q_new = calc_Q(X, mu , sigma, pi, gamma)
        delta = Q_new - Q
        Q = Q_new

    #result

    #plot
    # n,binsm, _= pyplot.hist(X)
    n, bins, _ = pyplot.hist(X, 50, density=True, alpha = 0.2)
    seq = np.arange(0, 1200, 1)
    for i in range(K):
        pyplot.plot(seq,gaussian(mu[i],sigma[i])(seq),linewidth=2.0)
    #pyplot.plot(f)
    pyplot.show()