import pandas as pd
import numpy as np

# Global Data
DF1 = pd.read_csv(
    'Normal Data.csv', sep=',')
DF2 = pd.read_csv(
    'Arrythmic Data.csv', sep=',')
SECONDS = 60

# Processing functions


def get_beats_from_patient(df, column_name):
    boolean = df[column_name].notna()
    beats = 0
    for item in boolean:
        if item:
            beats += 1
        else:
            return beats
    return beats


def get_bpm_from_patient(df, column_name):
    beats = get_beats_from_patient(df, column_name)
    seconds = SECONDS
    bpm = beats/seconds * 60

    print(bpm)
    return bpm


def get_hr_from_df(df):
    heartrates = []
    for i in range(20):
        column_name = "Subject " + str(i+1)
        print(column_name)
        heartrates.append(get_bpm_from_patient(df, column_name))
    return heartrates


def get_rr_peaks_from_patient(df, column_name):
    rr_peaks = []
    boolean = df[column_name].notna()
    i = 0
    for item in boolean:
        if item:
            rr_peaks.append(df[column_name][2+i])
            i += 1
        else:
            return rr_peaks
    return rr_peaks


def get_rr_interval_from_patient(df, column_name):
    peaklist = get_rr_peaks_from_patient(df, column_name)
    # A neat numpy function to give us the intervals:
    rr_list = np.diff(peaklist)
    rr_intervals = np.abs(np.diff(rr_list))
    return rr_intervals


def get_rmssd_from_rr_interval(rr_interval):
    # A neat numpy function to give us the intervals:
    diff_nni = np.diff(rr_interval)
    rmssd = np.sqrt(np.mean(diff_nni ** 2))
    return rmssd


def get_rmssd_from_df(df):
    rmssd_values = []
    for i in range(20):
        column_name = "Subject " + str(i+1)
        print(column_name)
        rr_interval = get_rr_interval_from_patient(df, column_name)
        rmssd_values.append(get_rmssd_from_rr_interval(rr_interval))
    return rmssd_values


# Getting Heart Rates:
normal_hr = get_hr_from_df(DF1)
arrythmic_hr = get_hr_from_df(DF2)

normal_rmssd = get_rmssd_from_df(DF1)
arrythmic_rmssd = get_rmssd_from_df(DF2)

print(normal_rmssd)
print(arrythmic_rmssd)
