"""Module to load and filter climate data for Georgia and California.

This module provides the ClimateDataLoader class to load yearly average temperature
and precipitation data from CSV files for Georgia and California. The data files
expected are:
- data/georgia/GA_Yearly_Avg_Temps.csv
- data/georgia/GA_Yearly_Avg_Precip.csv
- data/california/CA_Yearly_Avg_Temps.csv
- data/california/CA_Yearly_Avg_Precip.csv

Each file contains monthly data which is processed to extract yearly averages,
standardize column names, and filter data by year range.
"""

import pandas as pd

class ClimateDataLoader:
    """Loader for climate time-series CSV data for Georgia and California.

    This class loads yearly average temperature and precipitation data from CSV files,
    standardizes column names, converts date formats, extracts year information,
    and filters the data to a specific year range.
    """

    def __init__(self):
        self.start_year = 1980
        self.end_year = 2022

    def load_ga_temperature(self):
        """Load Georgia yearly average temperature data.

        Reads 'data/georgia/GA_Yearly_Avg_Temps.csv', ignoring commented lines.
        Converts 'Date' from string format '%Y%m' to datetime, extracts year,
        renames 'Value' column to 'AvgTemperature', and filters by year range.

        Returns:
            pd.DataFrame: Filtered DataFrame with columns including 'Year' and 'AvgTemperature'.
        """
        # Read CSV, ignoring lines starting with '#' as comments
        df = pd.read_csv('data/georgia/GA_Yearly_Avg_Temps.csv', comment='#')
        # Parse 'Date' column to datetime using format YYYYMM
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
        # Extract year from the parsed 'Date'
        df['Year'] = df['Date'].dt.year
        # Rename 'Value' column to 'AvgTemperature' for clarity
        df['AvgTemperature'] = df['Value']
        # Filter rows to include only those within the specified year range
        return df[(df['Year'] >= self.start_year) & (df['Year'] <= self.end_year)]

    def load_ga_precipitation(self):
        """Load Georgia yearly average precipitation data.

        Reads 'data/georgia/GA_Yearly_Avg_Precip.csv', ignoring commented lines.
        Converts 'Date' from string format '%Y%m' to datetime, extracts year,
        renames 'Value' column to 'AvgPrecip', and filters by year range.

        Returns:
            pd.DataFrame: Filtered DataFrame with columns including 'Year' and 'AvgPrecip'.
        """
        # Read CSV, ignoring lines starting with '#' as comments
        df = pd.read_csv('data/georgia/GA_Yearly_Avg_Precip.csv', comment='#')
        # Parse 'Date' column to datetime using format YYYYMM
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
        # Extract year from the parsed 'Date'
        df['Year'] = df['Date'].dt.year
        # Rename 'Value' column to 'AvgPrecip' for clarity
        df['AvgPrecip'] = df['Value']
        # Filter rows to include only those within the specified year range
        return df[(df['Year'] >= self.start_year) & (df['Year'] <= self.end_year)]

    def load_ca_temperature(self):
        """Load California yearly average temperature data.

        Reads 'data/california/CA_Yearly_Avg_Temps.csv', ignoring commented lines.
        Converts 'Date' from string format '%Y%m' to datetime, extracts year,
        renames 'Value' column to 'AvgTemperature', and filters by year range.

        Returns:
            pd.DataFrame: Filtered DataFrame with columns including 'Year' and 'AvgTemperature'.
        """
        # Read CSV, ignoring lines starting with '#' as comments
        df = pd.read_csv('data/california/CA_Yearly_Avg_Temps.csv', comment='#')
        # Parse 'Date' column to datetime using format YYYYMM
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
        # Extract year from the parsed 'Date'
        df['Year'] = df['Date'].dt.year
        # Rename 'Value' column to 'AvgTemperature' for clarity
        df['AvgTemperature'] = df['Value']
        # Filter rows to include only those within the specified year range
        return df[(df['Year'] >= self.start_year) & (df['Year'] <= self.end_year)]

    def load_ca_precipitation(self):
        """Load California yearly average precipitation data.

        Reads 'data/california/CA_Yearly_Avg_Precip.csv', ignoring commented lines.
        Converts 'Date' from string format '%Y%m' to datetime, extracts year,
        renames 'Value' column to 'AvgPrecip', and filters by year range.

        Returns:
            pd.DataFrame: Filtered DataFrame with columns including 'Year' and 'AvgPrecip'.
        """
        # Read CSV, ignoring lines starting with '#' as comments
        df = pd.read_csv('data/california/CA_Yearly_Avg_Precip.csv', comment='#')
        # Parse 'Date' column to datetime using format YYYYMM
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m')
        # Extract year from the parsed 'Date'
        df['Year'] = df['Date'].dt.year
        # Rename 'Value' column to 'AvgPrecip' for clarity
        df['AvgPrecip'] = df['Value']
        # Filter rows to include only those within the specified year range
        return df[(df['Year'] >= self.start_year) & (df['Year'] <= self.end_year)]