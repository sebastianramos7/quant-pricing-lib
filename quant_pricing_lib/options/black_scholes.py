from scipy.stats import norm
import numpy as np
class BlackScholes:
    def __init__(self,S,K,T,r,sigma):
        """
Black-Scholes model for pricing European vanilla options.

Parameters:
S:float
Current price of the underlying asset
K:float
Strike price of the option
T:float
Time to maturity in years (e.g. 6 months = 0.5)
r:float
Risk-free interest rate (annualized, e.g. 5% = 0.05)
sigma:float
Volatility of the underlying asset (annualized, e.g. 20% = 0.20)

Example
-------
option = BlackScholes(S=100, K=105, T=1, r=0.05, sigma=0.20)
option.price(kind="call")
"""
        self.S=S
        self.K=K
        self.T=max(T,1e-10)
        self.r=r
        self.sigma=sigma
    def getd1_d2(self):
        d1=(np.log(self.S/self.K)+(self.r+0.5*self.sigma**2)*self.T)/(self.sigma*np.sqrt(self.T))
        d2=d1-self.sigma*np.sqrt(self.T)
        return d1,d2
    def price(self,kind="call"):
        d1,d2=self.getd1_d2()
        if kind.lower()=="call":
            price=(self.S*norm.cdf(d1))-(self.K*np.exp(-self.r*self.T)*norm.cdf(d2))
            return price
        elif kind.lower()=="put":
            price=(self.K*np.exp(-self.r*self.T)*norm.cdf(-d2))-(self.S*norm.cdf(-d1))
            return price
        else:
            raise ValueError("Kind must be 'call' or 'put'")
        
    def __repr__(self):
        return(f"BlackScholes(S={self.S},K={self.K},T={self.T},r={self.r}, sigma={self.sigma})")