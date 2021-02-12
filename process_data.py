import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Global Data
DF1 = pd.read_csv(
    'Normal Data.csv', sep=',')
DF2 = pd.read_csv(
    'Arrythmic Data.csv', sep=',')


# Processing functions
# This functions just returns the number of beats in the array by looking for NA
def get_beats_from_patient(df, column_name):
    boolean = df[column_name].notna()
    beats = 0
    for item in boolean:
        if item:
            beats += 1
        else:
            return beats - 1  # We subtract one to ignore the first beat.
    return beats


# This function finds the time difference between the first rr-peak and the last
def get_duration_from_patient(df, column_name):
    beats = get_beats_from_patient(df, column_name)
    first_beat_time = df[column_name][0]
    last_beat_time = df[column_name][beats - 1]
    # print(first_beat_time, last_beat_time)
    duration = last_beat_time - first_beat_time
    return duration


# This function gets bpm by diving numbers of beats by duration
def get_bpm_from_patient(df, column_name):
    beats = get_beats_from_patient(df, column_name)
    seconds = get_duration_from_patient(df, column_name)
    bpm = beats/seconds * 60
    # print(bpm)
    return bpm


# This function cleans up the data by returning, just an array of the rr-peaks without any NA.
def get_rr_peaks_from_patient(df, column_name):
    rr_peaks = []
    boolean = df[column_name].notna()
    i = 0
    for item in boolean:
        if item:
            rr_peaks.append(df[column_name][i])
            i += 1
        else:
            return rr_peaks
    return rr_peaks


# This function finds the times between rr-peaks
def get_rr_list_from_patient(df, column_name):
    peaklist = get_rr_peaks_from_patient(df, column_name)
    fs = 1 / get_duration_from_patient(df, column_name)
    # A neat numpy function to give us the intervals:
    rr_list = (np.diff(peaklist)) * 1000
    # print(rr_list)
    return rr_list


# This function finds the interval between rr-peaks
def get_rr_interval_from_patient(df, column_name):
    rr_list = get_rr_list_from_patient(df, column_name)
    rr_intervals = np.abs(rr_list)
    # print(rr_intervals)
    return rr_intervals


# This function finds the rmssd value from the rr-intervals
def get_rmssd_from_rr_interval(rr_interval):
    # A neat numpy function to give us the intervals:
    diff_nni = np.diff(rr_interval)
    rmssd = np.sqrt(np.mean(diff_nni ** 2))
    return rmssd


# Iterating Functions
# This function finds bpm for all patients in a df
def get_hr_from_df(df):
    heartrates = []
    for i in range(20):
        column_name = "Subject " + str(i+1)
        # print(column_name)
        heartrates.append(get_bpm_from_patient(df, column_name))
    return heartrates


# This function finds the duration of reads for all patients in a df
def get_durations_from_df(df):
    durations = []
    for i in range(20):
        column_name = "Subject " + str(i+1)
        # print(column_name)
        durations.append(get_duration_from_patient(df, column_name))
    return durations


# This function finds the rmssd for all patients in a df
def get_rmssd_from_df(df):
    rmssd_values = []
    for i in range(20):
        column_name = "Subject " + str(i+1)
        # print(column_name)
        rr_interval = get_rr_interval_from_patient(df, column_name)
        # print(rr_interval)
        rmssd_values.append(get_rmssd_from_rr_interval(rr_interval))
    return rmssd_values


# This function finds the mean ibi for all patients in a df
def get_ibi_from_df(df):
    ibi_values = []
    for i in range(20):
        column_name = "Subject " + str(i+1)
        # print(column_name)
        rr_interval = get_rr_interval_from_patient(df, column_name)
        ibi_values.append(np.mean(rr_interval))
    return ibi_values


# def get_lf_from_df(df):
#     lf_values = []
#     for i in range(20):
#         column_name = "Subject " + str(i+1)
#         # print(column_name)
#         rr_interval = get_rr_interval_from_patient(df, column_name)
#         lf_values.append(np.mean(rr_interval))
#     return lf_values


