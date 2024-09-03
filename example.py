
from datetime import datetime

from equiwatt_api.client import EquiwattSaaSClient

client = EquiwattSaaSClient(api_key="your_api_key_here")
client.enable_sandbox()

response = client.create_asset(
    userId="5daa97fe-3d17-48bd-88c6-9ff89a517179",
    assetId="78ff368e-35f1-4a5e-adda-71a517d25cc6",
    eventSchemeUUID="1e488632-1063-49f9-a6ab-60fd0f441338",
    name="Smart Meter A",
    assetType="SMARTMETER",
    installationDate=datetime.now().isoformat(),
    locationPostcode="NE83DF",
    locationBuildingNoOrName="equiwatt",
    locationAddress="PROTO, Abbott's Hill",
    locationLatitude="54.9",
    locationLongitude="1.59"
)

print(response)
