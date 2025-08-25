# app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from calc_gpa import compute_gpa_and_ratio   # ← 先ほどのPythonを利用
import tempfile, shutil, math

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.post("/api/calc")
async def calc(file: UploadFile = File(...)):
    # 受け取ったCSVを一時ファイルに保存して既存関数に渡す
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    gpa, ratio = compute_gpa_and_ratio(tmp_path)
    # NaN 対応しつつ丸め
    gpa_out   = None if (gpa is None or (isinstance(gpa, float) and math.isnan(gpa))) else round(float(gpa), 3)
    ratio_out = None if (ratio is None or (isinstance(ratio, float) and math.isnan(ratio))) else round(float(ratio), 4)

    return {"gpa": gpa_out, "ratio": ratio_out}
