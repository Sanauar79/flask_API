class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///api.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sanauarh@gmail.com'
    MAIL_PASSWORD = 'kftpwzpgeymcwutj'
    MAIL_DEFAULT_SENDER = 'sanauarh@gmail.com'
