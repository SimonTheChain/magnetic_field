#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# # Predicting the intensity of the magnetic field experienced by satellites in Earth orbit
# ## Dataset: https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/search/?Plane.position.bounds@Shape1Resolver.value=ALL&Observation.collection=MOST&Observation.instrument.name=Direct%20image&Observation.type=object#sortCol=caom2%3APlane.time.bounds.lower&sortDir=dsc&col_1=_checkbox_selector;;;&col_2=caom2%3AObservation.uri;;;&col_3=caom2%3APlane.productID;;;&col_4=caom2%3AObservation.target.name;;;&col_5=caom2%3APlane.position.bounds.cval1;;;&col_6=caom2%3APlane.position.bounds.cval2;;;&col_7=caom2%3APlane.time.bounds.lower;;;&col_8=caom2%3AObservation.instrument.name;;;&col_9=caom2%3APlane.time.exposure;;;&col_10=caom2%3AObservation.proposal.pi;;;&col_11=caom2%3AObservation.proposal.id;;;&col_12=caom2%3APlane.calibrationLevel;;;&col_13=caom2%3AObservation.observationID;;;


# internal imports
import os
import tarfile

# external imports
import pandas as pd
from astropy.io import fits
from cadcdata import StorageInventoryClient
from sklearn.impute import SimpleImputer
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# ### Config Variables
DATASETS_PATH = "./datasets/most/"
DATA_DOWNLOAD_LIST = "./datasets/most/cadcUrlList_test.txt"

COLUMNS = [
    "[DEGREES] LONGITUDE OF SATELLITE",
    "[DEGREES] LATITUDE OF SATELLITE",
    "[M] ALTITUDE OF SATELLITE",
    "[DEGREES] ANGLE TO EARTH LIMB",
    "[DEGREES] NADIR RIGHT ASCENSION",
    "[DEGREES] NADIR DECLINATION",
    "[DEGREES] NADIR LONGITUDE",
    "[DEGREES] NADIR LATITUDE",
    "[DEGREES] SOLAR RIGHT ASCENSION",
    "[DEGREES] SOLAR DECLINATION",
    "[DEGREES] SOLAR ALTITUDE",
    "[DEGREES] SOLAR AZIMUTH",
    "[DEGREES] SOLAR LONGITUDE",
    "[DEGREES] SOLAR LATITUDE",
    "[DEGREES] LUNAR RIGHT ASCENSION",
    "[DEGREES] LUNAR DECLINATION",
    "[DEGREES] LUNAR ALTITUDE",
    "[DEGREES] LUNAR AZIMUTH",
    "[DEGREES] LUNAR LONGITUDE",
    "[DEGREES] LUNAR LATITUDE",
    "[DEGREES] LUNAR-TARGET ANGULAR SEPERATION",
    "[nT] MAGNETIC FIELD STRENGTH",
]

CATEGORICAL_FEATURES = [
    "[DEGREES] SOLAR ALTITUDE",
    "[DEGREES] SOLAR AZIMUTH",
    "[DEGREES] SOLAR LONGITUDE",
]

TARGET_FEATURE = "[nT] MAGNETIC FIELD STRENGTH"

# ### Data Collection
client = StorageInventoryClient()

# download data as a list of *.tar files from a web search
with open(DATA_DOWNLOAD_LIST, "r") as to_download:
    for row in to_download:
        f = row.split("cadc:")[1]
        client.cadcget(f, DATASETS_PATH)

df_list = list()
df = pd.DataFrame(
    columns=[COLUMNS]
)

for root, dirs, files in os.walk(DATASETS_PATH):
    for f in files:
        
        # for every .tar file in the datasets directory
        if os.path.splitext(f)[1] == ".tar":

            with tarfile.open(
                name=os.path.join(root, f),
                mode="r"
            ) as tar_obj:

                # for every file in the tar file
                for member in tar_obj.getnames():
                    if os.path.splitext(member)[1] == ".fits":

                        # extract .tar file in memory
                        extracted = tar_obj.extractfile(member)

                        # open extracted .fits file
                        with fits.open(extracted) as hdul:
                            hdr = hdul[0].header
                            data_dct = {
                                "[DEGREES] LONGITUDE OF SATELLITE": hdr["SAT_LONG"],
                                "[DEGREES] LATITUDE OF SATELLITE": hdr["SAT_LAT"],
                                "[M] ALTITUDE OF SATELLITE": hdr["SAT_ALT"],
                                "[DEGREES] ANGLE TO EARTH LIMB": hdr["ELA_ANG"],
                                "[DEGREES] NADIR RIGHT ASCENSION": hdr["NAD_RA"],
                                "[DEGREES] NADIR DECLINATION": hdr["NAD_DEC"],
                                "[DEGREES] NADIR LONGITUDE": hdr["NAD_PHI"],
                                "[DEGREES] NADIR LATITUDE": hdr["NAD_THET"],
                                "[DEGREES] SOLAR RIGHT ASCENSION": hdr["SOL_RA"],
                                "[DEGREES] SOLAR DECLINATION": hdr["SOL_DEC"],
                                "[DEGREES] SOLAR ALTITUDE": ["SOL_ALTI"],
                                "[DEGREES] SOLAR AZIMUTH": ["SOL_AZIM"],
                                "[DEGREES] SOLAR LONGITUDE": ["SOL_PHI"],
                                "[DEGREES] SOLAR LATITUDE": hdr["SOL_THET"],
                                "[DEGREES] LUNAR RIGHT ASCENSION": hdr["LUN_RA"],
                                "[DEGREES] LUNAR DECLINATION": hdr["LUN_DEC"],
                                "[DEGREES] LUNAR ALTITUDE": hdr["LUN_ALTI"],
                                "[DEGREES] LUNAR AZIMUTH": hdr["LUN_AZIM"],
                                "[DEGREES] LUNAR LONGITUDE": hdr["LUN_PHI"],
                                "[DEGREES] LUNAR LATITUDE": hdr["LUN_THET"],
                                "[DEGREES] LUNAR-TARGET ANGULAR SEPERATION": hdr["LUN_SEP"],
                                "[nT] MAGNETIC FIELD STRENGTH": hdr["MAG_FLD"],
                            }
                            df_partial = pd.DataFrame(data_dct)
                            df_list.append(df_partial)

df_source = pd.concat(df_list, ignore_index=True)


# ### Data Cleaning and Pre-Processing
# identify target and predictor features
df_target = df_source[TARGET_FEATURE]
df_predictors = df_source.drop([TARGET_FEATURE], axis=1)

# drop categorical features to simplify the process
df_predictors = df_predictors.drop(CATEGORICAL_FEATURES, axis=1)

# split data in training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df_predictors, 
    df_target,
    train_size=0.8, 
    test_size=0.2, 
    random_state=10,
)

# impute missing values
imputer = SimpleImputer()
imputed_X_train = imputer.fit_transform(X_train)
imputed_X_test = imputer.transform(X_test)

# normalize data
scaler = preprocessing.StandardScaler()
scaled_imputed_X_train_plus = scaler.fit_transform(imputed_X_train)
scaled_imputed_X_test_plus = scaler.transform(imputed_X_test)

# ### Baseline model training and validation
# train model
model = RandomForestRegressor()
model.fit(scaled_imputed_X_train_plus, y_train)

# make predictions
preds = model.predict(scaled_imputed_X_test_plus)

# evaluate model
mean_absolute_error(y_test, preds)
print("First five predictions: ", ", ".join(str(p) for p in preds[:5].tolist()))