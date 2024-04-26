"""
 Author: Matt Hanson
 Created: 12/02/2021 12:24 PM
 """
import pandas as pd
import os

def get_output_metadata(return_dict=True):
    """
    note all keys are have been made uppper for consistancy.

    :param return_dict: boolean True return nested dictionary, otherwies returne dataframe
    :return:
    """
    data = pd.read_csv(os.path.join(os.path.dirname(__file__),'output_description.csv'))
    data.loc[:,'key'] = data.loc[:,'key'].str.upper()
    data = data.set_index('key')
    if return_dict:
        return data.transpose().to_dict()
    else:
        return data

if __name__ == '__main__':
    t = get_output_metadata()

    pass