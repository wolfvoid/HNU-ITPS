from flask import Flask, request, jsonify
from flask_cors import CORS
from app import app, admin
import decimal
import json
from VisionPresent.VisionPresent import Visualize

# 自定义 JSON 编码器，用于处理 Decimal 类型
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/vision/v1/top', methods=['POST'])
def vision_1():
    print("vision/v1/top")
    try:
        v = Visualize("VisionPresent/")
        v.graph_plot()
        return jsonify({'success': True, 'message': '重新计算成功'}), 200
    except FileNotFoundError as e:
        return jsonify({'success': False, 'message': '文件未找到', 'error': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'message': '值错误', 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': '未知错误', 'error': str(e)}), 500


@app.route('/vision/v2/roadrank', methods=['POST'])
def vision_2():
    print("vision/v2/top")
    try:
        data = request.get_json()
        rank = data.get('rank')
        if rank is None:
            return jsonify({'success': False, 'message': 'Rank is required'}), 400
        v = Visualize("VisionPresent/")
        v.road_rank(rank)
        return jsonify({'success': True, 'message': 'success'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/vision/v3/dayrank', methods=['POST'])
def vision_3():
    print("vision/v3/dayrank")
    try:
        v = Visualize("VisionPresent/")
        v.timeinterval_rank()
        return jsonify({'success': True, 'message': 'success'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/vision/v4/weekrank', methods=['POST'])
def vision_4():
    print("vision/v4/weekrank")
    try:
        v = Visualize("VisionPresent/")
        v.week_rank()
        return jsonify({'success': True, 'message': 'success'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/vision/traveltime', methods=['POST'])
def vision_5_8():
    print("vision/traveltime")
    try:
        data = request.get_json()
        status = data.get('status')
        ids = data.get('roads')
        v = Visualize("VisionPresent/")
        method = "/other.png"


        if status == "months":
            method = "Month"
        elif status == "amonth":
            method = "Date_no"
        elif status == "aday":
            method = "Hour"
        elif status == "aweek":
            method = "Day"
        else:
            return jsonify({'success': False, 'message': "wrong method"}), 500

        #match只能在python3.10及以上版本使用
        # match status:
        #     case "months":
        #         method = "Month"
        #     case "amonth":
        #         method = "Date_no"
        #     case "aday":
        #         method = "Hour"
        #     case "aweek":
        #         method = "Day"
        #     case "_":
        #         return jsonify({'success': False, 'message': "wrong method"}), 500
        v.traveltime_plot(method, ids)
        return jsonify({'success': True, 'message': 'success'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
