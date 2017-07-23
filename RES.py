from StringIO import StringIO
from httplib import NO_CONTENT

from flask import (
    Flask,
    render_template,
    json
)
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from xhtml2pdf import pisa

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


class ReportView(MethodView):

    FILE_HEADER = {
        'pdf': {
            'content_type': 'application/pdf'
        },
        'xml': {
            'content_type': 'application/xml'
        }
    }

    def get(self, file_type, report_id):
        if file_type in self.FILE_HEADER and report_id:
            report = Report.query.filter_by(id=report_id).first()
            if report:
                pass

app.add_url_rule('/report/<file_type>/<int:report_id>',
                 view_func=ReportView.as_view('report_view'))


if __name__ == '__main__':
    app.run()
