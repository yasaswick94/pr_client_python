from typing import List, Literal, Optional
from pydantic import BaseModel


class AssetCreatePayload(BaseModel):
    userId: str
    assetId: str
    eventSchemeUUID: Optional[str] = None
    name: str
    assetType: Literal['SMARTMETER']
    installationDate: Optional[str] = None
    locationPostcode: str
    locationBuildingNoOrName: str
    locationAddress: str
    locationLatitude: Optional[str] = None
    locationLongitude: Optional[str] = None

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
