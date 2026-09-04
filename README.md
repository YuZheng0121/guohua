# 明清仕女图分析系统

基于 Flask + YOLO + Grounding DINO + VLM 的中国画人物检测与分类系统。

## 快速开始

### 1. 环境要求
- Python 3.8+
- pip

### 2. 安装依赖
```bash
pip install flask
```

### 3. 下载代码
```bash
git clone git@github.com:YuZheng0121/guohua.git
cd guohua
```

### 4. 启动服务
```bash
python3 app.py
```

### 5. 访问网站
- 本地访问：http://localhost:5001
- 局域网访问：http://你的IP:5001

## 功能

- **统计概览**：展示分类统计、性别分布、检测标签频率等图表
- **图片查看**：支持按分类浏览图片，查看检测结果和姿态关键点
- **明清仕女图典藏**：展示18张精选明清仕女图
- **公开版权筛选**：按分类筛选公开版权图片

## 项目结构

```
guohua_webui/
├── app.py                          # Flask主程序
├── templates/                      # HTML模板
│   ├── index.html                  # 首页（统计概览）
│   ├── images.html                 # 图片查看页面
│   └── shinu.html                  # 明清仕女图典藏页面
├── static/                         # 静态文件
├── data/                           # 数据文件
│   ├── merged_results.json         # 检测结果数据
│   ├── pose_results_all.json       # 姿态关键点数据
│   ├── public_copyright_by_category.json  # 公开版权数据（按分类）
│   ├── mingqing_ids.json           # 明清仕女图ID列表
│   └── shinu_52_website.json       # 明清仕女图展示数据
└── images/                         # 缩略图文件夹
```

## 快速开始

### 环境要求

- Python 3.8+
- Flask

### 安装依赖

```bash
pip3 install flask
```

### 启动服务

```bash
# 进入项目目录
cd guohua_webui

# 启动Flask服务
python3 app.py
```

启动后访问：http://localhost:5001

### 后台运行

```bash
# 使用nohup后台运行
nohup python3 app.py > app.log 2>&1 &

# 查看日志
tail -f app.log

# 停止服务
pkill -f "python3 app.py"
```

## 部署到服务器

### 1. 上传代码

```bash
# 在本地压缩
tar -czf guohua_webui_deploy.tar.gz guohua_webui/

# 上传到服务器
scp guohua_webui_deploy.tar.gz username@server:/path/to/

# 在服务器上解压
ssh username@server
cd /path/to
tar -xzf guohua_webui_deploy.tar.gz
```

### 2. 安装依赖并启动

```bash
cd guohua_webui
pip3 install flask
nohup python3 app.py > app.log 2>&1 &
```

### 3. 配置防火墙（如需要）

```bash
# 开放5001端口
sudo ufw allow 5001
```

## 数据说明

### 图片分类

- **男**：男性人物画
- **女**：女性人物画
- **有男有女**：包含男女的画作
- **点景人物**：风景画中的人物

### 公开版权

- **男**：2406张
- **女**：822张
- **有男有女**：682张
- **点景人物**：1629张
- **合计**：5539张

## 技术栈

- **后端**：Python Flask
- **前端**：HTML/CSS/JavaScript
- **图表**：Chart.js
- **检测模型**：YOLO + DINO + VLM

## 相关链接

- 数据库：MySQL (backend.aailab.cn:12008)
- 模型服务：YOLOv8x-WorldV2
- 检测框架：Grounding DINO

## 许可证

内部项目，仅供研究使用。
