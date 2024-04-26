"""
 Author: Matt Hanson
 Created: 14/10/2021 8:50 AM
 """
import pandas as pd
import numpy as np


def make_cumuliative_annual(inseries, start_day, start_month):
    """

    :param inseries: pd.Series with
    :param start_day: int start day of the month (e.g. 1-31 for jan for calendar or 1jun for water year)
    :param start_month: int start month (e.g. jan for calendar or jun for water year)
    :return:
    """
    assert isinstance(start_day, int)
    assert isinstance(start_month, int)
    assert isinstance(inseries, pd.Series)
    out_data = pd.Series(index=inseries.index)

    years = pd.unique(inseries.index.year)
    start_date = pd.to_datetime(f'{years.min()-1}-{start_month:02d}-{start_day:02d}')
    for i in range(len(years)+1):
        end_date = start_date + pd.DateOffset(years=1, days=-1)
        idx = (inseries.index.date >= start_date) & (inseries.index.date <= end_date)
        out_data.loc[idx] = inseries.loc[idx].cumsum()

        start_date = end_date + pd.DateOffset(days=1)
    return out_data

if __name__ == '__main__':
    np.random.seed(55)
    test_data = pd.DataFrame(index=pd.date_range('2002-01-01', '2005-08-25'))
    test_data.loc[:, 'test_flow'] = np.random.randint(0,5,len(test_data))
    test_data.loc[:,'cum_sum'] = make_cumuliative_annual(test_data.loc[:,'test_flow'], 1,7)
    pass