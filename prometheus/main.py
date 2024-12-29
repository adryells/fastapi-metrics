from prometheus_client import start_http_server
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import time
import random

resource = Resource(attributes={
    SERVICE_NAME: "example-service"
})

start_http_server(port=9464, addr="localhost")

reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("example-meter")

request_counter = meter.create_counter(
    name="http_request_count",
    unit="1",
    description="Número total de requisições HTTP"
)

active_requests = meter.create_observable_gauge(
    name="http_active_requests",
    unit="1",
    description="Número atual de requisições em processamento",
    callbacks=[lambda: [({"endpoint": "/example"}, active_requests_count)]]
)

response_time_histogram = meter.create_histogram(
    name="http_response_time",
    unit="ms",
    description="Tempo de resposta das requisições HTTP em milissegundos"
)

active_requests_count = 0

def process_request():
    global active_requests_count

    active_requests_count += 1
    request_counter.add(1, {"endpoint": "/example"})

    response_time = random.uniform(100, 500)  # Tempo de resposta em ms
    time.sleep(response_time / 1000)  # Converte ms para segundos
    response_time_histogram.record(response_time, {"endpoint": "/example"})

    active_requests_count -= 1

if __name__ == "__main__":
    print("Servidor de métricas iniciado em http://localhost:9464/metrics")
    while True:
        process_request()
