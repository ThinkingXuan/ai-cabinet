from flask import jsonify

def success_response(result=None, status_code=200):
    """
    创建成功响应
    :param result: 返回结果数据
    :param status_code: HTTP状态码
    :return: JSON响应
    """
    response = {
        "success": True,
        "result": result
    }
    return jsonify(response), status_code

def error_response(message, errors=None, status_code=400):
    """
    创建错误响应
    :param message: 错误消息
    :param errors: 详细错误信息（可选）
    :param status_code: HTTP状态码
    :return: JSON响应
    """
    response = {
        "success": False,
        "message": message
    }
    
    if errors:
        response["errors"] = errors
        
    return jsonify(response), status_code 