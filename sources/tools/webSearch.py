
import os
import requests
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utility import animate_thinking, pretty_print
    from tools import Tools
else:
    from sources.tools.tools import Tools
    from sources.utility import animate_thinking, pretty_print

class webSearch(Tools):
    def __init__(self, api_key: str = None):
        """
        A tool to perform a Google search and return information from the first result.
        """
        super().__init__()
        self.tag = "web_search"
        self.api_key = api_key or os.getenv("SERPAPI_KEY")  # Requires a SerpApi key

    def execute(self, blocks: str, safety: bool = True) -> str:
        if self.api_key is None:
            return "Error: No SerpApi key provided."
        for block in blocks:
            query = block.strip()
            pretty_print(f"Searching for: {query}", color="status")
            if not query:
                return "Error: No search query provided."

            try:
                url = "https://serpapi.com/search"
                params = {
                    "q": query,
                    "api_key": self.api_key,
                    "num": 100,
                    "output": "json"
                }
                response = requests.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                results = []
                if "organic_results" in data and len(data["organic_results"]) > 0:
                    for result in data["organic_results"][:50]:
                        title = result.get("title", "No title")
                        snippet = result.get("snippet", "No snippet available")
                        link = result.get("link", "No link available")
                        results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}")
                    return "\n\n".join(results)
                else:
                    return "No results found for the query."
            except requests.RequestException as e:
                return f"Error during web search: {str(e)}"
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        return "No search performed"

    def execution_failure_check(self, output: str) -> bool:
        return output.startswith("Error") or "No results found" in output

    def interpreter_feedback(self, output: str) -> str:
        if self.execution_failure_check(output):
            return f"Web search failed: {output}"
        return f"Web search result:\n{output}"


if __name__ == "__main__":
    search_tool = webSearch(api_key=os.getenv("SERPAPI_KEY"))
    query = "when did covid start"
    result = search_tool.execute([query], safety=True)
    feedback = search_tool.interpreter_feedback(result)
    print(feedback)