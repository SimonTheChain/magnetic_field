#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

import magnetic_field.config.config as config
import magnetic_field.processing.data_management as data_management
import magnetic_field.processing.preprocessors as preprocessors
import pipeline


# import data
data_management.download_data_files()
df = data_management.load_datasets()

# identify target and predictors variables
df_target = df[config.TARGET_FEATURE]
df_predictors = df.drop([config.TARGET_FEATURE], axis=1)

# split the dataset in training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df_predictors,
    df_target,
    train_size=0.8,
    test_size=0.2,
    random_state=10,
)

# process data through pipeline
pipeline.magnetic_field_pipe.fit(X_train, y_train)

# make predictions
preds = pipeline.magnetic_field_pipe.predict(X_test)

# evaluate model
score = pipeline.magnetic_field_pipe.score(X_test, y_test)
print("Model score: {}".format(score))
