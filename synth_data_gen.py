import numpy as np
from plot_utils import plot_series

def generate_synthetic_data(time, level=0, trend=False, slope=0, 
                            seasonality=False, period=0, phase=0, amplitude=0, 
                            noise=False, noise_level=0, 
                            autocorrelation=False, ac_amplitude=0 , phi1=0, phi2=0, 
                            impulses=False, nb_impulses=0, impulse_amplitude=0,
                            non_stationarity=False):
    

    series = np.zeros_like(time) + level

    if trend:
        series = slope * time

    if seasonality:
        season_time = ((time + phase) % period) / period
        pattern = np.where(season_time < 0.4,
                    np.cos(season_time * 2 * np.pi),
                    1 / np.exp(3 * season_time))
        series += amplitude * pattern

    if noise:
        noise_pattern = noise_level * np.random.randn(len(time))
        series += noise_pattern

    if autocorrelation:
        ar = np.random.randn(len(time) + 50)
        
        ar[:50] = 100

        for step in range(50, len(time) + 50):
            ar[step] += phi1 * ar[step - 50]
            ar[step] += phi2 * ar[step - 33]

        ar = ar[50:] * ac_amplitude
        series += ar

    if impulses:
        impulse_indices = np.random.randint(len(time), size=nb_impulses)

        for index in impulse_indices:
            series[index] += np.random.rand() * impulse_amplitude 



    return series

time = np.arange(0,30,1e-1)
# series = generate_synthetic_data(time, trend=False, slope=0.7, seasonality=True, period=10, phase=0, amplitude=5, level=1, noise=True, noise_level=0.5, 
                                 # autocorrelation=False, phi1=0.5, phi2=-0.1, ac_amplitude=1, impulses=True, nb_impulses=10, impulse_amplitude=10)

series = generate_synthetic_data(time, autocorrelation=True, ac_amplitude=1, phi1=0.5, phi2=-0.1, impulses=True, nb_impulses=10, impulse_amplitude=10)


plot_series(time,series)
