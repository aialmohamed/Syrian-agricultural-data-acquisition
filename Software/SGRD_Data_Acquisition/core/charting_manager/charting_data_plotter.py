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
    def plot_indicators(self):
        """
        Plot each indicator over time.
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

        