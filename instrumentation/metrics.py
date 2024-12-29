from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
import time

metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("example.meter")

work_counter = meter.create_counter(
    "work.counter", unit="1", description="Counts the amount of work done"
)

class WorkItem:
    def __init__(self, work_type):
        self.work_type = work_type

def do_work(work_item):
    work_counter.add(1, {"work.type": work_item.work_type})
    print(f"Doing some {work_item.work_type} work...")

def main():
    work_types = ["type_a", "type_b", "type_c"]
    for _ in range(10):
        work_item = WorkItem(work_types[_ % len(work_types)])
        do_work(work_item)
        time.sleep(1)

if __name__ == "__main__":
    main()
