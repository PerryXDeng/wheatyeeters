import pandas as pd


def vectorize_mult(df, column, dictionary):
    """
    Changes all the categorical values into its respective
    number in the dictionary and then saves it in the DF
    :param df: dataframe
    :param column: column name
    :param dictionary: alterations to make
    """
    newCol = column + "Num"
    df[newCol] = df[column].map(dictionary)


class WellnessCSV:
    def __init__(self):
        self.file = "data/wellness.csv"
        self.end = "cleaned/notnormalized_with_0NaN_wellness.csv"

    def vectorize(self):
        df = pd.read_csv(self.file)

        # Vectorizing appropriate data
        vectorize_mult(df, "Pain", {"No": 0, "Yes": 1})
        vectorize_mult(df, "Illness", {"No": 0, "Slightly Off": 0.5, "Yes": 1})
        vectorize_mult(df, "Menstruation", {"No": 0, "Yes": 1})
        vectorize_mult(df, "Nutrition", {"Poor": 0, "Okay": 0.5, "Excellent": 1})
        vectorize_mult(df, "NutritionAdjustment", {"No": 0, "Yes": 1})
        vectorize_mult(df, "USGMeasurement", {"No": 0, "Yes": 1})

        readiness = []
        for i, value in df["TrainingReadiness"].iteritems():
            value = value.split("%")[0]
            value = int(value) * (1/100)
            readiness.append(value)

        df["TrainingReadinessNum"] = readiness

        # Filling in NaNs for appropriate layers where they won't make a statistical difference
        df["MenstruationNum"] = df["MenstruationNum"].fillna(0)
        df["USGMeasurementNum"] = df["USGMeasurementNum"].fillna(0)
        df["NutritionNum"] = df["MenstruationNum"].fillna(0)
        df["NutritionAdjustmentNum"] = df["NutritionAdjustmentNum"].fillna(0)

        # Saving the df to the "cleaned" CSV
        df.to_csv(self.end)


class FatigueSum:
    def __init__(self):
        self.file = "cleaned/time_series_normalized_wellness.csv"
        self.end = "cleaned/fatigue_total_sum.csv"

    def calculate(self):
        df = pd.read_csv(self.file)

        # get some of the fatigue for a particular date
        diction = dict()
        dates = df["TimeSinceAugFirst"].unique()
        dates = set(dates)
        dates = list(dates)

        # for each date, get unique data and get calculation
        for date in dates:
            pdf = df[df["TimeSinceAugFirst"] == date]
            num_players = len(pdf["playerID"].unique())
            fatigue_sum = pdf["normFatigue"].sum()
            result = fatigue_sum / num_players
            diction[date] = result

        # Converting
        dates = diction.keys()
        values = diction.values()

        final_df = pd.DataFrame()
        final_df["TimeSinceAugFirst"] = dates
        final_df["fatigueSum"] = values
        final_df.to_csv(self.end)

