# Take raw stripped data from SFGov website and
import numpy
import pandas
import matplotlib.pyplot as plt
import datetime
import json

def calculate_percentiles(data, key, percentiles):
    '''data is a Series object.'''
    pct_data = numpy.zeros(len(percentiles))
    for i in range(len(percentiles)):
        pct_data[i] = int(numpy.percentile(data[key], percentiles[i]))
    
    return pct_data


infile = "test.csv"

u_cols = ['county', 'address', 'city', 'zip', 'date', 'price']

data = pandas.read_csv(infile, sep="; ", names=u_cols,
            converters={'price':lambda x: x.lstrip('$').replace(',','')} )

print data.info()

data['price'] = data['price'].astype(int)
data['date'] = pandas.to_datetime(data['date'])

print data.shape, data.info()

percentiles = range(1,99)
years = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

json_df = pandas.DataFrame(columns = ("iy", "ix", "v", "y", "x"))

# Our JSON file should be of the format:
# {"ix": 0, "iy": 0, "v":100, "x": 50, "y": 2009}
# ix - index along x (percentile index)
# iy - index along y (separate curves)
# v - y coordinate: price@percentile (in thousands of dollars)
# x - x coordinate: (percentile)
# y - year (sidebar)

# So, our DataFrame must look like:
#
# "ix", "iy", "v", "x", "y"
# 0, 1, price, percentile, year

i_df = 0
base_prices = numpy.zeros(len(percentiles))


for iy in range(len(years)):

    y = int(years[iy])

    year_data = data[ (data['date'] >= datetime.datetime(y, 1, 1)) & (data['date'] <= datetime.datetime(y, 12, 31))]

    if iy == 0:
        for ix in range(len(percentiles)):
            x = percentiles[ix]
            base_prices[ix] = numpy.percentile(year_data['price'], x)/1000
            json_df.loc[i_df] = [int(iy), int(ix), 1.0, int(y), int(x)]

            i_df+=1

    else:

        for ix in range(len(percentiles)):
            x = percentiles[ix]
            v = numpy.percentile(year_data['price'], x)/1000

            json_df.loc[i_df] = [int(iy), int(ix), v/base_prices[ix], int(y), int(x)]

            i_df+=1

            print int(iy), int(ix), v/base_prices[ix], int(y), int(x)

print i_df


# Pandas is awesome.  orient = 'records' prints as just a set of key-pairs.  See docs
# for other formats that can be exported with this awesome function.
json_df.to_json(path_or_buf='../../viz/saltzberg.github.io/sf_real_estate/sf_housing.json', 
                     orient='records')

# How to get output as integers for ix and iy?


#print data['date']

#print data[data['date'].year==2015].head(), type(data['date'][0])
#print data['price']
