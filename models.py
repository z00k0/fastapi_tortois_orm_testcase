from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from typing import List, Dict


class Tariff(models.Model):
    id = fields.IntField(pk=True)
    cargo_type = fields.CharField(max_length=20)
    rate = fields.CharField(max_length=10)


class Tariffs(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    tariffs = fields.ManyToManyField(
        "models.Tariff", related_name="tariffs", through="tariffs_tariff"
    )


class TariffItem(BaseModel):
    cargo_type: str
    rate: float


class TariffRequest(BaseModel):
    tariffs: Dict[str, List[TariffItem]]


Tariff_Pydantic = pydantic_model_creator(Tariff, name="Tariff")
TariffIn_Pydantic = pydantic_model_creator(
    Tariff, name="TariffIn", exclude_readonly=True
)
