import pandas as pd
import numpy as np
import joblib

class My_predict:
    def __init__(self, path=''):
        self.info = path + 'gy_contest_link_info.txt'
        self.top = path + 'gy_contest_link_top.txt'
        self.model_path = path + 'model/xgbr.pkl'
        pass

    def create_lagging(self, df, df_original, i):
        # 创建滞后特征，返回合并后的数据框
        df1 = df_original.copy()
        df1['time_interval_begin'] = df1['time_interval_begin'] + pd.DateOffset(minutes=i * 2)
        df1 = df1.rename(columns={'travel_time': 'lagging' + str(i)})
        df2 = pd.merge(df, df1[['link_ID', 'time_interval_begin', 'lagging' + str(i)]],
                       on=['link_ID', 'time_interval_begin'],
                       how='left')
        return df2

    def mean_time(self, group):
        group['link_ID_en'] = group['travel_time'].mean()
        return group

    def predict(self, path, model_path):
        df = pd.read_csv( path , delimiter=';', dtype={'link_ID': object})
        df['time_interval_begin'] = pd.to_datetime(df['time_interval'].map(lambda x: x[1:20]))
        df = df.drop(['time_interval'], axis=1)
        df1 = df.copy()
        df1['time_interval_begin'] = df1['time_interval_begin'] + pd.DateOffset(minutes=5 * 2)
        df1 = df1.rename(columns={'travel_time': 'lagging' + str(5)})
        df2 = pd.merge(df, df1[['link_ID', 'time_interval_begin', 'lagging' + str(5)]], on=['link_ID', 'time_interval_begin'],how='left')
        df1 = self.create_lagging(df, df, 1)
        lagging = 5
        for i in range(2, lagging + 1):
            df1 = self.create_lagging(df1, df, i)
        link_infos = pd.read_csv(self.info, delimiter=';', dtype={'link_ID': object})
        link_tops = pd.read_csv(self.top, delimiter=',', dtype={'link_ID': object})
        link_tops = link_tops.fillna(0)
        link_infos = pd.merge(link_infos, link_tops, on=['link_ID'], how='left')
        link_infos['links_num'] = link_infos["in_links"]+link_infos["out_links"]
        link_infos['area'] = link_infos['length'] * link_infos['width']
        df2 = pd.merge(df1, link_infos[['link_ID', 'length', 'width', 'links_num', 'area']], on=['link_ID'], how='left')

        # 假期特征
        df2.loc[df2['date'].isin(
            ['2017-04-02', '2017-04-03', '2017-04-04', '2017-04-29', '2017-04-30', '2017-05-01',
            '2017-05-28', '2017-05-29', '2017-05-30']), 'vacation'] = 1
        df2.loc[~df2['date'].isin(
            ['2017-04-02', '2017-04-03', '2017-04-04', '2017-04-29', '2017-04-30', '2017-05-01',
            '2017-05-28', '2017-05-29', '2017-05-30']), 'vacation'] = 0

        # 起始分钟特征
        df2.loc[df2['time_interval_begin'].dt.hour.isin([6, 7, 8]), 'minute_series'] = \
            df2['time_interval_begin'].dt.minute + (df2['time_interval_begin'].dt.hour - 6) * 60

        df2.loc[df2['time_interval_begin'].dt.hour.isin([13, 14, 15]), 'minute_series'] = \
            df2['time_interval_begin'].dt.minute + (df2['time_interval_begin'].dt.hour - 13) * 60

        df2.loc[df2['time_interval_begin'].dt.hour.isin([16, 17, 18]), 'minute_series'] = \
            df2['time_interval_begin'].dt.minute + (df2['time_interval_begin'].dt.hour - 16) * 60

        # 星期特征
        df2['day_of_week'] = df2['time_interval_begin'].map(lambda x: x.weekday() + 1)
        df2.loc[df2['day_of_week'].isin([1, 2, 3]), 'day_of_week_en'] = 1
        df2.loc[df2['day_of_week'].isin([4, 5]), 'day_of_week_en'] = 2
        df2.loc[df2['day_of_week'].isin([6, 7]), 'day_of_week_en'] = 3

        # 时间段特征
        # 这里有我的改动，因为原本只需要一部分的时间，但是为了可以随意选择时间，这里将全天的时间划分成三个部分
        df2.loc[df['time_interval_begin'].dt.hour.isin([1, 2, 3, 4, 6, 7, 8]), 'hour_en'] = 1
        df2.loc[df['time_interval_begin'].dt.hour.isin([9, 10, 11, 12, 13, 14, 15]), 'hour_en'] = 2
        df2.loc[df['time_interval_begin'].dt.hour.isin([16, 17, 18, 19, 20, 21, 22, 23, 24]), 'hour_en'] = 3

        # 星期，时间段合并特征
        df2['week_hour'] = df2["day_of_week_en"].astype('str') + "," + df2["hour_en"].astype('str')
        df2 = pd.get_dummies(df2, columns=['week_hour', 'links_num', 'width'])
        df2 = df2.groupby('link_ID').apply(self.mean_time)
        sorted_link = np.sort(df2['link_ID_en'].unique())
        df2['link_ID_en'] = df2['link_ID_en'].map(lambda x: np.argmin(x >= sorted_link))
        df2 = df2.reset_index(drop=True)
        df1_set = {'width_15', 'hour_en', 'week_hour_2.0,2.0', 'week_hour_3.0,3.0', 'area', 'width_9', 'week_hour_2.0,1.0', 'time_interval_begin', 'width_12', 'week_hour_3.0,1.0', 'length', 'date', 'links_num_2', 'week_hour_1.0,1.0', 'links_num_3', 'week_hour_2.0,3.0', 'lagging3', 'lagging4', 'link_ID', 'week_hour_1.0,2.0', 'links_num_4', 'week_hour_1.0,3.0', 'imputation1', 'width_6', 'links_num_5', 'day_of_week_en', 'minute_series', 'vacation', 'lagging2', 'width_3', 'week_hour_3.0,2.0', 'lagging1', 'travel_time', 'day_of_week', 'link_ID_en', 'lagging5'}
        all_columns = set(df1_set).union(df2.columns)

        # 扩展 df2，添加 df1 中的列，缺失的列填充为 0
        df2 = df2.reindex(columns=all_columns, fill_value=0)
        df = df2.copy()

        lagging = 5
        lagging_feature = ['lagging%01d' % e for e in range(lagging, 0, -1)]
        # lagging_feature

        base_feature = [x for x in df.columns.values.tolist() if x not in ['time_interval_begin', 'link_ID', 'link_ID_int',
                                                                        'date', 'travel_time', 'imputation1',
                                                                        'minute_series', 'area', 'hour_en', 'day_of_week']]

        base_feature = [x for x in base_feature if x not in lagging_feature]

        train_feature = list(base_feature)
        train_feature.extend(lagging_feature)
        # print(train_feature)
        test_df = df2.iloc[[-1]].copy()
        # test_df = df2[].copy()

        test_X = test_df[train_feature]

        regressor = joblib.load(model_path)
        y_prediction = regressor.predict(test_X.values)

        test_df['lagging5'] = test_df['lagging4']
        test_df['lagging4'] = test_df['lagging3']
        test_df['lagging3'] = test_df['lagging2']
        test_df['lagging2'] = test_df['lagging1']
        test_df['lagging1'] = y_prediction

        test_df['predicted'] = np.expm1(y_prediction)
        test_df['time_interval_begin'] = test_df['time_interval_begin'] + pd.DateOffset(minutes=2)
        test_df['time_interval'] = test_df['time_interval_begin'].map(
            lambda x: '[' + str(x) + ',' + str(x + pd.DateOffset(minutes=2)) + ')')
        test_df.time_interval = test_df.time_interval.astype(object)

        test_df[['link_ID', 'date', 'time_interval', 'predicted']]

        return test_df[['link_ID', 'date', 'time_interval', 'predicted']]

    def transform_data(self, data):
        transformed_data = []
        for entry in data:
            # 提取时间区间
            time_interval = entry['time_interval']
            time_start, time_end = time_interval.strip('[]()').split(',')
            time_start = time_start.split(' ')[1]
            time_end = time_end.split(' ')[1]

            # 构建新的字典，符合指定结构
            transformed_entry = {
                'ID': entry['link_ID'],
                'Date': entry['date'],
                'Start_Time': time_start,
                'End_Time': time_end,
                'Value': entry['predicted']
            }
            transformed_data.append(transformed_entry)

        # 返回转换后的数据和总行数
        return transformed_data, len(transformed_data)

    def run_predict(self, data_path='data/data.txt'):
        ans = self.predict(data_path, self.model_path)
        transformed_data, total_rows = self.transform_data(ans.to_dict(orient='records'))
        return {'success': True, 'rows': transformed_data, 'total': total_rows}


if __name__=="__main__":
    my_predict = My_predict()
    print(my_predict.run_predict())