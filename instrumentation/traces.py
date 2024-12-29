# MAIS EM: https://opentelemetry.io/docs/languages/python/instrumentation/

import asyncio
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
import aiosqlite

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("example.tracer")

async def setup_database():
    async with aiosqlite.connect("example.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        """)
        await db.execute("INSERT INTO users (name) VALUES ('Manoel Gomes')")
        await db.execute("INSERT INTO users (name) VALUES ('Gugu Gaiteiro')")
        await db.commit()

async def fetch_data_from_db():
    with tracer.start_as_current_span("fetch_data_from_db") as span:
        async with aiosqlite.connect("example.db") as db:
            span.set_attribute("db.query", "SELECT * FROM users")
            cursor = await db.execute("SELECT * FROM users")
            rows = await cursor.fetchall()
            span.set_attribute("db.rows_returned", len(rows))
            return rows

async def main():
    await setup_database()

    data = await fetch_data_from_db()
    print("Data from DB:", data)

asyncio.run(main())


# é possivel passar como decorador:
@tracer.start_as_current_span("do_work")
def do_work():
    print("doing some work...")


# span é basicamente o GOAT, entender como criar e gerenciar e vapo, é possivel buscar infos de um span e tals

