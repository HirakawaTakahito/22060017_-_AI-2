from fastapi import FastAPI
from pydantic import BaseModel
import json
from typing import List
from pathlib import Path

app = FastAPI()

DATA_FILE = Path(__file__).parent / "data.json"
HISTORY_FILE = Path(__file__).parent / "history.json"

# 初期ファイル作成
for file in [DATA_FILE, HISTORY_FILE]:
    if not file.exists():
        file.write_text(json.dumps([] if "data" in file.name else {"usernames": [], "exercises": []}, ensure_ascii=False, indent=2))

# モデル
class Set(BaseModel):
    weight: float
    reps: int

class Record(BaseModel):
    username: str
    date: str
    exercise: str
    sets: List[Set]

# 記録追加
@app.post("/add_record")
def add_record(record: Record):
    try:
        # JSON読み込み
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

        # 総負荷量計算
        total_load = sum(s.weight * s.reps for s in record.sets)

        # データ追加
        data.append({
            "username": record.username,
            "date": record.date,
            "exercise": record.exercise,
            "sets": [s.dict() for s in record.sets],
            "total_load": total_load
        })

        # 履歴更新
        if record.username not in history["usernames"]:
            history["usernames"].append(record.username)
        if record.exercise not in history["exercises"]:
            history["exercises"].append(record.exercise)

        # 保存
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        return {"message": "保存完了", "total_load": total_load}
    except Exception as e:
        return {"error": str(e)}

# 全記録取得
@app.get("/get_records")
def get_records():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# 履歴取得
@app.get("/get_history")
def get_history():
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
    return history
