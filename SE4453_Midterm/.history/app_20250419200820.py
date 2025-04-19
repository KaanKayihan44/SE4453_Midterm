from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import psycopg2

# Initialize Flask app
app = Flask(__name__)

# Azure Key Vault configuration
vault_url = "https://midterm-kvault.vault.azure.net/"  # change if you named your vault differently
credential = DefaultAzureCredential()
client = SecretClient(vault_url=vault_url, credential=credential)

# Fetch PostgreSQL secrets from Key Vault
pg_user = "dbadmin"
pg_password = "YourPassword123!"
pg_host = "midterm-pg.postgres.database.azure.com"


# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=pg_host,
        user=pg_user,
        password=pg_password,
        dbname="postgres"  # change if you use a different DB name
    )
    print("✅ Connected to PostgreSQL successfully.")
except Exception as e:
    print("❌ Failed to connect to PostgreSQL:", e)
    conn = None

# Test endpoint
@app.route("/hello")
def hello():
    if conn is None:
        return "❌ No connection to PostgreSQL"

    try:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        return f"✅ Hello from the web app! PostgreSQL version: {version[0]}"
    except Exception as e:
        return f"❌ Error querying PostgreSQL: {str(e)}"

# Run locally (use gunicorn for production)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
