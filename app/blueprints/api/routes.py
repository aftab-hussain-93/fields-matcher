from flask import redirect, request, jsonify
from app.utils import save_file, get_file_headers, modify_headers,  allowed_file

from flask import Blueprint

api = Blueprint('api',__name__)

@api.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        resp = jsonify({
            'message' : 'No file part in request'
        })
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({
            'message':'No file selected for upload'
        })
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = save_file(file)
        headers, extension = get_file_headers(filename)
        headers_w_position = {}
        for i,head in enumerate(headers,start=1):
            headers_w_position[head] = {
                'header_name' : head,
                'position' : i
            }
        resp = jsonify({
            'filename': filename,
            'extension' : extension,
            'headers' : headers_w_position
        })
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({
            'message' : 'File type not allowed'
        })
        resp.status_code = 400
        return resp

@api.route('/api/modify',methods=['POST'])
def api_modify():
    data = request.get_json()
    #print(data)
    filename = data['filename']
    extension = data['extension']
    headers = data['headers']
    position_dict = {}
    header_name_dict = {}
    for head, details in headers.items():
        header_name_dict[head] = details['header_name']
        position_dict[head] = details['position']
    if len(position_dict.values()) != len(set(position_dict.values())):
        resp = jsonify({
            'message' : 'The position values provided are overlapping.'
        })
        resp.status_code = 400
        return resp
    else:
        new_name = modify_headers(filename, extension, position_dict, header_name_dict)
        resp = jsonify({
            'modifiedFile' : new_name
        })
        resp.status_code = 201
        return resp
        # return redirect(url_for('api_download', filename = new_name))

