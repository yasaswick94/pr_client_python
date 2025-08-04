from typing import List, Literal, Optional
from pydantic import BaseModel


class AssetCreatePayload(BaseModel):
    userId: str
    assetId: str
    eventSchemeUUID: Optional[str] = None
    name: str
    assetType: Literal["SMARTMETER"]
    installationDate: Optional[str] = None
    locationPostcode: str
    locationBuildingNoOrName: str
    locationAddress: str
    locationLatitude: Optional[str] = None
    locationLongitude: Optional[str] = None
    exportMpan: Optional[str] = None
    hhSettled: Optional[bool] = False
    bmuId: Optional[str] = None
    eventSchemeOptedInDateTime: Optional[str] = None

    class Config:
        extra = "forbid"


class EventAssetOptPayloadStatus(BaseModel):
    assetUUIDs: List[str]
    status: str

    class Config:
        extra = "forbid"


class EventAssetOptPayload(BaseModel):
    statuses: List[EventAssetOptPayloadStatus]

    class Config:
        extra = "forbid"


class EnergyConsumptionDataPoint(BaseModel):
    assetUUID: str
    timestamp: int
    value: float
    type: Literal["import", "export"]

    class Config:
        extra = "forbid"


class EventAssetOptOutPayload(BaseModel):
    assetUUIDs: List[str]

    class Config:
        extra = "forbid"
