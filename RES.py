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
                return self.get_response_for_file(file_type, report)
        return '', NO_CONTENT

    def get_response_for_file(self, file_type, report):
        """Return full response depend on file type"""
        if file_type == 'pdf':
            generated_report = self._get_report_pdf(report)
        response = app.make_response(generated_report.getvalue())
        return response

    def _get_report_pdf(self, report):
        """Return generated report in pdf from rendered html template"""
        pdf = StringIO()
        pisa.CreatePDF(StringIO(self._get_render_template(report)), pdf)
        return pdf

    def _get_render_template(self, report):
        return render_template('report.html',
                               **self._get_report_context(report))

    @staticmethod
    def _get_report_context(report):
        """Return context for rendering template"""
        data = json.loads(report.data)
        return {
            'organization': data['organization'],
            'inventory': data['inventory'],
            'reported_at': data['reported_at'],
            'created_at': data['created_at'],
        }


app.add_url_rule('/report/<file_type>/<int:report_id>',
                 view_func=ReportView.as_view('report_view'))


if __name__ == '__main__':
    app.run()
