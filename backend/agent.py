# =============================================================================
# Agent module for RAG Assistant
# =============================================================================
# This file creates an AI agent that can DECIDE when to search the database.
# Instead of always retrieving passages, the LLM chooses when retrieval helps.
# =============================================================================

from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from backend.database import RAGDatabase

class RAGAgent:
    def __init__(self, 
                 db: RAGDatabase, 
                 model_name: str, 
                 max_iter: int):
        self.db = db
        self.model_name = model_name
        self.max_iter = max_iter
        self.last_sources = []  # We'll store retrieved passages here for the UI

    def create_tool(self):
        # ---------------------------------------------------------------------
        # The @tool decorator transforms this function into something the
        # LLM can call. The docstring is CRUCIAL—it's what the LLM reads
        # to decide whether and how to use this tool.
        # ---------------------------------------------------------------------
        @tool("Query RAG Database")
        def query_rag_db(query: str) -> str:
            """Search the vector database containing customized texts.
            
            Args:
                query: Search query about topic.
                
            Returns:
                Relevant passages from the database
            """
            try:
                results = self.db.query(query)
                
                if results:
                    # Store sources for UI display
                    self.last_sources.extend(results)
                    
                    # Format passages for the LLM to read
                    passages = [row["text"] for row in results]
                    return "\n\n---\n\n".join([f"Passage {i+1}:\n{doc}" for i, doc in enumerate(passages)])
                else:
                    return "No relevant passages found."
                    
            except Exception as e:
                return f"Error querying database: {str(e)}"
        
        return query_rag_db

    # TO DO: Update the ask() function
    def ask(self, question: str) -> dict:
        """
        Ask a question to the agent.
        
        Returns:
            Dictionary with 'answer' and 'sources'.
        """
        # Reset sources for this query
        self.last_sources = []
        
        # TO DO: Create the LLM instance
        llm = LLM(
            model=self.model_name,
            temperature=0.5,
            timeout=100,
            max_tokens=5000,
            top_p=0.9,
            frequency_penalty=0.05,
            presence_penalty=0.05
        )

        # TO DO: Call the database tool (e.g. the function above)
        query_tool = self.create_tool()
        

        agent = Agent(
            role='internet toxicity Content Expert and public lecture host',
            goal='Answer questions about internet toxicity using the database',
            backstory='You are an expert who has access to a database with content about internet toxicity, and can explain concepts in simple terms if necessary.',
            tools=[query_tool],
            llm=llm,
            verbose=True, # Shows what the agent is doing
            allow_delegation=False, # Does not create sub-agents
            max_iter=self.max_iter # Limits tool calls
        )
        
        # TO DO: Create the task
        task = Task(
            description = """
                Answer the given question first by querying the database, then incoporate your own knowledge.
                Prioritize database sources in the answer.
            """,
            expected_output = "A comprehensive and easy-to-understand answer to the question.",
            question = question,
            agent = agent,
            tools = [query_tool]
        )

        # TO DO: Create the Crew and run it
        crew = Crew(
            llm=llm,
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Returns the answer and sources
        return {
            "answer": str(result),
            "sources": self.last_sources.copy()
        }
