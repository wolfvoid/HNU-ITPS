import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time
import networkx as nx
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class Visualize:
    def __init__(self, path=''):
        if path=='':
            temp = '../'
        else:
            temp=''
        self.data_root = temp + '../origin_data/gy_link_travel_time_part1/gy_link_travel_time_part1.txt'
        self.link_top_root = temp + '../origin_data/gy_link_top.txt'
        self.img_folder = temp + '../frontend/public/images'
        self.color = path + 'color.txt'

        self.data = pd.read_csv(self.data_root,delimiter=';',dtype={'link_ID':object})
        self.data['start_time'] =pd.to_datetime(self.data['time_interval'].str.split(',').str[0].str.strip('['))
        self.data.sort_values(by=['link_ID','start_time'],ascending=[True, True],inplace=True)
        self.data.drop(columns=['date','time_interval',],inplace=True)
        self.link_top = pd.read_csv(self.link_top_root,delimiter=';',dtype={'link_ID':object,'in_links':object,'out_links':object})
        self.link_top['in_links'] = self.link_top['in_links'].fillna('')
        self.link_top['out_links'] = self.link_top['out_links'].fillna('')

    def graph_plot(self):
        '''
        link_traveltime: 给出每一条路的通行时间
        '''
        # 读取颜色映射数据
        weight = pd.read_csv(self.color, delimiter=';', dtype={'link_ID': object})
        link_traveltime = {row['link_ID']: row['weight'] for _, row in weight.iterrows()}
        plt.figure(figsize=(120, 80))
        G = nx.DiGraph()
        # 构建有向图
        for _, row in self.link_top.iterrows():
            link_id = row['link_ID']
            in_links = row['in_links'].split("#") if row['in_links'] else []
            out_links = row['out_links'].split("#") if row['out_links'] else []
            for in_link in in_links:
                G.add_edge(in_link, link_id)
            for out_link in out_links:
                G.add_edge(link_id, out_link)
        # 计算节点布局
        layout = nx.kamada_kawai_layout(G)
        cmap = plt.get_cmap('coolwarm') # 曾用Spectral_r
        # 获取节点的值，并且处理超过level的情况
        node_values = [link_traveltime.get(node, 0) for node in G.nodes()]
        max_value = np.percentile(node_values, 90) if node_values else 1
        # 如果节点值超过level，则限制到level值
        for i in range(len(node_values)):
            if node_values[i] > max_value:
                node_values[i] = max_value
        # 计算节点颜色，确保颜色映射平滑
        # print(max_value)
        node_colors = [cmap(value / max_value) for value in node_values]
        # 绘制图像
        nx.draw(G, pos=layout, with_labels=True, node_color=node_colors, node_size=10000, edge_color='lightgrey', width=30,
                font_size=40, font_weight='bold', arrows=True, arrowsize=200)
        # 创建颜色条位置
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", size="3%", pad=0.5)
        # 添加图例
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(vmin=0, vmax=max_value))
        sm.set_array([])  # 仅用于图例
        plt.colorbar(sm, cax=cax, label='Link Travel Time')  # 使用指定的cax
        # 保存图像
        image_path = self.img_folder + "/v1.png"
        plt.savefig(image_path)
        return image_path

    def traveltime_plot2(self, mthd="Month", ids=['4377906283525800514','4377906287141600514']):
        '''
        mthd:
            Month: 不同路段在不同月分平均通行时间的变化
            Date_no: 不同路段在一个月之内平均通行时间变化
            Hour: 不同路段在一天之内平均通行时间变化
            Day: 不同路段在一周之内平均通行时间变化
        ids: 分析路段

        '''
        if mthd not in self.data.columns:
            if mthd == "Month":
                self.data["Month"]= self.data['start_time'].dt.month
            elif mthd == "Date_no":
                self.data["Date_no"]= self.data['start_time'].dt.day
            elif mthd == "Hour":
                self.data["Hour"]= self.data['start_time'].dt.hour
            elif mthd == "Day":
                self.data["Day"]= self.data.start_time.dt.strftime("%A")

        plt.figure()
        df_month = self.data.groupby(["link_ID",mthd]).agg({"travel_time":"mean"}).reset_index()
        for id in ids:
            df_filtered = df_month[df_month['link_ID'] == id]
            plt.plot(df_filtered[mthd], df_filtered['travel_time'], label=id)
        plt.legend(title='Link ID', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title('Travel Time for Different Link IDs')
        plt.xlabel(mthd)
        plt.ylabel('Average Travel Time')
        plt.xticks(rotation=45)
        plt.tight_layout()

        method = "/other.png"

        if mthd == "Month":
            method = "/v5.png"
        elif mthd == "Date_no":
            method = "/v6.png"
        elif mthd == "Hour":
            method = "/v7.png"
        elif mthd == "Day":
            method = "/v8.png"
        else:
            method = "/other.png"
        # match只能在python3.10及以上版本使用
        # match mthd:
        #     case "Month":
        #         method = "/v5.png"
        #     case "Date_no":
        #         method = "/v6.png"
        #     case "Hour":
        #         method = "/v7.png"
        #     case "Day":
        #         method = "/v8.png"
        #     case "_":
        #         method = "/other.png"
        image_path = self.img_folder + method
        plt.savefig(image_path)
        return image_path

    def traveltime_plot(self, mthd="Month", ids=['4377906283525800514', '4377906287141600514', '9377906286566510514']):
        '''
        mthd:
            Month: 不同路段在不同月分平均通行时间的变化
            Date_no: 不同路段在一个月之内平均通行时间变化
            Hour: 不同路段在一天之内平均通行时间变化
            Day: 不同路段在一周之内平均通行时间变化
        ids: 分析路段
        '''
        if mthd not in self.data.columns:
            if mthd == "Month":
                self.data["Month"] = self.data['start_time'].dt.month
            elif mthd == "Date_no":
                self.data["Date_no"] = self.data['start_time'].dt.day
            elif mthd == "Hour":
                self.data["Hour"] = self.data['start_time'].dt.hour
            elif mthd == "Day":
                self.data["Day"] = self.data.start_time.dt.strftime("%A")

        plt.figure()
        df_month = self.data.groupby(["link_ID", mthd]).agg({"travel_time": "mean"}).reset_index()

        # 使用渐变色彩表
        cmap = cm.get_cmap('viridis', len(ids))  # 选择一个渐变色彩表，比如 'viridis'

        for i, id in enumerate(ids):
            df_filtered = df_month[df_month['link_ID'] == id]
            plt.plot(df_filtered[mthd], df_filtered['travel_time'], label=id, color=cmap(i))

        plt.legend(title='Link ID', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title('Travel Time for Different Link IDs')
        plt.xlabel(mthd)
        plt.ylabel('Average Travel Time')
        plt.xticks(rotation=45)
        plt.tight_layout()

        method = "/other.png"


        if mthd == "Month":
            method = "/v5.png"
        elif mthd == "Date_no":
            method = "/v6.png"
        elif mthd == "Hour":
            method = "/v7.png"
        elif mthd == "Day":
            method = "/v8.png"
        else:
            method = "/other.png"


        # match mthd:
        #     case "Month":
        #         method = "/v5.png"
        #     case "Date_no":
        #         method = "/v6.png"
        #     case "Hour":
        #         method = "/v7.png"
        #     case "Day":
        #         method = "/v8.png"
        #     case "_":
        #         method = "/other.png"
        image_path = self.img_folder + method
        plt.savefig(image_path)
        return image_path

    def road_rank(self, nums=10):
        '''
            路段通行时间排序输出，输出通行时间最长的nums条路
        '''
        plt.figure(figsize=(10, 6))  # 设置图形的宽度和高度
        df_ID = self.data.groupby("link_ID").agg({"travel_time": "mean"}).reset_index().sort_values(by="travel_time",                                                                                     ascending=False)
        x = df_ID.head(nums)['link_ID'].to_list()
        x.reverse()
        y = df_ID.head(nums)['travel_time'].to_list()
        y.reverse()
        plt.barh(x, y, color='skyblue')
        plt.ylabel('Road ID', fontsize=12)  # 设置y轴标签的字体大小
        plt.xlabel('Average Travel Time', fontsize=12)  # 设置x轴标签的字体大小
        plt.title(f"Travel Time top-{nums}", fontsize=14)  # 设置标题的字体大小
        # 调整边距
        plt.subplots_adjust(left=0.2)  # 增加左边距

        image_path = self.img_folder + "/v2.png"
        plt.savefig(image_path)
        return image_path

    def timeinterval_rank(self):
        '''
        输出一天之内的按时间段划分的通行时间排序
        '''
        plt.figure()  
        if "Hour" not in self.data.columns:
            self.data["Hour"]= self.data['start_time'].dt.hour
        h = {}
        h["凌晨"] = self.data[(self.data['Hour']>=1) & (self.data['Hour']<5)]['travel_time'].mean()
        h["早上"] = self.data[(self.data['Hour']>=5) & (self.data['Hour']<8)]['travel_time'].mean()
        h["上午"] = self.data[(self.data['Hour']>=8) & (self.data['Hour']<11)]['travel_time'].mean()
        h["中午"] = self.data[(self.data['Hour']>=11) & (self.data['Hour']<13)]['travel_time'].mean()
        h["下午"] = self.data[(self.data['Hour']>=13) & (self.data['Hour']<17)]['travel_time'].mean()
        h["傍晚"] = self.data[(self.data['Hour']>=17) & (self.data['Hour']<19)]['travel_time'].mean()
        h["晚上"] = self.data[(self.data['Hour']>=19) & (self.data['Hour']<23)]['travel_time'].mean()
        h["午夜"] = self.data[(self.data['Hour']==23) | (self.data['Hour']==0)]['travel_time'].mean()
        sorted_h = dict(sorted(h.items(), key=lambda item: item[1], reverse=False))
        plt.figure(figsize=(10, 6))
        plt.barh(list(sorted_h.keys()),sorted_h.values(), color='lightcoral')
        plt.xlabel('Average Travel Time')
        plt.ylabel('Time Interval')

        image_path = self.img_folder + "/v3.png"
        plt.savefig(image_path)
        return image_path

    def week_rank(self):
        '''
        一周内排序
        '''
        plt.figure()  
        if "Day" not in self.data.columns:
            self.data["Day"]= self.data.start_time.dt.strftime("%A")
        df_day = self.data.groupby("Day").agg({"travel_time":"mean"}).reset_index().sort_values(by="travel_time",ascending=False)
        x = df_day['Day'].to_list()
        x.reverse()
        y = df_day['travel_time'].to_list()
        y.reverse()
        plt.barh(x,y, color='skyblue')
        plt.ylabel('Day')
        plt.xlabel('Average Travel Time')
        plt.title(f"Travel Time Rank in a week")

        image_path = self.img_folder + "/v4.png"
        plt.savefig(image_path)
        return image_path

    
if __name__ == '__main__':
    t = Visualize()
    # t.road_rank()
    # t.week_rank()
    # t.timeinterval_rank()
    t.traveltime_plot(mthd="Month")
    t.traveltime_plot(mthd="Date_no")
    t.traveltime_plot(mthd="Hour")
    t.traveltime_plot(mthd="Day")
    # t.graph_plot()

