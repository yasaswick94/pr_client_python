from typing import Dict, List


class EventDetails():
    incentiveType: str
    uuid: str
    name: str
    type: str
    status: str
    startDateTime: str
    endDateTime: str
    optInRequired: bool
    incentive: float
    eligibility: Dict[str, str]

    def __init__(self, data: Dict):
        self.incentiveType = data.get('incentiveType')
        self.uuid = data.get('uuid')
        self.name = data.get('name')
        self.type = data.get('type')
        self.status = data.get('status')
        self.startDateTime = data.get('startDateTime')
        self.endDateTime = data.get('endDateTime')
        self.optInRequired = data.get('optInRequired')
        self.incentive = data.get('incentive')
        self.eligibility = data.get('eligibility')


class EventAssetOnlyUUID():
    uuid: str

    def __init__(self, data: Dict):
        self.uuid = data.get('uuid')


class EventAsset():
    uuid: str
    assetId: str

    def __init__(self, data: Dict):
        self.uuid = data.get('uuid')
        self.assetId = data.get('assetId')


class EventAssetState():
    asset: EventAsset
    state: str

    def __init__(self, data: Dict):
        self.asset = EventAsset(data.get('asset'))
        self.state = data.get('state')


class AssetDetails():
    uuid: str
    assetId: str
    name: str
    assetType: str
    archived: bool
    installationDate: str
    createdAt: str
    updatedAt: str

    def __init__(self, data: Dict):
        self.uuid = data.get('uuid')
        self.assetId = data.get('assetId')
        self.name = data.get('name')
        self.assetType = data.get('assetType')
        self.archived = data.get('archived')
        self.installationDate = data.get('installationDate')
        self.createdAt = data.get('createdAt')
        self.updatedAt = data.get('updatedAt')


class EventAssetBaselineDetails():
    value: str
    method: str
    type: str

    def __init__(self, data: Dict):
        self.value = data.get("value")
        self.method = data.get("method")
        self.type = data.get("type")


class EventAssetDetails():
    asset: EventAsset
    baselines: List[EventAssetBaselineDetails]

    def __init__(self, data: Dict):
        self.asset = EventAsset(data.get('asset'))
        self.baselines = [EventAssetBaselineDetails(baseline) for baseline in data.get("baselines", [])]


class EventAssetBaseline():
    value: str
    method: str
    asset: EventAsset

    def __init__(self, data: Dict):
        self.value = data.get('value')
        self.method = data.get('method')
        self.asset = EventAsset(data.get('asset'))


class EventAssetStat():
    asset: EventAssetOnlyUUID
    state: str
    energyForecasted: float
    energyConsumed: float
    energySaved: float

    def __init__(self, data: Dict):
        self.asset = EventAssetOnlyUUID(data.get('asset'))
        self.state = data.get('state')
        self.energyForecasted = data.get('energyForecasted')
        self.energyConsumed = data.get('energyConsumed')
        self.energySaved = data.get('energySaved')
