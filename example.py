
from datetime import datetime

from equiwatt_api.client import EquiwattSaaSClient

client = EquiwattSaaSClient(api_key="your_api_key_here", tenant_id="785e92f7-7c87-4c30-8a09-f57b3b6a65d7")
client.enable_sandbox()

# response = client.create_asset(
#     userId="5daa97fe-3d17-48bd-88c6-9ff89a517179",
#     assetId="78ff368e-35f1-4a5e-adda-71a517d25cc6",
#     eventSchemeUUID="1e488632-1063-49f9-a6ab-60fd0f441338",
#     name="Smart Meter A",
#     assetType="SMARTMETER",
#     installationDate=datetime.now().isoformat(),
#     locationPostcode="NE83DF",
#     locationBuildingNoOrName="equiwatt",
#     locationAddress="PROTO, Abbott's Hill",
#     locationLatitude="54.9",
#     locationLongitude="1.59"
# )

# for item in client.get_event_asset_baselines(event_uuid='2b488d39-b752-49ed-94aa-8827e2f6e280', chunk_size=1):
#     print(item[0].asset.assetId)
#     print(item[0].value)
#     print('---------')