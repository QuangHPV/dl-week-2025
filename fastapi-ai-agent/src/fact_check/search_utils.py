import json
import dotenv
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_community import GoogleSearchAPIWrapper

dotenv.load_dotenv()

class SearchEngine():
    def __init__(self, cse, api):
        self.client = GoogleSearchAPIWrapper(google_api_key=api, google_cse_id=cse, k=3)
        self.fact_check_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a fact-checking assistant that verifies claims against various sources found on the web.
        
        Given the search results, determine if the claim is likely to be:
        - TRUE: The claim is the same as the evidence from reliable sources
        - FALSE: There is any difference between the claim and the information gotten
        - UNVERIFIABLE: Not enough information from reliable sources to verify the claim
        
        Give me a short concise answer and cite sources as needed, be very critical, any differences in the information is considered not good.
        """),
        ("human", "Claim to verify: {claim}\n\nSearch results:\n{search_results}")
        ])

        self.tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=self.client.run,
        )

    def search(self, query):
        return self.tool.run(query)

    def get_links(self, query):
        return self.client.results(query, num_results=3)

class FactChecker():
    def __init__(self, llm_api, cse=None, google_api=None, search_engine=None):
        self.llm = ChatOpenAI(api_key=llm_api)
        # Use the provided search engine or create a new one if not provided
        if search_engine:
            self.searcher = search_engine
        else:
            self.searcher = SearchEngine(cse, google_api)

    def fact_check(self, fact):
        # Generate search queries based on the fact
        query_data = self.generate_query(fact)
        
        # Parse the query data from JSON string to Python object
        queries = json.loads(query_data)
        
        # Initialize a list to store search results for each query
        all_search_results = []
        
        # Execute each search query and collect results
        for query_item in queries["search_queries"]:
            query = query_item["query"]
            search_result = self.searcher.search(query)
            all_search_results.append(f"Query: {query}\nResults: {search_result}\n")
        
        # Combine all search results into a single string
        combined_results = "\n".join(all_search_results)
        
        # Use the fact check prompt with the LLM to analyze the results
        fact_check_chain = self.searcher.fact_check_prompt | self.llm
        
        # Get the fact-checking result
        result = fact_check_chain.invoke({
            "claim": fact,
            "search_results": combined_results
        })
        
        return result

    def generate_query(self, fact):
        prompt = """I need you to help me generate effective Google search queries to verify whether a fact is true or false. For any fact I share with you, please respond ONLY with a JSON object in the following format, with no additional text before or after:

{{
  "fact": "The fact I provided",
  "key_claims": [
    "Claim 1",
    "Claim 2"
  ],
  "search_queries": [
    {{
      "query": "search query 1",
      "look_for": "what to look for in results"
    }},
    {{
      "query": "search query 2",
      "look_for": "what to look for in results"
    }},
    {{
      "query": "search query 3",
      "look_for": "what to look for in results"
    }}
}}

Important guidelines:
- Each query must be self-contained and work independently in Google search
- Formulate complete, specific queries that don't require additional context
- Use neutral language in queries that doesn't presuppose truth or falsehood
- Include search terms that could reveal contradictory information
- Aim for 3-5 search queries
- Suggest specific, credible source types in the recommended_sources array

Here is the fact: {fact}"""
        res = self.llm.invoke(prompt.format(fact=fact))
        queries = json.loads(res.content)
        print(queries)
        return res.content
