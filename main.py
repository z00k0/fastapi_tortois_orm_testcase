# from typing import List
import datetime
from fastapi import FastAPI, HTTPException
from models import (
    Tariff,
    Tariffs,
    Tariff_Pydantic,
    TariffIn_Pydantic,
    TariffRequest,
    TariffItem,
)
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
import uvicorn
from typing import List, Dict

app = FastAPI(title="FastAPI Tortoise ORM tastcase for SMIT")


@app.post("/api/tariffs")
async def upload_tariffs(tariff_request: Dict[str, List[TariffItem]]):
    for key, item in tariff_request.items():
        date = key
        tariffs_obj = await Tariffs.create(date=date)
        for tariff in item:
            cargo_type = tariff.cargo_type
            rate = tariff.rate
            tariff_obj = await Tariff.create(cargo_type=cargo_type, rate=rate)
            await tariffs_obj.tariffs.add(tariff_obj)

    return {"message": "Tariffs uploaded successfully"}


@app.get("/calculate-insurance-cost")
async def calculate_insurance_cost(date: str, declared_value: float, cargo_type: str):
    t_obj = (
        await Tariff.filter(cargo_type__iexact=cargo_type)
        .filter(tariffs__date__lte=date)
        .first()
    )
    if not t_obj:
        return {"error": "No tariffs found for the specified date or cargo type"}

    insurance_cost = declared_value * float(t_obj.rate)
    return {"insurance_cost": insurance_cost}


register_tortoise(
    app,
    db_url="sqlite://sqlite3.db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
