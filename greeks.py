from scipy.stats import norm
import numpy as np
class Greeks:
    def __init__(self, bs_model, kind="call"):
        """
        Calcule les Greeks à partir d'une instance de BlackScholes.
        bs_model : une instance de la classe BlackScholes
        kind : "call" ou "put"
        """
        self.bs=bs_model
        self.kind=kind.lower()
        self.d1,self.d2=self.bs.getd1_d2()
        self.n_prime_d1=norm.pdf(self.d1)
    def delta(self):
        if self.kind=="call":
            return norm.cdf(self.d1)
        return norm.cdf(self.d1) - 1

    def gamma(self):
        return self.n_prime_d1/(self.bs.S*self.bs.sigma*np.sqrt(self.bs.T))

    def vega(self,unit=0.01):
        v=self.bs.S*np.sqrt(self.bs.T)*self.n_prime_d1
        return v*unit

    def theta(self,days_per_year=365):
        term1=-(self.bs.S*self.n_prime_d1*self.bs.sigma)/(2*np.sqrt(self.bs.T))
        if self.kind=="call":
            theta_annuel=term1-self.bs.r*self.bs.K*np.exp(-self.bs.r*self.bs.T)*norm.cdf(self.d2)
        else:
            theta_annuel=term1+self.bs.r*self.bs.K*np.exp(-self.bs.r*self.bs.T)*norm.cdf(-self.d2)
        return theta_annuel/days_per_year

    def rho(self, unit=0.01):
        if self.kind=="call":
            r_val=self.bs.K*self.bs.T*np.exp(-self.bs.r*self.bs.T)*norm.cdf(self.d2)
        else:
            r_val=-self.bs.K*self.bs.T*np.exp(-self.bs.r*self.bs.T)*norm.cdf(-self.d2)
        return r_val*unit

    def all_greeks(self):
        """Retourne un dictionnaire avec tous les greeks"""
        return {
            "kind":self.kind,
            "Delta": self.delta(),
            "Gamma": self.gamma(),
            "Vega (1%)": self.vega(),
            "Theta (1 day)": self.theta(),
            "Rho (1%)": self.rho()
        }
    def __repr__(self):
        return f"Greeks(model={self.bs},kind='{self.kind}')"