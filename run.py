import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # 确保上传目录存在
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"📁 创建上传目录: {upload_folder}")
    
    print("=" * 50)
    print("🚀 Tomato 项目管理系统后端已启动!")
    print("=" * 50)
    print("\n📚 可用API端点:")
    print("  GET    /api/projects                 # 获取所有项目")
    print("  POST   /api/projects                 # 创建新项目")
    print("  GET    /api/projects/<id>           # 获取项目详情")
    print("  PUT    /api/projects/<id>           # 更新项目")
    print("  DELETE /api/projects/<id>           # 删除项目")
    print("\n  GET    /api/projects/<id>/files    # 获取项目文件")
    print("  POST   /api/projects/<id>/files     # 上传文件")
    print("  GET    /api/files/<id>              # 获取文件信息")
    print("  GET    /api/files/<id>/download     # 下载文件")
    print("  DELETE /api/files/<id>              # 删除文件")
    print("\n🌐 访问地址: http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)