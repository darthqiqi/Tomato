from flask import Blueprint, request, jsonify
from app import db
from app.models import Project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    """获取所有项目"""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify({
        'success': True,
        'count': len(projects),
        'projects': [project.to_dict() for project in projects]
    })

@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """获取单个项目"""
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'success': True,
        'project': project.to_dict()
    })

@projects_bp.route('/projects', methods=['POST'])
def create_project():
    """创建新项目"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({
            'success': False,
            'error': '项目名称不能为空'
        }), 400
    
    project = Project(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '项目创建成功',
        'project': project.to_dict()
    }), 201

@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '项目更新成功',
        'project': project.to_dict()
    })

@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目（会级联删除相关文件）"""
    project = Project.query.get_or_404(project_id)
    
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '项目删除成功'
    })