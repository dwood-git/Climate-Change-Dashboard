"""
Data management module for the wildfire climate change visualization dashboard.

This module handles loading, caching, and providing access to all datasets
used throughout the application, including temperature, precipitation,
vegetation, drought, and fire data.

Author: Dylan Wood
Last updated: January 2025
"""

import pandas as pd
import os
from typing import Dict, Any, Optional
from loader import ClimateDataLoader


class DataManager:
    """
    Centralized data manager for loading and caching application datasets.
    
    This class provides a single point of access to all data used in the
    dashboard, with lazy loading and caching for performance optimization.
    """
    
    def __init__(self):
        """Initialize the data manager and climate data loader."""
        self._loader = ClimateDataLoader()
        self._cache: Dict[str, pd.DataFrame] = {}
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all datasets into cache on initialization."""
        try:
            # Load temperature data
            self._cache['ga_temperature'] = self._loader.load_ga_temperature()
            self._cache['ca_temperature'] = self._loader.load_ca_temperature()
            
            # Load precipitation data
            self._cache['ga_precipitation'] = self._loader.load_ga_precipitation()
            self._cache['ca_precipitation'] = self._loader.load_ca_precipitation()
            
            # Load vegetation data
            self._cache['vegetation'] = pd.read_csv("data/vegetation/Vegetation_Index_California_Georgia.csv")
            
            # Load drought data
            self._cache['drought'] = pd.read_csv("data/drought/Drought_Severity_California_Georgia.csv")
            
            # Load fire model data
            self._cache['fire_model'] = pd.read_csv("data/california/Fire_Model_California.csv")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            # Initialize with empty DataFrames if loading fails
            self._cache = {
                'ga_temperature': pd.DataFrame(),
                'ca_temperature': pd.DataFrame(),
                'ga_precipitation': pd.DataFrame(),
                'ca_precipitation': pd.DataFrame(),
                'vegetation': pd.DataFrame(),
                'drought': pd.DataFrame(),
                'fire_model': pd.DataFrame()
            }
    
    def get_ga_temperature(self) -> pd.DataFrame:
        """Get Georgia temperature data."""
        return self._cache.get('ga_temperature', pd.DataFrame())
    
    def get_ca_temperature(self) -> pd.DataFrame:
        """Get California temperature data."""
        return self._cache.get('ca_temperature', pd.DataFrame())
    
    def get_ga_precipitation(self) -> pd.DataFrame:
        """Get Georgia precipitation data."""
        return self._cache.get('ga_precipitation', pd.DataFrame())
    
    def get_ca_precipitation(self) -> pd.DataFrame:
        """Get California precipitation data."""
        return self._cache.get('ca_precipitation', pd.DataFrame())
    
    def get_vegetation_data(self) -> pd.DataFrame:
        """Get vegetation indices data."""
        return self._cache.get('vegetation', pd.DataFrame())
    
    def get_drought_data(self) -> pd.DataFrame:
        """Get drought severity data."""
        return self._cache.get('drought', pd.DataFrame())
    
    def get_fire_model_data(self) -> pd.DataFrame:
        """Get fire model data for California."""
        return self._cache.get('fire_model', pd.DataFrame())
    
    def get_california_fire_data(self) -> pd.DataFrame:
        """Get California-specific fire data."""
        fire_data = self.get_fire_model_data()
        if not fire_data.empty:
            return fire_data[fire_data["State"] == "California"]
        return pd.DataFrame()
    
    def reload_data(self):
        """Reload all datasets from source files."""
        self._cache.clear()
        self._load_all_data()
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get a summary of all loaded datasets."""
        summary = {}
        for key, df in self._cache.items():
            summary[key] = {
                'rows': len(df),
                'columns': list(df.columns) if not df.empty else [],
                'loaded': not df.empty
            }
        return summary 