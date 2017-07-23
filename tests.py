import os
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
            TESTING=True,
        )
        self.app = app.test_client()
        with app.app_context():
            self.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


if __name__ == '__main__':
    ut_main()
