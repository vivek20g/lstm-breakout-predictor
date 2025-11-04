"""
simulator/simulator.py

Class-based wrapper around simulator functions for a tidy API.
"""
from . import generate_dataframe, generate_dataset


class Simulator:
    """Simple class wrapper providing the main simulator API.

    Methods:
    - generate_dataframe(excel_path, sheet_name=None) -> pd.DataFrame
    - generate_dataset(excel_path, out_path, sheet_name=None) -> str
    """

    @staticmethod
    def generate_dataframe(excel_path, sheet_name=None):
        return generate_dataframe(excel_path, sheet_name)

    @staticmethod
    def generate_dataset(excel_path, out_path, sheet_name=None):
        return generate_dataset(excel_path, out_path, sheet_name)
