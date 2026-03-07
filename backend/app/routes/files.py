import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Project, ProjectFile

files_bp = Blueprint('files', __name__)

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_category(filename):
    """根据扩展名获取文件分类"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    config = current_app.config['ALLOWED_EXTENSIONS']
    
    for category, extensions in config.items():
        if ext in extensions:
            return category
    return 'other'

@files_bp.route('/projects/<int:project_id>/files', methods=['GET'])
def get_project_files(project_id):
    """获取项目的所有文件"""
    project = Project.query.get_or_404(project_id)
    
    files = ProjectFile.query.filter_by(project_id=project_id)\
        .order_by(ProjectFile.uploaded_at.desc()).all()
    
    return jsonify({
        'success': True,
        'count': len(files),
        'files': [file.to_dict() for file in files]
    })

@files_bp.route('/projects/<int:project_id>/files', methods=['POST'])
def upload_file(project_id):
    """上传文件到项目"""
    # 检查项目是否存在
    project = Project.query.get_or_404(project_id)
    
    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': '没有选择文件'
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': '没有选择文件'
        }), 400
    
    # 安全检查
    original_filename = secure_filename(file.filename)
    
    # 获取文件分类
    file_category = get_file_category(original_filename)
    
    # 检查是否允许该类型
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS'].get(file_category, set())
    if file_category == 'other' or not allowed_file(original_filename, allowed_extensions):
        return jsonify({
            'success': False,
            'error': f'不支持的文件类型。允许的类型: {list(current_app.config["ALLOWED_EXTENSIONS"].keys())}'
        }), 400
    
    # 生成唯一文件名
    file_ext = original_filename.rsplit('.', 1)[1].lower()
    stored_filename = f"{uuid.uuid4().hex}.{file_ext}"
    
    # 创建项目目录
    project_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(project_id))
    os.makedirs(project_dir, exist_ok=True)
    
    # 保存文件
    filepath = os.path.join(project_dir, stored_filename)
    file.save(filepath)
    
    # 获取文件信息
    file_size = os.path.getsize(filepath)
    
    # 保存到数据库
    project_file = ProjectFile(
        original_name=original_filename,
        stored_name=stored_filename,
        file_type=file_category,
        file_size=file_size,
        mime_type=file.mimetype,
        description=request.form.get('description', ''),
        project_id=project_id
    )
    
    db.session.add(project_file)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '文件上传成功',
        'file': project_file.to_dict()
    }), 201

@files_bp.route('/files/<int:file_id>', methods=['GET'])
def get_file_info(file_id):
    """获取文件信息"""
    file = ProjectFile.query.get_or_404(file_id)
    return jsonify({
        'success': True,
        'file': file.to_dict()
    })

@files_bp.route('/files/<int:file_id>/download', methods=['GET'])
def download_file(file_id):
    """下载文件"""
    file = ProjectFile.query.get_or_404(file_id)
    
    project_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(file.project_id))
    
    return send_from_directory(
        directory=project_dir,
        path=file.stored_name,
        as_attachment=True,
        download_name=file.original_name
    )

@files_bp.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """删除文件"""
    file = ProjectFile.query.get_or_404(file_id)
    
    # 删除物理文件
    project_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(file.project_id))
    filepath = os.path.join(project_dir, file.stored_name)
    
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # 删除数据库记录
    db.session.delete(file)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '文件删除成功'
    })