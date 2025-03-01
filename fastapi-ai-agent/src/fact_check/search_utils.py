from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
import os
import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json
dotenv.load_dotenv()

class SearchEngine():
    def __init__(self, cse, api):
        self.client = GoogleSearchAPIWrapper(google_api_key=api, google_cse_id=cse)
        self.fact_check_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a fact-checking assistant that verifies claims against various sources found on the web.
        
        Given the search results, determine if the claim is:
        - TRUE: The claim is supported by evidence from reliable sources
        - FALSE: The claim is contradicted by evidence from reliable sources
        - PARTIALLY TRUE: Some aspects of the claim are true while others are false or misleading
        - UNVERIFIABLE: Not enough information from reliable sources to verify the claim
        
        Explain your reasoning, cite the specific sources that support your determination, and include direct quotes from these sources when relevant.
        
        When evaluating sources, consider their reliability and credibility. Academic sources, reputable news organizations, and official government or institutional websites are generally more reliable.
        
        Always maintain a neutral, objective tone and avoid speculation beyond what the evidence supports.
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
        return self.client.results(query)

class FactChecker():
    def __init__(self, llm_api, cse, google_api):
        self.llm = ChatOpenAI(api_key=llm_api)
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
