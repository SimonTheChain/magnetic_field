#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

import magnetic_field.processing.preprocessors as pp


magnetic_field_pipe = Pipeline(
    [
        ("Simple Imputer", pp.SimpleImputer()),
        ("Regressor", RandomForestRegressor()),
      ]
)
