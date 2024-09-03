from typing import Literal
from pydantic import BaseModel


class AssetCreatePayload(BaseModel):
    userId: str
    assetId: str
    eventSchemeUUID: str
    name: str
    assetType: Literal['SMARTMETER']
    installationDate: str
    locationPostcode: str
    locationBuildingNoOrName: str
    locationAddress: str
    locationLatitude: str
    locationLongitude: str

    class Config:
        extra = 'forbid'
