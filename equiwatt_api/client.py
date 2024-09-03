import uuid
import requests
from .models import AssetCreatePayload
from .exceptions import EquiwattAPIException
from pydantic import ValidationError
from typing import Literal
from datetime import datetime


class EquiwattSaaSClient:
    def __init__(self, api_key, base_url=""):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

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
            raise EquiwattAPIException(f"Failed to create asset: {response.status_code} {response.text}")
        
        return response.json()
