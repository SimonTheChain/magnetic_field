#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

import magnetic_field.processing.preprocessors as pp


magnetic_field_pipe = Pipeline(
    [
        ("Most Frequent Imputer", pp.FrequentImputer()),
        ("Tabular to Numeric", pp.TabularToNumeric()),
        ("Regressor", RandomForestRegressor()),
      ]
)
