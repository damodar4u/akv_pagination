from azure.identity import DefaultAzureCredential
from azure.core.rest import HttpRequest
from azure.core.pipeline.transport import RequestsTransport

# Vault details
vault_url = "https://<YourKeyVaultName>.vault.azure.net/"
api_version = "7.5"
max_results = 25  # Azure enforced maximum

# Authenticate
credential = DefaultAzureCredential()
token = credential.get_token("https://vault.azure.net/.default").token

# Headers
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Manual HTTP Request
transport = RequestsTransport()
url = f"{vault_url}/secrets"
params = {"api-version": api_version, "maxresults": max_results}

# Fetch all secrets with pagination
all_secrets = []
next_link = None

while True:
    if next_link:
        # Fetch the next page using nextLink
        request = HttpRequest("GET", next_link, headers=headers)
    else:
        # Fetch the first page
        request = HttpRequest("GET", url, headers=headers, params=params)
    
    # Send the request
    response = transport.send(request)
    response.raise_for_status()
    
    # Parse response
    data = response.json()
    for secret in data.get("value", []):
        all_secrets.append(secret["id"])
        print(f"Secret: {secret['id']}")
    
    # Check for nextLink
    next_link = data.get("nextLink")
    if not next_link:
        break

print(f"\nTotal Secrets Retrieved: {len(all_secrets)}")
