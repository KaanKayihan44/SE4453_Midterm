from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = "https://midterm-kvault.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=vault_url, credential=credential)

pg_user = client.get_secret("pg-user").value
pg_password = client.get_secret("pg-password").value
pg_host = client.get_secret("pg-host").value


app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello from the web app!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
