from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, description="متنی که باید خلاصه شود")

class AskRequest(BaseModel):
    context_text: str = Field(..., min_length=20, description="متن مرجع")
    question: str = Field(..., min_length=5, description="سوال کاربر")

class SentimentRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=5,
        description="متن برای تحلیل احساس"
    )


app = FastAPI(
    title="Text Summarizer & QA API",
    description="سرویس خلاصه‌سازی و پاسخ به سوال بر اساس متن",
    version="1.1.0"
)

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

embedding_model =SentenceTransformer(

    "all-MiniLM-L6-v2"
)

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
)

# -------------------- اندپوینت‌ها (بخش ۴) --------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=[
                {
                    "role": "system",
                    "content": "تو یک خلاصه‌کننده حرفه‌ای هستی. متن را به صورت چند خطی، تمیز، روان و بدون اضافه کردن اطلاعات خارجی خلاصه کن"
                },
                {
                    "role":"user",
                    "content":request.text
                }
            ],
            temperature=0.3
        )
        summary = response.choices[0].message.content.strip()
        return {
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Embedding search
def find_relevant_text(
        context,
        question
):

    sentences = context.split(".")


    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 0
    ]


    context_vectors = embedding_model.encode(
        sentences
    )


    question_vector = embedding_model.encode(
        [question]
    )


    scores = cosine_similarity(
        question_vector,
        context_vectors
    )[0]


    best_indexes = scores.argsort()[-3:]


    result = [
        sentences[i]
        for i in best_indexes
    ]


    return ".".join(result)


@app.post("/ask")
async def ask(request: AskRequest):
    try:
        system_prompt = """
        تو یک دستیار پاسخگو هستی که فقط و فقط بر اساس متنی که به عنوان context به تو داده می‌شود پاسخ می‌دهی.
        اگر جواب سوال داخل متن نباشد، صادقانه بگو: «بر اساس متن داده‌شده نمی‌توانم پاسخ دهم.»
        هیچ اطلاعاتی از دانش خودت اضافه نکن.
        """

        user_prompt = f"""
        متن مرجع:
        {request.context_text}

        سوال:
        {request.question}
        """

        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sentiment")
async def sentiment(
        request: SentimentRequest
):

    try:

        result = sentiment_model(
            request.text
        )[0]


        return {

            "sentiment":
            result["label"],


            "score":
            result["score"]

        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )