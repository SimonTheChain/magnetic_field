#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import tarfile

import pandas as pd
from astropy.io import fits
from cadcdata import StorageInventoryClient

import magnetic_field.config.config as config


def download_data_files():
    client = StorageInventoryClient()

    # download data as a list of *.tar files from a web search
    with open(config.DATA_DOWNLOAD_LIST, "r") as to_download:
        for row in to_download:
            f = row.split("cadc:")[1]
            client.cadcget(f, config.DATASETS_PATH)

def load_datasets() -> pd.DataFrame:
    df_list = list()
    df = pd.DataFrame(
        columns=[config.COLUMNS]
    )

    for root, dirs, files in os.walk(config.DATASETS_PATH):
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

    df = pd.concat(df_list, ignore_index=True)
    return df