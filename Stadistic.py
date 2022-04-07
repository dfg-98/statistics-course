# Import necessary libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.read_csv('yatch.csv')
df.head()
# LongPosition
var_name = 'LongPosition'
num_class = 11

min_value = df[var_name].min()
max_value = df[var_name].max()
bins = np.linspace(min_value, max_value, num_class)
labels = []
for i in range(len(bins) - 1):
    labels.append(f"[{bins[i]:.2f}, {bins[i + 1]:.2f}]")
df[f'{var_name}_bins'] = pd.cut(df[var_name], bins=bins, labels=labels, include_lowest=True)

plt.hist(df[f'{var_name}_bins'], bins=len(bins))
absolute_df = df[var_name].groupby(df[f'{var_name}_bins']).count()
frecuency_df = df[var_name].groupby(df[f'{var_name}_bins']).count() / df.shape[0]
absolute_df_acumulated = []
absolute_df_acumulated.append(absolute_df[0])
for i in range(len(absolute_df) - 1):
    absolute_df_acumulated.append(absolute_df[i + 1] + absolute_df_acumulated[i])
print(absolute_df_acumulated)
frecuency_df.plot(kind='bar')
print(absolute_df)
print(frecuency_df)
print(bins)

# MEAN
class_marks = []
for i in range(len(bins) - 1):
    class_marks.append((bins[i] + bins[i + 1]) / 2)
print(class_marks)
mean = 0
for i in range(len(class_marks)):
    mean = mean + class_marks[i] * absolute_df[i]
mean = mean / len(df)
print(mean)

# MODE
amp_class = bins[0] - bins[1]
mode_class = -1
for i in range(len(absolute_df)):
    if absolute_df[i] > absolute_df[mode_class]:
        mode_class = i
print(mode_class)
mode = bins[mode_class] + amp_class * (frecuency_df[mode_class] - frecuency_df[mode_class - 1]) / (
        (frecuency_df[mode_class] - frecuency_df[mode_class - 1]) + (
        frecuency_df[mode_class] - frecuency_df[mode_class - 1]))
print(mode)

# MEDIAN
median_class = -1
for i in range(len(absolute_df_acumulated)):
    if absolute_df_acumulated[i] >= len(df) / 2:
        median_class = i
        break

median = bins[median_class - 1] + amp_class * (
        (len(df) / 2) - absolute_df_acumulated[
    median_class - 1]) / (absolute_df_acumulated[median_class] - absolute_df_acumulated[median_class - 1])
print(median)

# VARIANCE
variance = 0
for i in range(len(class_marks)):
    variance = variance + frecuency_df[i] * (class_marks[i] - mean) ** 2
variance = variance / len(df)
print(variance)

# DEVIATIONS COEFFICIENT
dev = math.sqrt(variance)
print(dev)

# Variance COEFFICIENT
var_coef = dev / mean
print(var_coef)

# Intervalo de Confianza de la Media
mean_estimator = 0
for i in range(len(df[var_name])):
    mean_estimator=mean_estimator+df[var_name][i]
mean_estimator=mean_estimator/len(df)
low_limit_mean = mean_estimator - 2 * variance / math.sqrt(len(df))
top_limit_mean = mean_estimator + 2 * variance / math.sqrt(len(df))
print("El intervalo de confianza para la media es entre " + str(low_limit_mean) + " y " + str(top_limit_mean))

# Intervalo de Confianza para la Varianza
variance_estimator = 0
for i in range(len(df[var_name])):
    variance_estimator = variance_estimator+(df[var_name][i]-mean_estimator)**2
variance_estimator = variance_estimator/(len(df)-1)
low_limit_variance = (len(df)-1)*variance_estimator/((len(df)-1) * 2 ** 2)
top_limit_variance = (len(df)-1)*variance_estimator/((len(df)-1) * 2 ** 2)
print("El intervalo de confianza para la varianza es entre " + str(low_limit_variance) + " y " + str(top_limit_variance))
