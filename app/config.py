import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """基础配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # 数据库
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 
        f"sqlite:///{os.path.join(basedir, 'instance', 'tomato.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(basedir, 'uploads'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB
    
    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {
        'excel': {'xlsx', 'xls', 'csv'},
        'image': {'jpg', 'jpeg', 'png', 'gif', 'bmp'},
        'pdf': {'pdf'},
        'document': {'doc', 'docx', 'txt'},
        'ppt': {'ppt', 'pptx'}
    }

class DevelopmentConfig(Config):
    """开发配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产配置"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}