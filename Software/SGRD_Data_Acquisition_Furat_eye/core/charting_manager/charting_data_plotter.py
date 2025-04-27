import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class ChartingDataPlotter:
    def __init__(self, data):
        """
        Initialize the ChartingDataPlotter with the data to be plotted.
        """
        self.data = data
        self.df = None
    def _create_frame(self):
        """
        Create data frames for plotting.
        """
        df = pd.DataFrame(self.data)
        df['date'] =pd.to_datetime(df['date'])
        for col in df.columns:
            if col not in ['date', 'region_id']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        self.df = df
    def plot_indicator(self):
        """
        Plot an indicator over time.
        """
        if self.df is None:
            self._create_frame()

        indicators = [col for col in self.df.columns if col not in ["date", "region_id"]]
        region = self.df["region_id"].iloc[0] if "region_id" in self.df else "Unknown"
        sns.set_theme(context="paper",style="white")
        for indicator in indicators:
            plt.figure(figsize=(10, 5))
            plt.plot(self.df["date"], self.df[indicator], marker="o", label=indicator)
            plt.title(f"{indicator} over time\nRegion: {region}")
            plt.xlabel("Date")
            plt.ylabel(indicator)
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
    @staticmethod
    def plot_combined_indicators(df1, df2, label1="Indicator 1", label2="Indicator 2", title=None):
        """
        Plot two indicators from two dataframes on the same figure.
        Assumes both have 'date' as a column.
        """
        df1 = pd.DataFrame(df1)
        df2 = pd.DataFrame(df2)

        df1['date'] = pd.to_datetime(df1['date'])
        df2['date'] = pd.to_datetime(df2['date'])

        value_col1 = [col for col in df1.columns if col not in ['date', 'region_id']][0]
        value_col2 = [col for col in df2.columns if col not in ['date', 'region_id']][0]

        sns.set_theme(context="paper", style="white")
        plt.figure(figsize=(10, 5))
        plt.plot(df1['date'], pd.to_numeric(df1[value_col1], errors='coerce'), marker='o', label=label1)
        plt.plot(df2['date'], pd.to_numeric(df2[value_col2], errors='coerce'), marker='s', label=label2)
        plt.title(title or f"{label1} vs {label2} over time")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    def plot_indicators(self):
        """
        Plot all indicators in the data.
        """
        df = pd.DataFrame(self.data)
        indicators = [col for col in df.columns if col not in ["date", "region_id"]]
        df_long = pd.melt(df, id_vars=["date"], value_vars=indicators, var_name="Indicator", value_name="Value")
        
        # Convert to numeric!
        df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")
        
        df_wide = df_long.pivot_table(index="date", columns="Indicator", values="Value")
        df_wide = df_wide.sort_index()

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df_long, x="date", y="Value", hue="Indicator", marker="o")
        plt.title("Indicators over time")
        plt.xlabel("Date")
        plt.ylabel("Index Value")
        plt.legend(title="Indicators")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    def plot_and_interpolate(self, resample_rule='MS'):
        """
        Plot all indicators after resampling and interpolating missing values.
        
        Parameters:
        resample_rule (str): The pandas resample rule, e.g., 'D' for daily, 'W' for weekly, 'MS' for month start.
        """
        df = pd.DataFrame(self.data)
        indicators = [col for col in df.columns if col not in ["date", "region_id"]]
        
        df_long = pd.melt(df, id_vars=["date"], value_vars=indicators, var_name="Indicator", value_name="Value")
        
        # Convert types
        df_long["date"] = pd.to_datetime(df_long["date"])
        df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")
        
        # Pivot to wide format
        df_wide = df_long.pivot_table(index='date', columns='Indicator', values='Value')
        
        # Resample and interpolate
        df_wide = df_wide.resample(resample_rule).mean()
        df_wide = df_wide.interpolate(method='linear')

        # Melt back to long format for plotting
        df_long_interpolated = df_wide.reset_index().melt(id_vars="date", var_name="Indicator", value_name="Value")
        
        # Plot
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df_long_interpolated, x="date", y="Value", hue="Indicator", marker="o")
        plt.title(f"Interpolated Indicators over Time (Resampled: {resample_rule})")
        plt.xlabel("Date")
        plt.ylabel("Index Value")
        plt.legend(title="Indicators")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        