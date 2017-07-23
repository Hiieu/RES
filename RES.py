from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=
    'postgresql://interview:LetMeIn@candidate.suade.org/suade',
    SQLALCHEMY_ECHO=False,
    SECRET_KEY='A3ZZpa&Z&*kP88KhWYrf3',
    DEBUG=True,
)
db = SQLAlchemy(app)


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column(db.Text)


if __name__ == '__main__':
    app.run()
