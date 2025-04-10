import os
import json
from pathlib import Path
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


class HardCover:
    def __init__(self):

        self.config = {
            'hardcover_api_key': os.environ.get("HARDCOVER_API_KEY"),
            'hardcover_endpoint': os.environ.get("HARDCOVER_ENDPOINT")
        }
        if not self.config.get("hardcover_api_key"):
            print("ERROR: HARDCOVER_API_KEY environment variable not set.")
            exit()
        if not self.config.get("hardcover_endpoint"):
            print("ERROR: HARDCOVER_ENDPOINT environment variable not set.")
            exit()
        self.headers = {
            "authorization": f"Bearer {self.config.get("hardcover_api_key")}"}
        self.transport = RequestsHTTPTransport(
            url=self.config.get("hardcover_endpoint"),
            headers=self.headers,
            use_json=True,
        )
        self.client = Client(transport=self.transport,
                             fetch_schema_from_transport=False)
        pass

    def load_query(self, query_name: str) -> str:
        path = Path(f"queries/{query_name}.graphql")
        return path.read_text()

    def getAuthorId(self, authorName) -> int:
        self.query = self.load_query("hardcover/author_id_from_name")
        self.get_author_id_query = gql(self.query)
        self.values = {'name': authorName}
        self.executeQuery(query=self.query, variable_values=self.values)
        return 1234

    def getBooksByAuthor(self, authorId):
        self.query = self.load_query("hardcover/books_by_author_id")
        # self.query = self.load_query("hardcover/test")
        self.get_author_books_query = gql(self.query)
        self.values = {'authorId': authorId}
        # self.values = {'authorId': "344878"}
        self.executeQuery(query=self.get_author_books_query,
                          variable_values=self.values)

    def executeQuery(self, query, variable_values):
        try:
            print(query)
            # result = self.client.execute(query)
            result = self.client.execute(query,
                                         variable_values=variable_values)

            print("\n--- Result ---")
            print(json.dumps(result, indent=2))  # Pretty print the JSON result
        except Exception as e:
            print(f"\n--- ERROR ---")
            print(f"An error occurred: {e}")
        pass
