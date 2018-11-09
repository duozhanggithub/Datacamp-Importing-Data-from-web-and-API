import requests
import json
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt

class RestAPIClient(object):

    def __init__(self):

        '''
        def read_sensor_data(self, sensor_id, from_ts, to_ts,
                         as_list = False,as_dict = False,as_series = False,
                         log_level = 0, log_file_handle = None, most_recent_value_only = False,
                         sensorname : str = ‘’):
        '''

    def read_sensor_data(self, sensorname, from_ts, to_ts, as_list=False,
                         as_dict=False, as_series=False):

        # GET data
        url = 'http://localhost:66/data?sensorname={}'.format(sensorname)
        r_get = requests.get(url)

        # get the timestamps(ts) and values, put them separately in two lists
        sensor_data = r_get.json()
        sensor_data_ts = [x[0] for x in sensor_data]
        sensor_data_value = [x[1] for x in sensor_data]

        # create a dataframe, dataframe easier selection between from_ts to to_ts in the next steps
        sensor_dataframe = pd.DataFrame(data=sensor_data_value, index=sensor_data_ts, columns=['Sensor Value'])
        sensor_dataframe.sort_index(inplace=True)
        # select dataframe between the desired timestamp range
        from_ts_timestamp = time.mktime(datetime.datetime.strptime(from_ts, "%d/%m/%Y").timetuple())
        to_ts_timestamp = time.mktime(datetime.datetime.strptime(to_ts, "%d/%m/%Y").timetuple())
        self.selected_sensor_dataframe = sensor_dataframe.loc[from_ts_timestamp: to_ts_timestamp]

        sensor_data_ts_selected = self.selected_sensor_dataframe.index.tolist()
        sensor_data_value_selected = self.selected_sensor_dataframe['Sensor Value'].tolist()
        self.sensor_data_list = [*map(lambda x, y: [x, y], sensor_data_ts_selected, sensor_data_value_selected)]

        # export selected timestamps and values as Panda Series, use time stamp as index, sensor_data_value as data
        if as_series == True:
            self.sensor_data_series = self.selected_sensor_dataframe['Sensor Value']
            print(self.sensor_data_series)

        # export selected timestamps and values as list, the list in format of [ [timestamp, value], [timestamp, value], [timestamp, value]]
        if as_list == True:
            print(self.sensor_data_list)

        # read requests and turn it into a dict
        if as_dict == True:
            # 1. use timestamp(ts) as key, sensor_data_value as value
            self.sensor_data_dictionary1 = dict(zip(sensor_data_ts_selected, sensor_data_value_selected))
            print(self.sensor_data_dictionary1)

            # 2. according to the json file format in your PostMan test, use 'sensorname' and 'values' as key,
            # use the user specified sensorname as key, sensor_data as value
            self.sensor_data_dictionary2 = {'sensorname': sensorname, 'values': self.sensor_data_list}
            print(self.sensor_data_dictionary2)

    '''
    def append_timeseries(self, series: list,
                          owner_collection: str,
                          common: dict):
    '''

    def append_timeseries(self, series, common):
        # POST data
        url = 'http://localhost:66/data/'
        data_to_post = json.dumps({"sensorname": post_common["sensorname"], "values": post_series})
        r_post = requests.post(url, data=data_to_post)

    def plot_sensor_data(self):
        # turn timestamps into readable date format
        readable_date = [datetime.datetime.fromtimestamp(x[0]).strftime('%Y-%m-%d %H:%M:%S') for x in self.sensor_data_list]

        x = readable_date
        y = [x[1] for x in self.sensor_data_list]

        fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(12, 5), gridspec_kw={'width_ratios': [3, 1]})
        ax[0].plot_date(x, y, marker='o', linestyle='-')
        ax[0].set_title("Time series")
        ax[0].set_ylabel("Values")
        ax[1].boxplot(y, vert=True)
        ax[1].set_title("Time series statistics")
        ax[1].get_xaxis().set_visible(False)

        fig.tight_layout()
        fig.autofmt_xdate()

        plt.show()

    def get_basic_statistics(self):
        self.sensor_data_count = self.selected_sensor_dataframe['Sensor Value'].count()
        self.sensor_data_mean = self.selected_sensor_dataframe['Sensor Value'].mean()
        self.sensor_data_median = self.selected_sensor_dataframe['Sensor Value'].median()
        self.sensor_data_max = self.selected_sensor_dataframe['Sensor Value'].max()
        self.sensor_data_min = self.selected_sensor_dataframe['Sensor Value'].min()
        self.sensor_data_std = self.selected_sensor_dataframe['Sensor Value'].std()
        self.sensor_data_skew = self.selected_sensor_dataframe['Sensor Value'].skew()
        self.sensor_data_kurt = self.selected_sensor_dataframe['Sensor Value'].kurt()


#TEST PART
rest_api_test = RestAPIClient()


print('export list:')
rest_api_test.read_sensor_data(sensorname='TEST_Duo', from_ts="17/10/2018", to_ts="25/10/2018", as_list=True,
                               as_dict=False, as_series=False)
print('type: {}'.format(type(rest_api_test.sensor_data_list)))
print()

print('export dict:')
rest_api_test.read_sensor_data(sensorname='TEST_Duo', from_ts="17/10/2018", to_ts="25/10/2018", as_list=False,
                               as_dict=True, as_series=False)
print('type: {} and {}'.format(type(rest_api_test.sensor_data_dictionary1), type(rest_api_test.sensor_data_dictionary2)))
print()

print('export Panda series:')
rest_api_test.read_sensor_data(sensorname='TEST_Duo', from_ts="17/10/2018", to_ts="25/10/2018", as_list=False,
                               as_dict=False, as_series=True)
print('type: {}'.format(type(rest_api_test.sensor_data_series)))
print()

rest_api_test.get_basic_statistics()
print('Basic statistics of time series')
print('count {}'.format(rest_api_test.sensor_data_count))
print('mean {}'.format(rest_api_test.sensor_data_mean))
print('median {}'.format(rest_api_test.sensor_data_median))
print('max {}'.format(rest_api_test.sensor_data_max))
print('min {}'.format(rest_api_test.sensor_data_min))
print('std {}'.format(rest_api_test.sensor_data_std))
print('skew {}'.format(rest_api_test.sensor_data_skew))
print('kurt {}'.format(rest_api_test.sensor_data_kurt))

rest_api_test.plot_sensor_data()

post_common = {'sensorname': 'TEST_Duo'}
post_series = [[1539985000, 12], [1539958000, 13]]
rest_api_test.append_timeseries(post_series, post_common)