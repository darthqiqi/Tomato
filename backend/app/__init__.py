from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)  # 允许跨域，方便前端调用
    
    # 注册蓝图
    from app.routes.projects import projects_bp
    from app.routes.files import files_bp
    
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(files_bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        print("✅ 数据库表已创建")
    
    return app