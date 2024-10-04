from typing import List, Literal
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


class EventAssetOptPayloadStatus(BaseModel):
    assetUUIDs: List[str]
    status: str

    class Config:
        extra = 'forbid'


class EventAssetOptPayload(BaseModel):
    statuses: List[EventAssetOptPayloadStatus]

    class Config:
        extra = 'forbid'


