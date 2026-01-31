# 导入FastAPI框架的核心类
from fastapi import FastAPI
# 导入CORS中间件，用于处理跨域请求
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用的实例
# title参数设置API文档的标题
app = FastAPI(title="Tomato API")

# 配置CORS（跨源资源共享）中间件
# 这是为了让前端（运行在localhost:3000）能访问这个后端API
app.add_middleware(
    CORSMiddleware,
    # 允许访问的来源列表，这里只允许前端localhost:3000
    allow_origins=["http://localhost:3000"],
    # 是否允许发送认证信息（如cookies）
    allow_credentials=True,
    # 允许的HTTP方法，*表示所有方法（GET、POST等）
    allow_methods=["*"],
    # 允许的HTTP头部，*表示所有头部
    allow_headers=["*"],
)

# 定义一个路由处理函数
# @app.get("/") 是一个装饰器，表示：
# - 当用户用GET方法访问根路径"/"时
# - 调用这个read_root函数
@app.get("/")
def read_root():
    # 返回一个JSON响应
    # FastAPI会自动将Python字典转为JSON
    return {"message": "Welcome to Tomato API!"}

# 另一个路由：健康检查端点
# 常用于监控系统是否正常运行
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",      # 服务状态
        "service": "Tomato Backend"  # 服务名称
    }


def test():
    print('hello world')
