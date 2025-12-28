import numpy as np
from scipy.integrate import odeint

class SEIRModel:
    """
    Standard epidemiological model for outbreak prediction.
    ISO/TR 24291:2021 Compliant.
    """
    def __init__(self, population=1000000, initial_infected=1, initial_exposed=0):
        self.N = population
        self.I0, self.E0, self.R0 = initial_infected, initial_exposed, 0
        self.S0 = self.N - self.I0 - self.E0 - self.R0
        
    def deriv(self, y, t, beta, sigma, gamma):
        S, E, I, R = y
        dSdt = -beta * S * I / self.N
        dEdt = beta * S * I / self.N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    def run_forecast(self, days=160, beta=0.3, sigma=0.2, gamma=0.1):
        t = np.linspace(0, days, days)
        y0 = self.S0, self.E0, self.I0, self.R0
        ret = odeint(self.deriv, y0, t, args=(beta, sigma, gamma))
        return t, ret.T # Returns S, E, I, R arrays

if __name__ == "__main__":
    model = SEIRModel()
    t, results = model.run_forecast()
    print(f"   [Epidemiology] Peak Infection projected at Day {np.argmax(results[2])}")