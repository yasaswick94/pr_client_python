import uuid
import hmac
import hashlib
import requests
from typing import Iterator, List
from equiwatt_api.response import AssetDetails, EventAssetBaseline, EventAssetState, EventDetails
from equiwatt_api.schema.paginator import PowerResponsePaginatedResponse
from .schema.asset import (
    AssetCreatePayload,
    EnergyConsumptionDataPoint,
    EventAssetOptPayload,
    EventAssetOptPayloadStatus,
    EventAssetOptOutPayload
)
from .exceptions import EquiwattAPIException
from pydantic import ValidationError
from typing import Dict, Literal
from datetime import datetime


class EquiwattSaaSClient:
    def __init__(self, api_key: str, tenant_id: str, base_url="", version: str = "1.0"):
        if api_key and tenant_id:
            try:
                uuid.UUID(tenant_id)
            except ValueError:
                raise EquiwattAPIException("Invalid tenant ID")
            self.base_url = base_url
            self.api_key = api_key
            self.headers = {"tenant": tenant_id, "x-api-key": f"{self.api_key}", "Content-Type": "application/json"}
            if version:
                self.headers["x-api-version"] = version
        else:
            raise EquiwattAPIException("API key and tenant id are required")

    def enable_sandbox(self):
        self.base_url = "https://sandbox.equiwatt.com"

    def set_service_url(self, url):
        self.base_url = url

    def create_asset(
        self,
        userId: str,
        assetId: str,
        name: str,
        assetType: Literal["SMARTMETER"],
        locationPostcode: str,
        locationBuildingNoOrName: str,
        locationAddress: str,
        locationLatitude: str,
        locationLongitude: str,
        installationDate: datetime = None,
        eventSchemeUUID: uuid.uuid4 = None,
    ):
        """
        Create an asset in the Equiwatt SaaS platform, all fields are required
        Args:
            userId (str): The user ID associated with the asset.
            assetId (str): The unique identifier for the asset.
            eventSchemeUUID (UUID): The UUID for the event scheme.
            name (str): The name of the asset.
            assetType (Literal['SMARTMETER']): The type of the asset.
            installationDate (datetime): The installation date of the asset.
            locationPostcode (str): The postcode of the asset's location.
            locationBuildingNoOrName (str): The building number or name of the asset's location.
            locationAddress (str): The address of the asset's location.
            locationLatitude (str): The latitude of the asset's location.
            locationLongitude (str): The longitude of the asset's location.

        Returns:
            Dict: The response from the API as a dictionary.

        Raises:
            EquiwattAPIException: If there is an error in creating the asset or if the API call fails.
        """
        try:
            payload = AssetCreatePayload(
                userId=userId,
                assetId=assetId,
                eventSchemeUUID=eventSchemeUUID,
                name=name,
                assetType=assetType,
                installationDate=installationDate,
                locationPostcode=locationPostcode,
                locationBuildingNoOrName=locationBuildingNoOrName,
                locationAddress=locationAddress,
                locationLatitude=locationLatitude,
                locationLongitude=locationLongitude,
            )
        except ValidationError as e:
            raise EquiwattAPIException(f"Invalid payload data: {e.json()}")

        url = f"{self.base_url}/api/v1/assets"
        response = requests.post(url, json=payload.model_dump(), headers=self.headers)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    def create_bulk_assets(self, assets: list):
        """
        Create multiple assets in the Equiwatt SaaS platform.

        Args:
            assets (list): A list of AssetCreatePayload objects.

        Returns:
            Dict: The response from the API as a dictionary.

        Raises:
            EquiwattAPIException: If there is an error in creating the assets or if the API call fails.
        """
        url = f"{self.base_url}/api/v1/assets/bulk"
        validated_assets = []
        for asset in assets:
            try:
                validated_assets.append(AssetCreatePayload(**asset))
            except ValidationError as e:
                raise EquiwattAPIException(f"Invalid payload data: {e.json()}")
        payload = {"assets": [asset.model_dump() for asset in validated_assets]}
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    def _get_paginated_assets(
        self, page: int = 1, items_per_page: int = 100
    ) -> PowerResponsePaginatedResponse[AssetDetails]:
        """
        Get assets registered in powerResponse platform.

        Args:
            assetUUID (str): The UUID of the asset to archive, this is different from the assetId.

        Returns:
            True: If the asset is successfully archived.
        """

        url = f"{self.base_url}/api/v1/assets?page={page}&pageSize={items_per_page}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return PowerResponsePaginatedResponse[AssetDetails](AssetDetails, **data)

    def get_assets(self, chunk_size: int = 100) -> Iterator[List[AssetDetails]]:
        """
        This is a generator function that yields a list of assets registered in the powerResponse platform.

        Args:
            chunk_size (int, optional): The number of items per chunk. Defaults to 100.
        """
        page = 1
        while True:
            paginated_response = self._get_paginated_assets(page=page, items_per_page=chunk_size)
            yield paginated_response.items
            if paginated_response.pagination.currentPage >= paginated_response.pagination.totalPages:
                break
            page += 1

    def archive_asset(self, assetUUID: str):
        """
        Archive an asset in the Equiwatt SaaS platform.

        Args:
            assetUUID (str): The UUID of the asset to archive, this is different from the assetId.

        Returns:
            True: If the asset is successfully archived.
        """

        url = f"{self.base_url}/api/v1/assets/{assetUUID}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)
        return True

    def get_scheme_list(self):
        """
        Get the list of allowed event schemes.

        Returns:
            Dict: The response from the API as a dictionary.
        """
        url = f"{self.base_url}/api/v1/event-schemes"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    def create_user(self, user_id: str):
        """
        Create a user in the equiwatt PowerResponse platform.

        Returns:
            Dict: The response from the API as a dictionary.
        """
        url = f"{self.base_url}/api/v1/users"
        payload = {"userId": user_id}
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    def get_webhooks(self, page: int = 1, items_per_page: int = 10) -> PowerResponsePaginatedResponse[Dict]:
        """
        Get the list of webhooks

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            items_per_page (int, optional): The number of items per page. Defaults to 10.

        Returns:
            Pagination[Dict]: A Pagination object containing webhooks and pagination details.

        Raises:
            EquiwattAPIException: If there is an error in retrieving the webhooks or if the API call fails.
        """
        url = f"{self.base_url}/api/v1/webhooks?page={page}&pageSize={items_per_page}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return PowerResponsePaginatedResponse[Dict](**data)

    def create_webhook_subcription(self, name: str, url: str, eventTypes: List[str]):
        """
        Get the list of allowed event schemes.

        Returns:
            Dict: The response from the API as a dictionary.
        """
        payload = {"name": name, "url": url, "eventTypes": eventTypes}
        url = f"{self.base_url}/api/v1/webhooks/subscribe"
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    def delete_webhook_subcription(self, webhook_uuid: str):
        """
        Delete a webhook subscription

        Returns:
            True: If the webhook is successfully deleted.
        """
        url = f"{self.base_url}/api/v1/webhooks/{webhook_uuid}/unsubscribe"
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)
        return True

    def get_event_details(self, event_uuid: str) -> EventDetails:
        """
        Get event details

        Returns:
            True: If the webhook is successfully deleted.
        """
        url = f"{self.base_url}/api/v1/events/{event_uuid}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)
        return EventDetails(response.json())

    def _get_paginated_event_assets(
        self, event_uuid: str, page: int = 1, items_per_page: int = 100
    ) -> PowerResponsePaginatedResponse[EventAssetState]:
        """
        Get event details

        Returns:
            True: If the webhook is successfully deleted.
        """
        url = f"{self.base_url}/api/v1/events/{event_uuid}/assets?page={page}&pageSize={items_per_page}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)
        data = response.json()
        return PowerResponsePaginatedResponse[EventAssetState](EventAssetState, **data)

    def get_event_assets(self, event_uuid: str, chunk_size: int = 100) -> Iterator[List[EventAssetState]]:
        """
        This is a generator function that yields a list of assets registered in the powerResponse platform.

        Args:
            chunk_size (int, optional): The number of items per chunk. Defaults to 100.
        """
        page = 1
        while True:
            paginated_response = self._get_paginated_event_assets(
                event_uuid=event_uuid, page=page, items_per_page=chunk_size
            )
            yield paginated_response.items
            if paginated_response.pagination.currentPage >= paginated_response.pagination.totalPages:
                break
            page += 1

    def _get_paginated_event_asset_baselines(
        self, event_uuid: str, page: int = 1, items_per_page: int = 100
    ) -> PowerResponsePaginatedResponse[EventAssetBaseline]:
        """
        Get event details

        Returns:
            True: If the webhook is successfully deleted.
        """
        url = f"{self.base_url}/api/v1/events/{event_uuid}/baselines?page={page}&pageSize={items_per_page}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)
        data = response.json()
        return PowerResponsePaginatedResponse[EventAssetBaseline](EventAssetBaseline, **data)

    def get_event_asset_baselines(self, event_uuid: str, chunk_size: int = 100) -> Iterator[List[EventAssetBaseline]]:
        """
        This is a generator function that yields a list of assets registered in the powerResponse platform.

        Args:
            chunk_size (int, optional): The number of items per chunk. Defaults to 100.
        """
        page = 1
        while True:
            paginated_response = self._get_paginated_event_asset_baselines(
                event_uuid=event_uuid, page=page, items_per_page=chunk_size
            )
            yield paginated_response.items
            if paginated_response.pagination.currentPage >= paginated_response.pagination.totalPages:
                break
            page += 1

    def event_asset_opt_in(self, event_uuid: str, asset_uuids: List[str], status: str):
        """
        Opt in or out of an event
        """
        try:
            payloadStatus = EventAssetOptPayloadStatus(assetUUIDs=asset_uuids, status=status)
            payload = EventAssetOptPayload(statuses=[payloadStatus])
        except ValidationError as e:
            raise EquiwattAPIException(f"Invalid payload data: {e.json()}")

        url = f"{self.base_url}/api/v1/events/{event_uuid}/asset-optin"
        response = requests.post(url, json=payload.model_dump(), headers=self.headers)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    def scheme_asset_opt_in(self, scheme_uuid: str, asset_uuids: List[str], status: str):
        """
        Opt in or out a list of assets to/from a scheme
        states = ["OPT_IN", "OPT_OUT"]
        """
        try:
            payloadStatus = EventAssetOptPayloadStatus(assetUUIDs=asset_uuids, status=status)
            payload = EventAssetOptPayload(statuses=[payloadStatus])
        except ValidationError as e:
            raise EquiwattAPIException(f"Invalid payload data: {e.json()}")

        url = f"{self.base_url}/api/v1/event-schemes/{scheme_uuid}/assets-optin"
        response = requests.post(url, json=payload.model_dump(), headers=self.headers)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    def scheme_asset_opt_out(self, asset_uuids: List[str]):
        """
        Opt out asset from all schemes
        """
        try:
            payload = EventAssetOptOutPayload(assetUUIDs=asset_uuids)
        except ValidationError as e:
            raise EquiwattAPIException(f"Invalid payload data: {e.json()}")

        url = f"{self.base_url}/api/v1/event-schemes/assets/opt-out"
        response = requests.post(url, json=payload.model_dump(), headers=self.headers)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    # Energy data

    def send_energy_readings(self, readings: List[EnergyConsumptionDataPoint]):
        """
        Send energy readings to the Equiwatt powerResponse platform
        """
        try:
            payload = [reading.model_dump() for reading in readings]
        except ValidationError as e:
            raise EquiwattAPIException(f"Invalid payload data: {e.json()}")

        url = f"{self.base_url}/api/v1/energy-consumption"
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code != 201:
            raise EquiwattAPIException.from_response(response)
        return response.json()

    # Webhook signature verification

    def hash_challenge(self, amt: str, challenge: str) -> str:
        h = hmac.new(amt.encode(), challenge.encode(), hashlib.sha256)
        return h.hexdigest()

    def verify_payload(self, token: str, signature: str, body: str) -> bool:
        """
        Verify webhook signature
        """
        return self.hash_challenge(token, body) == signature

    def connect_asset_tariffs(self, asset_uuid: str, direction: str="import") -> str:
        """
        Return tariff connect URL for asset.
        """
        url = f"{self.base_url}/api/assets/{asset_uuid}/tariff/connect/{direction}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return data

    def get_asset_tariffs(self, asset_uuid: str, page: int = 1, page_size: int = 10, direction: str = 'import'):
        """
        Return asset tariffs
        """
        url = f"{self.base_url}/api/assets/{asset_uuid}/tariff/{direction}?page={page}&pageSize={page_size}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return data

    def disconnect_asset_tariffs(self, asset_uuid: str, direction: str = "import") -> str:
        """
        Disconnect asset tariff.
        """
        url = f"{self.base_url}/api/assets/{asset_uuid}/tariff/{direction}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return data

    def get_asset_tariff_plans(self, asset_uuid: str):
        """
        Return asset tariff plans
        """
        url = f"{self.base_url}/api/assets/{asset_uuid}/tariff-plans"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return data

    def enable_asset_tariff_schedules(self, asset_uuid: str, tariff_type: str):
        """
        Enable asset tariff schedules
        """
        if not tariff_type in ['import', 'export', 'supply']:
            raise EquiwattAPIException(f"Invalid tariff schedule type: {tariff_type}")

        url = f"{self.base_url}/api/assets/{asset_uuid}/tariff/schedules/{tariff_type}"
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return data

    def refresh_asset_tariff_schedules(self, asset_uuid: str, tariff_type: str):
        """
        Enable asset tariff schedules
        """
        if not tariff_type in ['import', 'export', 'supply']:
            raise EquiwattAPIException(f"Invalid tariff schedule type: {tariff_type}")

        url = f"{self.base_url}/api/assets/{asset_uuid}/tariff/schedules/{tariff_type}/refresh"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return data

    def get_asset_tariff_schedules(self, asset_uuid: str, tariff_type, page: int = 1, page_size: int = 10):
        """
        Return asset tariff schedules
        """
        url = f"{self.base_url}/api/assets/{asset_uuid}/tariff/schedules/{tariff_type}?page={page}&pageSize={page_size}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return data
