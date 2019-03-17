from app import app as application

if __name__ == '__main__':
    application.run(debug=True, host='127.0.0.1', port=8000)