#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from category_encoders import OneHotEncoder

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

import config


# impute missing values
#def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
#    my_imputer = SimpleImputer(strategy="most_frequent", add_indicator=True, copy=True)
#    df_unscaled = pd.DataFrame(my_imputer.fit_transform(df))
#    df_unscaled.columns = df.columns
#    return df_unscaled


class FrequentImputer(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass
    
    def fit(self, X: pd.DataFrame, y: pd.Series=None) -> pd.DataFrame:
        # nothing to do here, just return the dataframe as is
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        # fill missing values and return the modified dataframe
        my_imputer = SimpleImputer(strategy="most_frequent", add_indicator=True, copy=True)
        X = X.copy()
        X = pd.DataFrame(my_imputer.fit_transform(X))
        X.columns = X.columns
        return X


# change tabular into numeric
#def tabular_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
#    encoder = OneHotEncoder(
#        cols=[config.CATEGORICAL_FEATURES],
#        handle_unknown='return_nan',
#        return_df=True,
#        use_cat_names=True,
#    )
#    df_unscaled_numeric = encoder.fit_transform(df)
#    df_types_corrected = df_unscaled_numeric.astype(np.float64)
#    return df_types_corrected


class TabularToNumeric(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass
    
    def fit(self, X: pd.DataFrame, y: pd.Series=None) -> pd.DataFrame:
        # nothing to do here, just return the dataframe as is
        return self
    
    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        # convert categorical features to numerical features
        encoder = OneHotEncoder(
            cols=[config.CATEGORICAL_FEATURES],
            handle_unknown='return_nan',
            return_df=True,
            use_cat_names=True,
        )
        X = X.copy()
        X = encoder.fit_transform(X)
        X = X.astype(np.float64)
        return X
