from random import randint

import uvicorn
from fastapi import FastAPI
from opentelemetry import trace, metrics

app = FastAPI()
tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")

roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value",
)

@app.post("/rolldice")
def roll_dice(player: str = ""):
    with tracer.start_as_current_span("rolldice") as rollspan:
        result = str(randint(1, 6))
        rollspan.set_attribute("rolldice.value", result)
        roll_counter.add(1, {"roll.value": result})

        if player:
            print(f"{player} is rolling the dice: {result}")
        else:
            print(f"Anonymous player is rolling the dice: {result}")
        return result



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)