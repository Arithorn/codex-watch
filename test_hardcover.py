import os
import json
from pathlib import Path
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

# --- Configuration ---
HARDCOVER_API_KEY = os.environ.get("HARDCOVER_API_KEY")
HARDCOVER_GRAPHQL_ENDPOINT = "https://api.hardcover.app/v1/graphql"  # Correct endpoint

# Correct Authentication Header for Bearer Token
AUTH_HEADERS = {"authorization": f"Bearer {HARDCOVER_API_KEY}"}

# --- !! IMPORTANT: Replace with the Author ID you found !! ---
# Example: If the author ID you found is "a_random_string_123"
AUTHOR_ID_TO_QUERY = "344878"
# ---

# --- Check Configuration ---
if not HARDCOVER_API_KEY:
    print("ERROR: HARDCOVER_API_KEY environment variable not set.")
    exit()

# --- Setup GraphQL Client ---
transport = RequestsHTTPTransport(
    url=HARDCOVER_GRAPHQL_ENDPOINT,
    headers=AUTH_HEADERS,
    use_json=True,
)

# Consider setting fetch_schema_from_transport=True if you want the client
# to try and download the schema for validation/introspection (might add startup time)
client = Client(transport=transport, fetch_schema_from_transport=False)

# --- Define GraphQL Query for Author and their Books ---
# This query uses a variable $authorId of type ID! (ID is a common GraphQL type, ! means required)
# We fetch the author's name and the id, title, and publishedYear for their books.
# You might need to adjust field names (e.g., 'publishedYear', 'books') based on
# what you saw in the playground or Hardcover's actual schema.


def load_query(query_name: str) -> str:
    path = Path(f"queries/{query_name}.graphql")
    return path.read_text()


query = load_query("hardcover/books_by_author_id")
query2 = load_query("hardcover/author_id_from_name")

get_author_books_query = gql(query)
get_author_id_query = gql(query2)

# --- Set Query Variables ---
# This dictionary maps the variable name in the query ($authorId) to its value
variable_values = {"authorId": AUTHOR_ID_TO_QUERY}
variable_values2 = {"name": "Zogarth"}

# --- Execute the Query ---
# print(f"--- Querying Hardcover for Author ID: {AUTHOR_ID_TO_QUERY} ---")
print(f"--- Get Zogarth Author ID")
try:
    # result = client.execute(get_author_books_query,
    #                         variable_values=variable_values)
    result = client.execute(get_author_id_query,
                            variable_values=variable_values2)

    print("\n--- Result ---")
    print(json.dumps(result, indent=2))  # Pretty print the JSON result

except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"An error occurred: {e}")
    # Consider more specific error handling, e.g., for transport errors
    # from gql.transport.exceptions import TransportQueryError
    # if isinstance(e, TransportQueryError):
    #     print(f"Server responded with errors: {e.errors}")

print("-" * 30)
