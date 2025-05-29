# SerpApi Retriever

# libraries
import os
import requests
import urllib.parse
import httpx
import uuid

class SearchPlugin():
    """
    SearchPlugin Retriever
    """
    def __init__(self, query, query_domains=None):
        """
        Initializes the SearchPlugin object
        Args:
            query:
        """
        self.query = query
        self.query_domains = query_domains or None
        self.api_key = self.get_api_key()

    def get_api_key(self):
        """
        Gets the SearchPlugin API key
        Returns:

        """
        try:
            api_key = os.environ["SEARCH_PLUGIN_KEY"]
        except:
            raise Exception("SearchPlugin API key not found. Please set the SEARCH_PLUGIN_KEY environment variable.")
        return api_key
    
    def search(self, max_results=7):
        """
        Searches the query
        Returns:

        """
        print("SearchPlugin: Searching with query {0}...".format(self.query))
        """Useful for general internet search queries using SerpApi."""

        body = {
            "query": self.query,
            "search_mode": "serpapi",
            # "is_references_enabled": True,
            # "is_ranker_enabled": True,
            # "doc_count": max_results,
            # "text_sources": True,
            # "images_sources": {},
            # "send_debug_info": False,
            # "text_sources": {"rambler": {}}
        }
        
        headers = {
            "Authorization": f"{self.get_api_key()}",
            "X-User-ID": str(uuid.uuid4()),
            "X-Client-ID": str(uuid.uuid4()),
            "X-Request-ID": str(uuid.uuid4()),
            "X-Session-ID": str(uuid.uuid4()),
        }
        
        search_response = []
        
        try:
            with httpx.Client() as client:
                response = client.post(
                    os.environ.get(
                        "SEARCH_PLUGIN_URL", 
                        "https://gigachat.dev.app.sberdevices.ru/retrieval_proxy"),
                    headers=headers,
                    json=body,
                )
                
                if response.is_success:
                    result = response.json()
                    documents = result.get("payload", {}).get("documents", [])
                    sources = result.get("sources", {})

                    for doc in documents:
                        ref = str(doc.get("reference_keyword"))
                        source = sources.get(ref, {})
                        search_response.append({
                            "title": source.get("title", ""),
                            "href": source.get("url", ""),
                            "body": doc.get("text", "")
                        })
                return search_response
        except Exception as e:
            print(f"Error: {e}. Failed fetching sources. Resulting in empty response.")
            search_response = []
        return search_response
