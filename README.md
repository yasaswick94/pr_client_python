# Equiwatt API Client
The Equiwatt API Client is a Python package that provides easy access to the Equiwatt SaaS API. This client allows you to interact with the API endpoints to manage assets and other data within your application.

## Installation
You can install the package via pip. Run the following command:

```
pip install git+https://github.com/equiwatt/saas_client_python.git

```
### Usage

Here’s a quick guide on how to initialize and use the EquiwattSaaSClient with the Equiwatt API:

##### Import the Client
First, import the EquiwattSaaSClient class from the equiwatt_api.client module.

```
from equiwatt_api.client import EquiwattSaaSClient
```

##### Initialize the Client
Create an instance of EquiwattSaaSClient by providing your api_key and tenant_id.

```
client = EquiwattSaaSClient(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID"
)
```

Replace YOUR_API_KEY and YOUR_TENANT_ID with your actual API key and tenant ID.

##### Enable Sandbox Mode
To test your integration without affecting live data, you can enable sandbox mode.

```
client.enable_sandbox()

```


### Documentation
For more detailed documentation on how to use the EquiwattSaaSClient, including methods for interacting with various endpoints, please refer to the official documentation.


### License
This project is licensed under the MIT License. See the LICENSE file for details.