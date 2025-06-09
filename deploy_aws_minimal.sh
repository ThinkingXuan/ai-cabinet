#!/bin/bash

# AWS EC2最小化部署脚本（不使用虚拟环境）
set -e

echo "开始最小化部署 AI Cabinet API 到 AWS EC2..."

# 检测Linux发行版
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
else
    OS=$(uname -s)
fi

echo "检测到操作系统: $OS"

# 安装系统依赖
echo "安装系统依赖..."
if command -v apt-get &> /dev/null; then
    # Debian, Ubuntu
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
elif command -v yum &> /dev/null; then
    # Amazon Linux, CentOS, RHEL
    sudo yum update -y
    sudo yum install -y python3 python3-pip
elif command -v dnf &> /dev/null; then
    # Fedora, newer RHEL/CentOS
    sudo dnf update -y
    sudo dnf install -y python3 python3-pip
else
    echo "无法识别的包管理器，请手动安装Python3和pip。"
    exit 1
fi

# 安装项目依赖
echo "安装项目依赖..."
pip3 install --user -r requirements.txt
pip3 install --user gunicorn

# 创建配置文件
echo "创建环境配置文件..."
cat > .env << EOF
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
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
cd "\$(dirname "\$0")"
nohup python3 -m gunicorn -w 2 -b 0.0.0.0:8080 main:app > logs/out.log 2> logs/error.log &
echo \$! > app.pid
echo "应用已在后台启动，PID: \$(cat app.pid)"
EOF

# 创建停止脚本
cat > stop.sh << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
if [ -f app.pid ]; then
  pid=\$(cat app.pid)
  echo "停止应用 (PID: \$pid)..."
  kill \$pid
  rm app.pid
  echo "应用已停止"
else
  echo "找不到PID文件，应用可能未运行"
fi
EOF

# 创建重启脚本
cat > restart.sh << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
if [ -f app.pid ]; then
  ./stop.sh
fi
./start.sh
EOF

# 设置脚本权限
chmod +x start.sh stop.sh restart.sh

# 初始化数据库
echo "创建数据库..."
python3 -c "
from main import app, db
with app.app_context():
    db.create_all()
"

# 检查是否支持systemd
if command -v systemctl &> /dev/null; then
    echo "检测到systemd，创建服务文件..."
    cat > ai-cabinet.service << EOF
[Unit]
Description=AI Cabinet API Server
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 -m gunicorn -w 2 -b 0.0.0.0:8080 main:app
Restart=always
StandardOutput=append:$(pwd)/logs/out.log
StandardError=append:$(pwd)/logs/error.log

[Install]
WantedBy=multi-user.target
EOF

    echo "如需使用systemd管理服务，请执行以下命令："
    echo "sudo cp ai-cabinet.service /etc/systemd/system/"
    echo "sudo systemctl daemon-reload"
    echo "sudo systemctl enable ai-cabinet"
    echo "sudo systemctl start ai-cabinet"
    echo ""
fi

echo "部署完成！运行以下命令启动应用："
echo "./start.sh"
echo ""
echo "管理命令："
echo "- 启动应用：./start.sh"
echo "- 停止应用：./stop.sh"
echo "- 重启应用：./restart.sh"
echo "- 查看日志：cat logs/out.log 或 cat logs/error.log"
echo ""
echo "注意：请确保已正确配置安全组，开放8080端口。" 