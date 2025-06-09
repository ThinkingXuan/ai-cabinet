#!/bin/bash

# AWS EC2最小化部署脚本
set -e

echo "开始最小化部署 AI Cabinet API 到 AWS EC2..."

# 安装依赖
echo "安装系统依赖..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# 创建Python虚拟环境
echo "创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装项目依赖
echo "安装项目依赖..."
pip install -r requirements.txt
pip install gunicorn

# 创建配置文件
echo "创建环境配置文件..."
cat > .env << EOF
FLASK_ENV=production
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')
JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')
# 如需使用MySQL，取消下面一行的注释并配置正确的连接串
# DATABASE_URL=mysql+pymysql://username:password@localhost/dbname
EOF

# 创建日志目录
echo "创建日志目录..."
mkdir -p logs

# 创建启动脚本
echo "创建启动脚本..."
cat > start.sh << EOF
#!/bin/bash
source venv/bin/activate
gunicorn -w 2 -b 0.0.0.0:8080 main:app
EOF
chmod +x start.sh

# 创建systemd服务文件（可选，使服务自动启动）
echo "创建systemd服务文件..."
sudo tee /etc/systemd/system/ai-cabinet.service > /dev/null << EOF
[Unit]
Description=AI Cabinet API Server
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/gunicorn -w 2 -b 0.0.0.0:8080 main:app
Restart=always
StandardOutput=append:$(pwd)/logs/out.log
StandardError=append:$(pwd)/logs/error.log

[Install]
WantedBy=multi-user.target
EOF

# 初始化数据库
echo "创建数据库..."
python -c "
from main import app, db
with app.app_context():
    db.create_all()
"

# 启用并启动服务
echo "启用服务..."
sudo systemctl daemon-reload
sudo systemctl enable ai-cabinet
sudo systemctl start ai-cabinet

echo "部署完成！应用已启动，可通过服务器IP:8080访问。"
echo "请确保已正确配置安全组，开放8080端口。"
echo ""
echo "管理命令："
echo "- 查看服务状态：sudo systemctl status ai-cabinet"
echo "- 重启服务：sudo systemctl restart ai-cabinet"
echo "- 停止服务：sudo systemctl stop ai-cabinet"
echo "- 查看日志：cat logs/out.log 或 cat logs/error.log" 