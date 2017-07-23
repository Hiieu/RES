import os
from httplib import (
    NO_CONTENT,
    NOT_FOUND,
    OK
)
from tempfile import mkstemp
from unittest import (
    main as ut_main,
    TestCase
)

from flask import json

from RES import (
    app,
    db,
    Report,
    ReportView
)

DATA_1 = {
    "organization": "Dunder Mifflin",
    "reported_at": "2015-04-21",
    "created_at": "2015-04-22",
    "inventory": [
        {"name": "paper", "price": "2.00"},
        {"name": "stapler", "price": "5.00"},
        {"name": "printer", "price": "125.00"},
        {"name": "ink", "price": "3000.00"}
    ]
}


class FlaskrTestCase(TestCase):
    def init_db(self):
        """Initializes the database."""
        db.init_app(app)
        db.create_all()
        self._populate_db()

    @staticmethod
    def _populate_db():
        """Add mocked data to database"""
        data_1 = json.dumps(DATA_1)
        data_2 = json.dumps({
            "organization": "Skynet Papercorp", "reported_at": "2015-04-22",
            "created_at": "2015-04-23",
            "inventory": [{"name": "paper", "price": "4.00"}]
        })
        report_1 = Report(data=data_1)
        report_2 = Report(data=data_2)
        db.session.add(report_1)
        db.session.add(report_2)
        db.session.commit()

    def setUp(self):
        """Create temporary database"""
        self.db_fd, app.config['DATABASE'] = mkstemp()
        app.config.update(
            DEBUG=False,
            SQLALCHEMY_DATABASE_URI=
            'sqlite:///{0}'.format(app.config['DATABASE']),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True,
        )
        self.app = app.test_client()
        with app.app_context():
            self.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_report_pdf_1(self):
        response = self.app.get('/report/pdf/1')
        self.assertEqual(response.status_code, OK)
        self.assertEqual(response.headers[1], ('Content-Length', '2090'))
        self.assertEqual(response.headers[2],
                         ('Content-Disposition',
                          'inline; filename=Report_1.pdf'))

    def test_report_pdf_2(self):
        response = self.app.get('/report/pdf/2')
        self.assertEqual(response.headers[1], ('Content-Length', '2004'))
        self.assertEqual(response.headers[2],
                         ('Content-Disposition',
                          'inline; filename=Report_2.pdf'))

    def test_report_xml_1(self):
        response = self.app.get('/report/xml/1')
        self.assertEqual(response.headers[1], ('Content-Length', '578'))
        self.assertEqual(response.headers[2],
                         ('Content-Disposition',
                          'inline; filename=Report_1.xml'))

    def test_invalid_report_id(self):
        response = self.app.get('/report/pdf/100')
        self.assertEqual(response.status_code, NO_CONTENT)

    def test_invalid_url(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, NOT_FOUND)

    def test_get_report_context_method(self):
        """Check method output for rendered context"""
        report_1 = Report(data=json.dumps(DATA_1))
        context = ReportView._get_report_context(report_1)
        self.assertDictEqual(context,
                             {
                                 'organization': DATA_1['organization'],
                                 'inventory': DATA_1['inventory'],
                                 'reported_at': DATA_1['reported_at'],
                                 'created_at': DATA_1['created_at'],
                             })


if __name__ == '__main__':
    ut_main()
