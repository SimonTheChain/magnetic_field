#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

from sklearn.base import BaseEstimator, TransformerMixin


class MagneticImputer(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass
    
    def fit(self, X: pd.DataFrame, y: pd.Series=None) -> pd.DataFrame:
        # nothing to do here, just return the dataframe as is
        return self
    
    def transform(self, X:pd.DataFrame) -> np.array:
        # fill missing values and return the modified dataframe
        my_imputer = SimpleImputer()
        X = X.copy()
        X = pd.DataFrame(my_imputer.fit_transform(X))
        return X


class MagneticScaler(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass
    
    def fit(self, X: np.array, y: pd.Series=None) -> np.array:
        # nothing to do here, just return the dataframe as is
        return self
    
    def transform(self, X:np.array) -> np.array:
        # fill missing values and return the modified dataframe
        my_imputer = SimpleImputer()
        X = X.copy()
        imputed_X = my_imputer.fit_transform(X)
        return imputed_X