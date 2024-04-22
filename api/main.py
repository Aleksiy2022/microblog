from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/api/users/me")
async def get_tweets():
    print("***************************")
    print("Запрос пришел сюда")
    return {
        "result": "true",
        "user": {
            "id": 1,
            "name": "Ivan",
            "followers": [
                {
                    "id": 2,
                    "name": "Oleg"
                }
            ],
            "following": [
                {
                    "id": 3,
                    "name": "Kirill"
                }
            ]
        }
    }

