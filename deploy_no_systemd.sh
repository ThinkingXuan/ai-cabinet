#!/bin/bash

# AWS EC2极简部署脚本（不使用systemd）
set -e

echo "开始极简部署 AI Cabinet API 到 AWS EC2..."

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
cd "\$(dirname "\$0")"
source venv/bin/activate
nohup gunicorn -w 2 -b 0.0.0.0:8080 main:app > logs/out.log 2> logs/error.log &
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
python -c "
from main import app, db
with app.app_context():
    db.create_all()
"

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
echo "      为了保持应用持久运行，建议使用screen或tmux等工具。" 