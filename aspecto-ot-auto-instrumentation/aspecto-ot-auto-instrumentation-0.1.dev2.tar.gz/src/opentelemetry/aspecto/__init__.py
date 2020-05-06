from opentelemetry import trace
from opentelemetry.ext.jaeger import JaegerSpanExporter
from opentelemetry.ext.zipkin import ZipkinSpanExporter
from opentelemetry.ext.otcollector.trace_exporter import CollectorSpanExporter as OTSpanExporter
from opentelemetry.sdk.trace import TracerProvider, Resource
from opentelemetry.sdk.trace.export import Span, SpanExporter

import requests
import json
import uuid
import os
import socket
import sys
import subprocess
import typing

from opentelemetry.aspecto.utils import fetch_git_hash, read_aspecto_json
from opentelemetry.aspecto.config_service import get_config
from opentelemetry.aspecto.batch_processor import BatchExportSpanProcessor

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
_INSTALLED_PACKAGES = [r.decode().split('==')[0] for r in reqs.split()]

def outgoing_http_custom_attributes(span: Span, result: requests.Response):
    request_body = result.request.body
    if request_body is not None and type(request_body) is str:
        span.set_attribute("http.request.body", request_body)

    if result.content is not None:
        span.set_attribute("http.response.body", result.content.decode('utf-8'))

    span.set_attribute("http.request.headers", json.dumps(dict(result.request.headers)))
    span.set_attribute("http.response.headers", json.dumps(dict(result.headers)))
    span.set_attribute("aspecto.plugin.name", "requests")


class AspectoInstrumentor:
    class DevJaegerPayload(typing.TypedDict):
        host: str
        port: int

    def __init__(
        self,
        service_name: str,
        aspecto_auth: str = None,
        dev_jaeger: DevJaegerPayload = None,
        env: str = "empty",
    ):
        if aspecto_auth is None:
            token_from_json = read_aspecto_json()
            if token_from_json is not None:
                aspecto_auth = token_from_json
            else:
                try:
                    aspecto_auth = os.environ["ASPECTO_AUTH"]
                except Exception:
                    raise ValueError("Must provide aspecto token via constructor or through ASPECTO_AUTH env var")

        self.dev_jaeger = dev_jaeger
        self.service_name = service_name
        self.aspecto_auth = aspecto_auth
        self.git_hash = fetch_git_hash()
        self.env = env
        self.process_id = str(uuid.uuid4())
        self.resources = {
            "aspecto.instance.id": self.process_id,
            "aspecto.hostname": socket.gethostname(),
            "aspecto.token": self.aspecto_auth,
            "aspecto.githash": self.git_hash,
            "aspecto.package.name": self.service_name,
            "telemetry.sdk.language": "python",
            "telemetry.sdk.version": sys.version,
            "env": self.env
        }
        self.span_processor = BatchExportSpanProcessor(tags=self.resources)

    def instrument(self):
        if 'Flask' in _INSTALLED_PACKAGES:
            print('Aspecto Instrumenting Flask')
            from opentelemetry.aspecto.ext.flask import FlaskInstrumentor
            FlaskInstrumentor().instrument()

        trace_provider = TracerProvider(resource=Resource(labels=self.resources))

        if 'requests' in _INSTALLED_PACKAGES:
            print('Aspecto Instrumenting requests')
            from opentelemetry.aspecto.ext.requests import enable
            enable(trace_provider, outgoing_http_custom_attributes)

        trace.set_tracer_provider(trace_provider)
        trace.get_tracer_provider().add_span_processor(self.span_processor)

        get_config(self.aspecto_auth, self.on_config)

    def on_config(self, config):
        print("Aspecto Initializing Privacy Engine")
        self.span_processor.init_privacy_engine(config["privacyRules"])

        # Jaeger dev
        if self.dev_jaeger is not None:
            dev_jaeger_exporter: SpanExporter = JaegerSpanExporter(
                service_name=self.service_name,
                agent_host_name=self.dev_jaeger["host"],
                agent_port=self.dev_jaeger["port"],
            )
            self.span_processor.add_exporter(dev_jaeger_exporter)

        # Zipkin
        zipkin_exporter: SpanExporter = ZipkinSpanExporter(
            service_name=self.service_name,
            host_name="jaeger-collector.aspecto.io",
            port=443,
            endpoint="/api/v2/spans",
            protocol="https"
        )
        self.span_processor.add_exporter(zipkin_exporter)

        # OTEL
        otel_collector_url = "opentelemetry-collector-opencensus.aspecto.io"
        if "collectorUrl" in config:
            otel_collector_url = config["collectorUrl"]

        collector_exporter: SpanExporter = OTSpanExporter(
            service_name=self.service_name,
            endpoint=otel_collector_url,
        )
        self.span_processor.add_exporter(collector_exporter)


