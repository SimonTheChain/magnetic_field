#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from category_encoders import OneHotEncoder

import config


# impute missing values
def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    my_imputer = SimpleImputer(strategy="most_frequent", add_indicator=True, copy=True)
    df_unscaled = pd.DataFrame(my_imputer.fit_transform(df))
    df_unscaled.columns = df.columns
    return df_unscaled

# change tabular into numeric
def tabular_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    encoder = OneHotEncoder(
        cols=[config.CATEGORICAL_FEATURES],
        handle_unknown='return_nan',
        return_df=True,
        use_cat_names=True,
    )
    df_unscaled_numeric = encoder.fit_transform(df)
    df_types_corrected = df_unscaled_numeric.astype(np.float64)
    return df_types_corrected
