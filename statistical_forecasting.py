import tensorflow as tf
import keras
import numpy as np
from plot_utils import plot_series
from synth_data_gen import generate_synthetic_data
import matplotlib.pyplot as plt


time = np.arange(0,1000, dtype=float)
series = generate_synthetic_data(time, trend=True, slope=1, seasonality=True, period=200, amplitude=300, noise=True, noise_level=10)
split_time = 600


def trailing_moving_average(series, window_size):
    forecast = []
    for time in range(len(series)-window_size):
        forecast.append(series[time:time+window_size].mean())
    
    return np.array(forecast)

ma_series = trailing_moving_average(series, 30)

ma_series = ma_series[split_time-30:]

print("\nMoving average : \nmae = ", keras.metrics.mean_absolute_error(series[split_time:], ma_series).numpy())
print("mse = ", keras.metrics.mean_squared_error(series[split_time:], ma_series).numpy())

plot_series(time[split_time:], (series[split_time:],ma_series))

def differenced_series(series, window_size):
    return series[window_size:] - series[:-window_size]


diff_series = differenced_series(series, 200) # You should remove slope*period from the differenced series
ma_diff_series = trailing_moving_average(diff_series, 30)

ma_diff_series = ma_diff_series[split_time-230:]
ma_diff_series += series[split_time-200:-200]


plot_series(time[split_time:], (ma_diff_series, series[split_time:]))

print("\nDifferenced series : \nmae = ", keras.metrics.mean_absolute_error(series[split_time:], ma_diff_series).numpy())
print("mse = ", keras.metrics.mean_squared_error(series[split_time:], ma_diff_series).numpy())