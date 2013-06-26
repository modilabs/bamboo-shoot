import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    User,
    Dataset,
    Dashboard,
    Chart,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        user = User(username="modilabs")
        dataset1 = Dataset(
            user=user, bamboo_host="http://bamboo.io",
            dataset_id="d59dee1092e74e2da947ac75c7b5fcfa",
            title="Students Survey 1")
        dataset2 = Dataset(
            user=user, bamboo_host="http://bamboo.io",
            dataset_id="bb9bdf69384b4400a08fcf7ecc4b0a01",
            title="Students Survey 2")
        dataset3 = Dataset(
            user=user, bamboo_host="http://192.168.56.2:8080",
            dataset_id="361bbd13d61c47718dd8e1ec36197acc",
            title="Students Survey 3")
        dashboard = Dashboard(user=user, title="Students Survey",
                              slug="students-survey")
        chart1 = Chart(dashboard=dashboard, dataset=dataset3,
                       title="Gender by Grade", x_field_id='sex',
                       y_field_id='grade')
        chart2 = Chart(dashboard=dashboard, dataset=dataset3,
                       title="Income by Gender", x_field_id='income',
                       y_field_id='sex')
        DBSession.add(user)
