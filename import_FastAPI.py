from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pandas as pd
import random
import uvicorn
from typing import Dict

app = FastAPI()

# 기본 키워드 데이터 (엑셀 파일로 수정 가능)
data = {
    "누가": ["학생", "선생님", "개발자", "디자이너"],
    "언제": ["아침에", "점심에", "저녁에", "밤에"],
    "어디서": ["학교에서", "회사에서", "집에서", "카페에서"],
    "무엇을": ["공부한다", "일한다", "논다", "밥을 먹는다"],
    "어떻게": ["열심히", "느긋하게", "빠르게", "신중하게"],
    "왜": ["목표를 이루기 위해", "스트레스를 풀기 위해", "돈을 벌기 위해", "재미로"]
}

@app.get("/")
def read_root():
    return {"message": "DOYOON의 랜덤 문장 생성기 API입니다!"}

@app.get("/generate")
def generate_sentence():
    sentence = f"{random.choice(data['누가'])}는 {random.choice(data['언제'])} {random.choice(data['어디서'])} {random.choice(data['무엇을'])} {random.choice(data['어떻게'])} {random.choice(data['왜'])}."
    return {"sentence": sentence}

@app.post("/upload_excel/")
async def upload_excel(file: UploadFile = File(...)):
    global data

    # 엑셀 파일 읽기
    df = pd.read_excel(file.file)

    # 엑셀 파일이 올바른 형식인지 확인
    if not set(["누가", "언제", "어디서", "무엇을", "어떻게", "왜"]).issubset(df.columns):
        return {"error": "엑셀 파일의 형식이 잘못되었습니다. 올바른 형식: 누가, 언제, 어디서, 무엇을, 어떻게, 왜"}

    # NaN 값 제거 후 리스트로 변환하여 업데이트
    data["누가"] = df["누가"].dropna().tolist()
    data["언제"] = df["언제"].dropna().tolist()
    data["어디서"] = df["어디서"].dropna().tolist()
    data["무엇을"] = df["무엇을"].dropna().tolist()
    data["어떻게"] = df["어떻게"].dropna().tolist()
    data["왜"] = df["왜"].dropna().tolist()

    return {"message": "엑셀 데이터가 성공적으로 반영되었습니다!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


git init