import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

os.makedirs("img", exist_ok=True)

#I selected 2012 through 2021 to capture the growth and expansion phase of the product lifecycle. 
#the Bass model assumes cumulative adoption always increases toward M.
#fitbit hit its peak of 41.5M users in 2021 before declining due to smartwatches.

years_list = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
time_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
users_list = [0.56, 2.60, 6.70, 14.90, 23.60, 29.00, 33.80, 38.30, 40.20, 41.50, 40.00, 38.50, 36.00, 33.00]

#slice the growth phase (first 10 years) for curve fitting
train_time = np.array(time_list[:10])
train_users = np.array(users_list[:10])


#bass diffusion formula 
def bass_formula(time_point, alpha, beta, ceiling):
    exponential_rate = np.exp(-(alpha + beta) * time_point)
    total_adopters = ceiling * (1 - exponential_rate) / (1 + (beta / alpha) * exponential_rate)
    return total_adopters

#initial guesses, bounds 
#without custom starting guesses, defaults parameter is 1,which fails on complex exponential models.
#0.033 is starting guess for innovation rate.
#0.45 is starting guess for imitation rate.
#45 is starting guess for market potential based on Fitbit's 41.5M peak.

initial_guesses = [0.033, 0.45, 45]
parameter_bounds = ([0.00005, 0.0005, 15], [0.15, 1.2, 220])

fitted_params, _ = curve_fit(
    bass_formula, 
    train_time, 
    train_users, 
    p0=initial_guesses, 
    bounds=parameter_bounds
)

#curve_fit returns an array where:
#[0] = alpha (p, innovation coefficient)
#[1] = beta (q, imitation coefficient)
#[2] = M, market potential

alpha_est = fitted_params[0]
beta_est = fitted_params[1]
ceiling_est = fitted_params[2]

print("bass model parameters are`")
print("innovation rate p is`", round(alpha_est, 7))      #round to 7 decimal 
print("imitation rate q is`", round(beta_est, 7))          #round to 7 decimal 
print("market size M is`", round(ceiling_est, 3), "million users")  #round to 3 decimal


#for WHOOP MG`
#np.arange(1, 13) for 12 year 
forecast_time = np.arange(1, 13)

#market capacity 50 million. Look-alike analysis estimate for WHOOP MG's target market.
whoop_market_capacity = 50.0  
adoption = bass_formula(forecast_time, alpha_est, beta_est, whoop_market_capacity)

#lets plot graph
fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(time_list, users_list, marker='o', color='red', linewidth=1, label='Fitbit')
ax.plot(forecast_time, adoption, linestyle='--', color='purple', linewidth=1, label='WHOOP MG')

ax.set_title("diffusion graph of WHOOP MG", fontsize=27)
ax.set_xlabel("diffusion in years")
ax.set_ylabel("active users in millions")
ax.grid(True, linestyle=':', alpha=0.33)
ax.legend(frameon=True)
plt.tight_layout()
plt.savefig("img/image1.png")
plt.show()