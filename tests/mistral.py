import os
import json
from crewai import Agent, Task, Crew, Process
from langchain_mistralai import ChatMistralAI
from crewai.tools import BaseTool
from ytmusicapi import YTMusic
# Corrected line
from pydantic import BaseModel, Field
# --- IMPORTANT SECURITY NOTE ---
# Always load API keys from environment variables, not hardcoded in the script.
# In your terminal: export MISTRAL_API_KEY='your_real_api_key'
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

# 1. Define the Input Schema for the Custom Tool
class YouTubeMusicSearchToolInput(BaseModel):
    """Input for the YouTube Music Search Tool."""
    query: str = Field(..., description="The string of keywords to search for.")
    limit: int = Field(5, description="The maximum number of songs to return.")

# 2. Define the Custom Tool for YouTube Music Search
class YouTubeMusicSearchTool(BaseTool):
    name: str = "YouTube Music Search"
    description: str = "Searches YouTube Music for songs based on a string of keywords. Returns a list of matching songs with their titles and links."
    args_schema: type[BaseModel] = YouTubeMusicSearchToolInput

    def _run(self, query: str, limit: int = 5) -> str:
        """
        Uses ytmusicapi to search for songs and returns a JSON formatted string
        of the results.
        """
        try:
            ytmusic = YTMusic()
            # The limit parameter is now used in the search
            search_results = ytmusic.search(query, filter="songs", limit=limit)
            
            formatted_results = []
            for song in search_results:
                formatted_results.append({
                    "title": song['title'],
                    "link": f"https://music.youtube.com/watch?v={song['videoId']}"
                })
            
            return json.dumps(formatted_results, indent=2)
        except Exception as e:
            return f"An error occurred during search: {str(e)}"

# 3. Set up the LLM
# The model name 'mistral/mistral-large-latest' is correct for telling LiteLLM which provider to use.
llm = ChatMistralAI(
    api_key=MISTRAL_API_KEY,
    model="mistral/mistral-large-latest"
)

# Instantiate the custom tool
music_search_tool = YouTubeMusicSearchTool()

# 4. Define Your Agents
keyword_extractor = Agent(
  role='Keyword Extraction Specialist',
  goal='Extract relevant and effective search keywords from a user\'s natural language query about songs.',
  backstory="""You are an expert in understanding user sentiment and intent.
  Your specialty is breaking down complex or vague requests into simple,
  powerful keywords that can be used for precise database and API searches.""",
  verbose=True,
  allow_delegation=False,
  llm=llm
)

music_searcher = Agent(
  role='YouTube Music Discovery Expert',
  goal='Find song recommendations on YouTube Music using a given set of keywords.',
  backstory="""You are a digital DJ with an encyclopedic knowledge of music.
  You are a master at using the YouTube Music search tool to find the perfect tracks
  that match a specific vibe or theme described by keywords.""",
  verbose=True,
  allow_delegation=False,
  llm=llm,
  # Equip this agent with the custom tool
  tools=[music_search_tool]
)

# 5. Define the Tasks
def create_crew_tasks(query, num_songs):
    extract_keywords_task = Task(
      description=f"Analyze the following user query and extract the best possible search keywords from it: '{query}'",
      expected_output="A comma-separated string of keywords. For example: sad, love, breakup, heartbreak",
      agent=keyword_extractor
    )

    search_songs_task = Task(
      description=f"Using the keywords provided, search YouTube Music for {num_songs} matching songs.",
      expected_output=f"A final JSON object containing a list of {num_songs} songs, each with a 'title' and a 'link'.",
      agent=music_searcher,
      # Pass the output of the first task to this one
      context=[extract_keywords_task]
    )
    return [extract_keywords_task, search_songs_task]


# 6. Create and Run the Crew
def main():
    # The natural language query from the user
    user_query = "Energetic songs for a workout"
    # You can now control the number of songs here
    number_of_songs = 2
    
    tasks = create_crew_tasks(user_query, number_of_songs)
    
    song_crew = Crew(
      agents=[keyword_extractor, music_searcher],
      tasks=tasks,
      process=Process.sequential,
      verbose=True
    )

    print(f"🚀 Crew is starting its work for the query: '{user_query}' and looking for {number_of_songs} songs.")
    result = song_crew.kickoff()

    print("\n\n########################")
    print("## Here is the final result:")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    main()