import uuid
import requests

from equiwatt_api.schema.paginator import PowerResponsePaginatedResponse
from .schema.asset import AssetCreatePayload
from .exceptions import EquiwattAPIException
from pydantic import ValidationError
from typing import Dict, Literal
from datetime import datetime


class EquiwattSaaSClient:
    def __init__(self, api_key: str, tenant_id: str, base_url=""):
        if api_key and tenant_id:
            try:
                uuid.UUID(tenant_id)
            except ValueError:
                raise EquiwattAPIException("Invalid tenant ID")
            self.base_url = base_url
            self.api_key = api_key
            self.headers = {
                'tenant': tenant_id,
                'X-API-KEY': f'{self.api_key}',
                'Content-Type': 'application/json'
            }
        else:
            raise EquiwattAPIException("API key and tenant id are required")

    def enable_sandbox(self):
        self.base_url = "https://sandbox.equiwatt.com"

    def set_to_local(self):
        self.base_url = "http://localhost:3000"

    def create_asset(
            self,
            userId: str,
            assetId: str,
            eventSchemeUUID: uuid.uuid4,
            name: str,
            assetType: Literal['SMARTMETER'],
            installationDate: datetime,
            locationPostcode: str,
            locationBuildingNoOrName: str,
            locationAddress: str,
            locationLatitude: str,
            locationLongitude: str):
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
                locationLongitude=locationLongitude
            )
        except ValidationError as e:
            raise EquiwattAPIException(f"Invalid payload data: {e.json()}")

        url = f'{self.base_url}/api/v1/assets'
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
        url = f'{self.base_url}/api/v1/assets/bulk'
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

    def archive_asset(self, assetUUID: str):
        """
        Archive an asset in the Equiwatt SaaS platform.

        Args:
            assetUUID (str): The UUID of the asset to archive, this is different from the assetId.

        Returns:
            True: If the asset is successfully archived.
        """

        url = f'{self.base_url}/api/v1/assets/{assetUUID}'
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
        url = f'{self.base_url}/api/v1/event-schemes'
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
        url = f'{self.base_url}/api/v1/users'
        payload = {
            "userId": user_id
        }
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
        url = f'{self.base_url}/api/v1/webhooks?page={page}&itemsPerPage={items_per_page}'
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)

        data = response.json()
        return PowerResponsePaginatedResponse[Dict](**data)

    def create_webhook_subcription(self, name: str, url: str, eventTypes: list[str]):
        """
        Get the list of allowed event schemes.

        Returns:
            Dict: The response from the API as a dictionary.
        """
        payload = {
            "name": name,
            "url": url,
            "eventTypes": eventTypes
        }
        url = f'{self.base_url}/api/v1/webhooks/subscribe'
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
        url = f'{self.base_url}/api/v1/webhooks/{webhook_uuid}/unsubscribe'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200:
            raise EquiwattAPIException.from_response(response)
        return True
