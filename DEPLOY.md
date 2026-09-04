# 部署指南

## 从GitHub克隆并部署

### 步骤1：克隆仓库

```bash
git clone https://github.com/your-username/guohua_webui.git
cd guohua_webui
```

### 步骤2：下载数据文件

由于数据文件太大（约1GB），需要单独下载：

```bash
# 创建数据目录
mkdir -p data images

# 下载数据文件（从你的服务器或备份）
# 文件列表：
# - merged_results.json (77MB)
# - pose_results_all.json (366MB)
# - public_copyright_by_category.json (243KB)
# - mingqing_ids.json (1.4KB)
# - shinu_52_website.json (54KB)
# - images/ (803MB)

# 示例：从服务器下载
scp username@server:/path/to/data/*.json ./data/
scp -r username@server:/path/to/images/ ./images/
```

### 步骤3：安装依赖

```bash
pip3 install flask
```

### 步骤4：启动服务

```bash
python3 app.py
```

访问：http://localhost:5001

---

## 完整部署（包含数据）

### 步骤1：下载完整压缩包

```bash
# 从GitHub releases或服务器下载完整压缩包
wget https://github.com/your-username/guohua_webui/releases/download/v1.0/guohua_webui_full.tar.gz

# 解压
tar -xzf guohua_webui_full.tar.gz
cd guohua_webui
```

### 步骤2：安装依赖并启动

```bash
pip3 install flask
nohup python3 app.py > app.log 2>&1 &
```

---

## 服务器部署（生产环境）

### 使用systemd管理服务

```bash
# 创建服务文件
sudo nano /etc/systemd/system/guohua-webui.service
```

添加以下内容：

```ini
[Unit]
Description=Chinese Painting Analysis WebUI
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/guohua_webui
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable guohua-webui
sudo systemctl start guohua-webui

# 查看状态
sudo systemctl status guohua-webui

# 查看日志
sudo journalctl -u guohua-webui -f
```

### 使用nginx反向代理（可选）

```bash
# 安装nginx
sudo apt install nginx

# 配置nginx
sudo nano /etc/nginx/sites-available/guohua-webui
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/guohua-webui /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 常见问题

### Q: 启动后无法访问？

1. 检查防火墙是否开放5001端口：
   ```bash
   sudo ufw allow 5001
   ```

2. 检查服务是否正常运行：
   ```bash
   ps aux | grep python3
   ```

3. 检查日志：
   ```bash
   tail -f app.log
   ```

### Q: 数据文件在哪里？

数据文件太大，不包含在Git仓库中。需要从以下位置获取：
- 服务器：`/root/guohua_webui/data/`
- 备份：`guohua_webui_deploy.tar.gz`

### Q: 如何更新数据？

```bash
# 停止服务
pkill -f "python3 app.py"

# 替换数据文件
cp /path/to/new/data/*.json ./data/

# 重启服务
python3 app.py
```

### Q: 如何查看实时日志？

```bash
tail -f app.log
```

### Q: 如何停止服务？

```bash
pkill -f "python3 app.py"
# 或者如果使用systemd
sudo systemctl stop guohua-webui
```

---

## 端口说明

- **5001**：WebUI默认端口
- **80**：nginx反向代理端口（可选）
- **443**：HTTPS端口（可选，需要SSL证书）

## 联系方式

如有问题，请联系项目维护者。
