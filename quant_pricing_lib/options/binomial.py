import numpy as np
from black_scholes import BlackScholes

class BinomialTree:
    def __init__(self, S, K, T, r, sigma, N=100, option_type="european", kind="call"):
        self.S=S
        self.K=K
        self.T=T
        self.r=r
        self.sigma=sigma
        self.N=N
        self.option_type=option_type.lower()
        self.kind=kind.lower()
        self._build_params()

    def _build_params(self):
        """
        Calcule dt, u, d, et p.
        Formules :
        dt = T / N
        u = exp(sigma * sqrt(dt))
        d = 1 / u
        p = (exp(r * dt) - d) / (u - d)
        """
        self.dt=self.T/self.N
        self.u=np.exp(self.sigma*np.sqrt(self.dt))
        self.d=1/self.u
        self.p=(np.exp(self.r*self.dt)-self.d)/(self.u-self.d)

    def _asset_prices_at_maturity(self):
        """
        Génère les prix de l'actif à l'étape N.
        Prix = S * (u ** j) * (d ** (N - j))
        """
        j=np.arange(self.N+1)
        S_at_maturity=self.S*(self.u**j)*(self.d**(self.N-j))
        return S_at_maturity

    def _initialize_payoffs(self, S_at_maturity):
        """
        Calcule le payoff final au temps T.
        Call : max(S - K, 0) | Put : max(K - S, 0)
        Utilise np.maximum(..., 0)
        """
        if self.kind=="call":
            payoff=np.maximum(S_at_maturity-self.K,0)
        elif self.kind=="put":
            payoff=np.maximum(self.K-S_at_maturity,0)
        else:
            raise ValueError("Kind must be 'call' or 'put'.")
        return(payoff)
    def _backward_induction(self,V):
        """
        Boucle de N-1 jusqu'à 0.
        1. Calcule la valeur de continuation (V_cont).
        2. Calcule le prix de l'actif au nœud actuel (pour l'exercice anticipé).
        3. Si American : V = max(V_cont, exercice_immediat)
           Si European : V = V_cont
        """
        dt=self.dt
        for i in reversed(range(self.N)):
            V=(self.p*V[1:]+(1-self.p)*V[:-1])*np.exp(-self.r*dt)
            if self.option_type=="american":
                j=np.arange(i+1)
                S_i=self.S*(self.u**j)*(self.d**(i-j))
                if self.kind=="call":
                    V=np.maximum(V,S_i-self.K)
                else:
                    V=np.maximum(V,self.K-S_i)
        return V[0]

    def price(self):
        S_mat=self._asset_prices_at_maturity()
        V=self._initialize_payoffs(S_mat)
        price=self._backward_induction(V)
        return price
        
    def compare_to_bs(self):
        """Instancie BlackScholes et compare"""
        bs=BlackScholes(self.S, self.K, self.T, self.r, self.sigma)
        bs_price=bs.price(kind=self.kind)
        bin_price=self.price()
        return {
            "Binomial": bin_price,
            "BlackScholes": bs_price,
            "Difference": bin_price-bs_price
        }