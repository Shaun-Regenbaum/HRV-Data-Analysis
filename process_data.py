import pandas as pd

# Global Data
DF1 = pd.read_csv(
    './HRV-Data-Analysis/Normal Data.csv', sep=',')
DF2 = pd.read_csv(
    './HRV-Data-Analysis/Arrythmic Data.csv', sep=',')
SECONDS = 60


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
    hrs = []
    for i in range(20):
        column_name = "Subject " + str(i+1)
        print(column_name)
        hrs.append(get_bpm_from_patient(df, column_name))
    return hrs


normal = get_hr_from_df(DF1)
arrythmic = get_hr_from_df(DF2)

print(normal, arrythmic)


# In order to find the heart rate, we simply need to divide the amount of R-Peaks identified in 60 seconds to get bpm:
# function derive_bpm(r-peaks, seconds):
