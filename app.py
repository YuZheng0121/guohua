#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国绘画分析WebUI
功能：
1. 首页：统计图表
2. 图片查看：关键点+检测结果开关
"""

import os
import json
import csv
from flask import Flask, render_template, jsonify, send_from_directory, request
from collections import Counter

app = Flask(__name__)

# 数据路径
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')
CSV_DIR = '/root/yolo/data/classified'

# 加载数据
print("加载数据...")
with open(os.path.join(DATA_DIR, 'pose_results_all.json'), 'r', encoding='utf-8') as f:
    pose_data = json.load(f)

with open(os.path.join(DATA_DIR, 'merged_results.json'), 'r', encoding='utf-8') as f:
    detection_data = json.load(f)

# 加载CSV获取朝代信息
dynasty_map = {}
csv_files = ['画作信息_男.csv', '画作信息_女.csv', '画作信息_有男有女.csv', '画作信息_点景人物.csv']
for csv_file in csv_files:
    csv_path = os.path.join(CSV_DIR, csv_file)
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                img_id = row.get('imageID', '')
                dynasty = row.get('dynasty', '')
                if img_id and dynasty:
                    dynasty_map[img_id] = dynasty

print("朝代信息: {}条".format(len(dynasty_map)))

# 建立索引
pose_dict = {item['image_id']: item for item in pose_data}
detection_dict = {item['uuid']: item for item in detection_data}

# 添加朝代信息到detection_dict
for uuid in detection_dict:
    if uuid in dynasty_map:
        detection_dict[uuid]['dynasty'] = dynasty_map[uuid]

print("姿态数据: {}张".format(len(pose_data)))
print("检测数据: {}张".format(len(detection_data)))

@app.route('/')
def index():
    """首页 - 统计概览"""
    return render_template('index.html')

@app.route('/images')
def images_page():
    """图片查看页面"""
    return render_template('images.html')

@app.route('/shinu')
def shinu_page():
    """明清仕女图典藏页面"""
    return render_template('shinu.html')

@app.route('/api/shinu52')
def get_shinu52():
    """返回52张明清仕女图数据（含检测结果）"""
    data_file = os.path.join(DATA_DIR, 'shinu_52_website.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/mingqing_ids')
def get_mingqing_ids():
    """返回明清仕女图ID列表"""
    ids_file = os.path.join(DATA_DIR, 'mingqing_ids.json')
    if os.path.exists(ids_file):
        with open(ids_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/public_copyright_ids')
def get_public_copyright_ids():
    """返回公开版权图片ID列表（按分类）"""
    # 支持按分类查询：?category=男
    category = request.args.get('category')
    ids_file = os.path.join(DATA_DIR, 'public_copyright_by_category.json')
    if os.path.exists(ids_file):
        with open(ids_file, 'r') as f:
            data = json.load(f)
        if category:
            return jsonify(data.get(category, []))
        # 不指定分类时返回所有
        all_ids = []
        for cat_ids in data.values():
            all_ids.extend(cat_ids)
        return jsonify(list(set(all_ids)))
    return jsonify([])

@app.route('/api/stats')
def get_stats():
    """统计数据API"""
    # 物体频率
    label_freq = Counter()
    for item in detection_data:
        for label in item.get('labels', []):
            label_freq[label] += 1

    # 朝代分布（从category推断）
    category_freq = Counter()
    for item in detection_data:
        category_freq[item.get('category', '未知')] += 1

    # 性别分类
    gender_freq = Counter()
    for item in detection_data:
        cat = item.get('category', '')
        if '女' in cat:
            gender_freq['女性'] += 1
        elif '男' in cat:
            gender_freq['男性'] += 1
        else:
            gender_freq['其他'] += 1

    return jsonify({
        'total_images': len(detection_data),
        'label_freq': dict(label_freq.most_common(15)),
        'category_freq': dict(category_freq.most_common(10)),
        'gender_freq': dict(gender_freq)
    })

@app.route('/api/images')
def get_images():
    """图片列表API"""
    images = []
    for uuid, item in detection_dict.items():
        images.append({
            'uuid': uuid,
            'category': item.get('category', ''),
            'labels': item.get('labels', []),
            'num_detections': item.get('num_detections', 0),
            'dynasty': item.get('dynasty', ''),
            'detection': {
                'labels': item.get('labels', []),
                'num_detections': item.get('num_detections', 0),
                'detections': item.get('detections', [])
            }
        })
    return jsonify(images)  # 返回全部图片

@app.route('/api/image/<uuid>')
def get_image_detail(uuid):
    """单张图片详情API"""
    result = {
        'uuid': uuid,
        'pose': None,
        'detection': None
    }

    if uuid in pose_dict:
        pose_item = pose_dict[uuid]
        # 只返回高置信度的关键点
        keypoints = []
        for kp in pose_item.get('keypoints', []):
            if len(kp) >= 3 and kp[2] > 0.3:
                keypoints.append({'x': kp[0], 'y': kp[1], 'confidence': kp[2]})
        result['pose'] = {
            'keypoints': keypoints,
            'total_keypoints': len(pose_item.get('keypoints', [])),
            'image_size': pose_item.get('image_size', [])
        }

    if uuid in detection_dict:
        det_item = detection_dict[uuid]
        result['detection'] = {
            'labels': det_item.get('labels', []),
            'detections': det_item.get('detections', []),
            'num_detections': det_item.get('num_detections', 0)
        }

    return jsonify(result)

@app.route('/api/thumb/<uuid>')
def get_thumbnail(uuid):
    """返回图片缩略图 - 从本地images目录"""
    # 先从本地images目录查找
    local_path = os.path.join(IMAGES_DIR, uuid + '.jpg')
    if os.path.exists(local_path):
        return send_from_directory(IMAGES_DIR, uuid + '.jpg')
    return '', 404

@app.route('/images/<path:filename>')
def serve_image(filename):
    """提供图片文件"""
    return send_from_directory(IMAGES_DIR, filename)

if __name__ == '__main__':
    print("\n启动WebUI...")
    print("访问地址: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
