from uuid import uuid4

from flask import request
from flask import jsonify
from flask import Flask
from flask_restplus import Api, Resource, Namespace, fields

import settings
import os
import sys
from lib.sdn_speedtest import Tester
from lib.sdn_pinger import Pinger

if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this app\n")


app = Flask(__name__)
api = Api(app, version='1.0', title='Inspector API', description='A SDN TESTING API')


ns = Namespace('inspector', description='manage inspector servers')

api.add_namespace(ns)


inspectorParser = api.parser()
inspectorParser.add_argument('mgm_ipv4', type=str)


inspectorModel = {
    'device_id': fields.String(description='device_id to connect'),
    'stage': fields.String(description='stage to connect'),
    'speedtest_type': fields.String(description='speedtest_type'),
}
inspectorModel = ns.model('inspectorModel', inspectorModel)


@api.route('/inspect', endpoint='Inspector')
class Inspector(Resource):

    @ns.expect(inspectorModel)
    def post(self):
        args = request.json
        tester = Tester(
            device_id=args.get('device_id', f"INSPECTOR-{uuid4()}"),
            stage=args.get('stage', 'app'),
            speedtest_type=args.get('speedtest_type', 'AZURE')
        )
        result = tester.get_ping_statistics()
        return result


@api.route('/latency', endpoint='Latency')
class AutoPinger(Resource):

    @ns.expect(inspectorModel)
    def post(self):
        args = request.json
        tester = Pinger(
            device_id=args.get('device_id', f"INSPECTOR-{uuid4()}"),
            stage=args.get('stage', 'app'),
            # speedtest_type=args.get('provider', 'AZURE'),
        )
        result = tester.get_ping_statistics()
        return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', processes=1)


def run_api():
    app.run(host='0.0.0.0', processes=1)
