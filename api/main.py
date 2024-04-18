from fastapi import FastAPI

app = FastAPI()


@app.post("/api/tweets")
async def get_tweets(api_key: str):
    return {
        "result": "true",
        "tweet_id": 1
    }
