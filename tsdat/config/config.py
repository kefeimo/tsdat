import yaml
import numpy as np
import xarray as xr
from typing import List, Dict
from .keys import Keys
from .attribute_defintion import AttributeDefinition
from .dimension_definition import DimensionDefinition
from .variable_definition import VariableDefinition
from .dataset_definition import DatasetDefinition
from .qctest_definition import QCTestDefinition

# TODO: add api method to download yaml templates or put them all
# in the examples folder.

class Config:
    """
    Wrapper for Dictionary of config values that provides helper functions for
    quick access.
    """

    def __init__(self, dictionary: Dict):
        self.dictionary = dictionary
        self.dataset_definition = DatasetDefinition(dictionary)
        self._parse_variables(dictionary) # Will be moved to dataset_definition
        self._parse_qc_tests(dictionary) # Will be moved to dataset_definition


    @classmethod
    def load(self, filepaths: List[str]) -> object:
        """-------------------------------------------------------------------
        Load one or more yaml config files which define data following 
        mhkit-cloud data standards.
        
        TODO: add a schema validation check on yaml so users can know if the 
        file is valid
        
        Args:
            filepaths (List[str]): The paths to the config files to load

        Returns:
            Config: A Config instance created from the filepaths.
        -------------------------------------------------------------------"""
        if isinstance(filepaths, str):
            filepaths = [filepaths]
        config = dict()
        for filepath in filepaths:
            with open(filepath, 'r') as file:
                dict_list = list(yaml.load_all(file, Loader=yaml.FullLoader))
                for dictionary in dict_list:
                    config.update(dictionary)
        return Config(config)

    def get_variable_names(self):
        # Stupid python 3 returns keys as a dict_keys object.
        # Not really sure the purpose of this extra class :(.
        return list(self.variables.keys())

    def get_variable(self, variable_name):
        return self.variables.get(variable_name, None)

    def get_variables(self):
        return self.variables.values()

    def get_qc_test_names(self):
        # Stupid python 3 returns keys as a dict_keys object.
        # Not really sure the purpose of this extra class :(.
        return list(self.qc_tests.keys())

    def get_qc_test(self, test_name):
        return self.qc_tests.get(test_name, None)

    def get_qc_tests(self):
        return self.qc_tests.values()

    def _parse_qc_tests(self, dictionary):
        self.qc_tests = {}
        test_names = dictionary.get(Keys.QC_TESTS, {}).keys()
        for test_name in test_names:
            test_dict = dictionary.get(Keys.QC_TESTS, {}).get(test_name, None)
            if test_dict:
                self.qc_tests[test_name] = QCTestDefinition(test_name, test_dict)

    def _parse_variables(self, dictionary):
        self.variables = {}
        variable_names = dictionary.get(Keys.VARIABLES, {}).keys()
        for variable_name in variable_names:
            var_dict = dictionary.get(Keys.VARIABLES, {}).get(variable_name, None)
            if var_dict:
                self.variables[variable_name] = VariableDefinition(variable_name, var_dict)
