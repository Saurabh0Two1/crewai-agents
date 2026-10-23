import os
import openai
from crewai.flow.flow import Flow, start,listen

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MovieRecommendationFlow(Flow):
    @start()
    def generate_genre(self):
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Give me a random movie genre.",
                },
            ],
        )
        random_genre = response.choices[0].message.content.strip()
        self.state["genre"] = random_genre
        return random_genre

    @listen(generate_genre)
    def recommend_movie(self, random_genre):
    
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Recommend a movie in {random_genre} genre.",
                },
            ],
        )

        movie_recommendation = response.choices[0].message.content.strip()
        self.state["recommendation"] = movie_recommendation
        return movie_recommendation


""" USAGE
    from flows.agentic_flow import MovieRecommendationFlow
    flow = MovieRecommendationFlow()
    final_result =await flow.kickoff_async()
    pprint(flow.state)
    print(f"\nMovie Recommendation: {final_result}")
"""