# Getting Durations:
# normal_duration = get_durations_from_df(DF1)
# arrythmic_duration = get_durations_from_df(DF2)
# print(normal_duration)
# print(arrythmic_duration)

# Getting Heart Rates:
# normal_hr = get_hr_from_df(DF1)
# arrythmic_hr = get_hr_from_df(DF2)
# print(normal_hr)
# print(arrythmic_hr)

# Getting IBI:
# normal_ibi = get_ibi_from_df(DF1)
# arrythmic_ibi = get_ibi_from_df(DF2)
# print(normal_ibi)
# print(arrythmic_ibi)

# Getting Rmssd:
# normal_rmssd = get_rmssd_from_df(DF1)
# arrythmic_rmssd = get_rmssd_from_df(DF2)
# print(normal_rmssd)
# print(arrythmic_rmssd)


# To find HF and LF we are gonna have to get a bit more complicated
# Also since Im doing this in python, I wont use the provided Matlab code:

def get_raw_and_interpplated_for_patient(df, column_name):
    # First we make an evenly spaced timeline:
    rr_peaks = get_rr_peaks_from_patient(df, column_name)
    rr_intervals = get_rr_interval_from_patient(df, column_name)

    # This is our raw data
    X = rr_peaks[1:]  # We want to remove the first one
    Y = rr_intervals

    # print(Y)
    # print(len(X), len(Y))

    # This is our interpolated data
    X_new = np.linspace(X[0], X[-1], len(X))
    f = interp1d(X, Y, kind='cubic', fill_value="extrapolate")
    Y_new = f(X_new)

    return X, Y, X_new, Y_new


# Just graphing it:
def graph_for_patient(df, column_name):
    RR_x, RR_y, RR_x_new, RR_y_new = get_raw_and_interpplated_for_patient(
        df, column_name)
    plt.title("Original and Interpolated Signal")
    plt.plot(RR_x, RR_y, label="Original", color='blue')
    plt.plot(RR_x_new, RR_y_new, label="Interpolated", color='red')
    plt.legend()
    plt.show()


def graph_fft_for_patient(df, column_name):
    RR_x, RR_y, RR_x_new, RR_y_new = get_raw_and_interpplated_for_patient(
        df, column_name)

    n = len(RR_x)
    # divide the bins into frequency categories
    frq = np.fft.fftfreq(n, d=60)

    # Get single side of the frequency range
    frq = frq[range(round(n/2))] * 100

    # Do FFT
    Y = np.fft.fft(RR_y_new)/n  # Calculate FFT
    Y = Y[range(round(n/2))]  # Return one side of the FFT

    print(frq)
    print(Y)

    # Plot
    plt.title("Frequency Spectrum of Heart Rate Variability")
    # Limit X axis to frequencies of interest (0-0.6Hz for visibility, we are interested in 0.04-0.5)
    # plt.xlim(0, 0.6)
    plt.ylim(0, 50)  # Limit Y axis for visibility
    plt.plot(frq, abs(Y))  # Plot it
    plt.xlabel("Frequencies in Hz")
    plt.show()


def get_lh_and_hf_for_patient(df, column_name):
    RR_x, RR_y, RR_x_new, RR_y_new = get_raw_and_interpplated_for_patient(
        df, column_name)

    n = len(RR_x)  # Length of the signal
    # divide the bins into frequency categories
    frq = np.fft.fftfreq(n, d=60)

    # Get single side of the frequency range
    frq = frq[range(round(n/2))] * 100

    # Do FFT
    Y = np.fft.fft(RR_y_new)/n  # Calculate FFT
    Y = Y[range(round(n/2))]  # Return one side of the FFT


    lf = np.trapz(abs(Y[(frq >= 0.04) & (frq <= 0.15)]))
    hf = np.trapz(abs(Y[(frq >= 0.16) & (frq <= 0.5)]))
    return lf, hf


graph_for_patient(DF2, "Subject 1")
graph_fft_for_patient(DF2, "Subject 1")
print(get_lh_and_hf_for_patient(DF2, "Subject 1"))
