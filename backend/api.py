from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chroma_db_adapter import ChromaDB
from model import Website

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


vs = ChromaDB(top_k=5)


class PageData(BaseModel):
    url: str
    title: str
    html: str


class SearchQuery(BaseModel):
    query: str


class DeleteByDateRequest(BaseModel):
    date: str  # YYYY-MM-DD


@app.post("/index-page")
async def index_page(data: PageData):
    print("Hello from /index-page")
    try:
        website = Website(
            url=data.url,
            title=data.title,
            html=data.html,
            access_time=datetime.now(),
        )
        vs.insert_website_to_vs(website)

        return {
            "status": "success",
            "url": data.url,
            "message": "Page indexed.",
        }

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search(query: SearchQuery):
    try:
        results = vs.semantic_search(query.query)
        return {
            "query": query.query,
            "results": [r.model_dump() for r in results],
        }

    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/history")
async def delete_all_history():
    try:
        count = vs.delete_all()
        return {"status": "success", "deleted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/history/{date}")
async def delete_history_by_date(date: str):
    try:
        count = vs.delete_by_date(date)
        return {"status": "success", "date": date, "deleted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
