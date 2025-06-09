import os
from dotenv import load_dotenv
from app import create_app, db

# 加载环境变量
load_dotenv()

# 创建应用实例
app = create_app(os.getenv('FLASK_ENV', 'development'))

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)