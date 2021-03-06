# import pandas, datetime, os
# from werkzeug.utils import secure_filename
# from flask import current_app
# # from app.blueprints.api.models import File, UpdatedFile


# ALLOWED_EXTENSIONS = {'csv','xls','xlsx'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS

# def get_file_headers(current_file):
#     file_name = current_file.filename
#     file_path = os.path.join(os.path.normpath(current_app.root_path), current_file.directory, current_file.filename)
#     ext = file_name.rsplit('.')[-1].lower()
#     if ext == 'csv':
#         df = pandas.read_csv(file_path)
#     elif ext in ['xls','xlsx']:
#         df = pandas.read_excel(file_path)
#     headers = df.columns.to_list()
#     return headers, ext

# def get_file_details(file_obj):
#     # print(pandas.read_csv(file_obj))
#     filename = file_obj.filename
#     ext = filename.rsplit('.')[-1].lower()
#     if ext == 'csv':
#         df = pandas.read_csv(file_obj)
#     elif ext in ['xls','xlsx']:
#         df = pandas.read_excel(file_obj)
#     headers = df.columns.to_list()
#     return headers, ext

# # def modify_headers(extension, position_dict, name_dict):
# #     file_path = session['file_path']
# #     filename = session['file_name']



# def modify_headers(current_file, extension, position_dict, name_dict):
#     filename = current_file.filename
#     new_header_ls = [x[0] for x in sorted(position_dict.items(), key=lambda x:x[1])]
#     with current_app.app_context():
#         DOWNLOAD_FOLDER = os.path.join(os.path.normpath(current_app.root_path),current_app.config['DOWNLOAD_FOLDER'])
#         app_download_dir = current_app.config['DOWNLOAD_FOLDER']
#     name, ext = os.path.splitext(filename)
#     ext = ext.split('.')[-1].lower()
#     file_path = os.path.join(os.path.normpath(current_app.root_path),current_file.directory,filename)
#     if ext == 'csv':
#         df = pandas.read_csv(file_path)
#     elif ext in ['xls','xlsx']:
#         df = pandas.read_excel(file_path)
#     df = df[new_header_ls]
#     df.rename(columns=name_dict,inplace=True)
#     extension = extension.lower()
#     now = datetime.datetime.now().strftime('%y%m%d%H%M%S%f')[:-3]
#     new_name = f'{name}{now}'
#     if extension in ('csv','comma'):
#         new_name = new_name + ".csv"
#         df.to_csv(os.path.join(os.path.normpath(DOWNLOAD_FOLDER),new_name), index = False, header=True)
#     elif extension in ('excel','xls','xlsx'):
#         new_name = new_name + ".xlsx"
#         df.to_excel(os.path.join(os.path.normpath(DOWNLOAD_FOLDER),new_name), index = False, header=True)
#     updated_file = current_file.generate_update_file(filename=new_name, directory=app_download_dir)
#     return updated_file

# def get_user_files(user):
#     uploaded_files = File.query.filter_by(user=user).all()
#     all_file_list = []
#     for uploads in uploaded_files:
#         uploaded_file_dict = {}
#         uploaded_file_dict['filename'] = uploads.filename
#         uploaded_file_dict['file_id'] = uploads.public_id
#         uploaded_file_dict['date_created'] = uploads.date_created
#         updated_files = UpdatedFile.query.filter_by(file=uploads).order_by(UpdatedFile.date_created).all()
#         updated_file_list = []
#         for version, file in enumerate(updated_files, start=1):
#             file_dict = {}
#             file_dict['version'] = version
#             file_dict['filename'] = file.filename
#             file_dict['file_id'] = file.public_id
#             file_dict['date_created'] = file.date_created
#             updated_file_list.append(file_dict)

#         uploaded_file_dict['updated_versions'] = updated_file_list
#         all_file_list.append(uploaded_file_dict)

#     return all_file_list