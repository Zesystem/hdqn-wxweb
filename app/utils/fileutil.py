import os
from datetime import datetime

HOSTNAME = 'localhost'
FILE_PATH = "/Users/torn/Desktop/hdqn-wxweb"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp3', 'mp4', 'amr', 'JPG', 'PNG', 'JPEG', 'MP3', 'MP4', 'AMR'])
 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def create_file(file):
    if not allowed_file(file.filename):
        return {'code' : 404}
    sub_path = ""
    file_type = file.filename.rsplit('.', 1)[1]
    if file_type in ("png", "jpg", "jpeg"):
        sub_path = "images"
    elif file_type == "mp3":
        sub_path = "musics"
    elif file_type == "mp4":
        sub_path = "videos"
    elif file_type == "amr":
        sub_path = "voices"
    fixpath = "upload/{}/{}.{}".format(sub_path, datetime.now().strftime("%Y%m%d%H%M%S"), file_type)
    filepath = "{}/app/static/{}".format(FILE_PATH, fixpath)
    print(filepath) 
    try:
        file.save(filepath)
        return {'code' : 200, 'filename': '{}/static/{}'.format(HOSTNAME, fixpath)}
    except:
        if os.path.exists(filepath):
            os.remove(filepath)
        return {'code' : 404}