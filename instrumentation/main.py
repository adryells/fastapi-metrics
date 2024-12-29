from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
import asyncio

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("example.tracer")

app = FastAPI()

async def fetch_data_from_db():
    with tracer.start_as_current_span("fetch_data_from_db") as span:
        await asyncio.sleep(1)
        span.set_attribute("db.query", "SELECT * FROM users")
        span.set_attribute("db.duration", "1s")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

async def process_data(data):
    with tracer.start_as_current_span("process_data") as span:
        await asyncio.sleep(0.5)
        span.set_attribute("data.count", len(data))
        return [user["name"].upper() for user in data]

@app.get("/process-users")
async def process_users():
    with tracer.start_as_current_span("process_users_endpoint") as span:
        data = await fetch_data_from_db()
        processed_data = await process_data(data)
        span.set_attribute("endpoint.success", True)
        return {"processed_users": processed_data}
