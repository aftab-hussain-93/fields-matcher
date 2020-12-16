import uuid, os, pandas, datetime, io
from flask import current_app
"""Module - file_manipulation.py
    Contains, classes and methods used for manipulating, and analyzing the uploaded files.
"""

class File:
    def __init__(self, user_id, file_path):
        self.user_id = user_id
        self.file_path = file_path

    @staticmethod
    def sanitize_filename_extension(filename):
        """Method used to sanitize the filename, get a new unique name, and extension details.

        """
        public_id = uuid.uuid4().hex
        extension = filename.rsplit('.')[-1].lower()
        sanitized_extension  = File.sanitize_extension(extension)
        if sanitized_extension:
            original_filename = os.path.splitext(filename)[0]
            unique_name = f"{public_id}.{sanitized_extension}"
            return (original_filename, sanitized_extension, unique_name)
        else:
            raise Exception("Incorrent extension")

    @staticmethod
    def sanitize_extension(extension):
        if extension.lower() in ['csv', 'comma']:
            extension = 'csv'
        elif extension.lower() in ['excel', 'xls', 'xlsx']:
            extension = 'xlsx'
        elif extension.lower() in ['json']:
            extension = 'json'
        else:
            extension = None
        return extension
    
    @staticmethod
    def get_ext_from_path(file_path):
        return os.path.splitext(file_path)[1]

    def generate_new_file_doc(self, file_object):
        """ Method to generate a file document and returning the file object back for upload onto AWS.

        Args:
            file_object ([type]): The uploaded file.
            user_id ([string]) : User's public ID if the file was uploaded by logged in user, else None
            file_path : The file path chosen based on the USER_ID
        Return:
            file_document ([dict]): File Document containg file details.
            file_object : Object to be stored onto AWS S3
        """
        # Generating Unique name for file for storage in the directory
        original_filename, extension, unique_name = self.sanitize_filename_extension(file_object.filename)

        if extension == 'csv':
            df = pandas.read_csv(file_object)
        elif extension == 'xlsx':
            df = pandas.read_excel(file_object)
        elif extension == 'json':
            df = pandas.read_json(file_object)
        else:
            raise Exception('Invalid File Type')

        headers = df.columns.to_list()
        file_object.seek(0)

        # Adding the File to DB
        file_document = {
            'original_filename': original_filename,
            'unique_name': unique_name,
            'file_path': self.file_path + f'{unique_name}',
            'user_id': self.user_id,
            'headers' : headers,
            'versions': [],
            'email_list': [],
            'phone_num_list': [],
            'date_created': datetime.datetime.utcnow(),
            'date_modified': datetime.datetime.utcnow(),
            'date_accessed': datetime.datetime.utcnow()
            }

        return {
            'file_object': file_object,
            'file_document': file_document
        }

    def generate_update_file_df(self, data_frame, current_file, new_extension):
        """
        Parameters:
        In - 
            data_frame = Consists of the modified data frame
            current_file = The file presently being modified
        Out - 
            file_document = File document that can be inserted into Mongo DB
            file_object = File buffer, either Bytes or String that is uploaded onto AWS S3 Bucket
        """
        public_id = uuid.uuid4().hex
        unique_name = f"{public_id}.{new_extension}"
        updated_file_path = self.file_path + f'{unique_name}'

        # Add parent file attribute to newly created file
        # If parent file attribute already exists then replicate the same one
        parent_file_oid = current_file.get('parent_file_oid') or current_file.get('_id')
        original_filename = current_file.get('original_filename')

        #### Modiying the File Headers
        updated_file = None
        if new_extension in ('csv'):
            updated_file = io.StringIO()
            data_frame.to_csv(updated_file, index = False, header=True)
        elif new_extension in ('xlsx'):
            updated_file = io.BytesIO()
            data_frame.to_excel(updated_file, index = False, header=True)
        elif new_extension in ('json'):
            updated_file = io.StringIO()
            data_frame.to_json(updated_file)
        updated_file.seek(0)
        current_app.logger.debug("New dataframe buffer is created")
        # current_app.logger.debug(updated_file)

        new_file_document = {
        'parent_file_oid' : parent_file_oid,
        'original_filename': original_filename,
        'unique_name': unique_name,
        'file_path': updated_file_path,
        'user_id': current_file.get('user_id'),
        'headers' : data_frame.columns.to_list(),
        'email_list': current_file.get('email_list'),
        'phone_num_list': current_file.get('phone_num_list'),
        'date_created': datetime.datetime.utcnow(),
        'date_modified': datetime.datetime.utcnow(),
        'date_accessed': datetime.datetime.utcnow()
        }

        return {
        'file_object': updated_file,
        'file_document': new_file_document
        }
