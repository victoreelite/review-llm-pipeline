import csv
import json
import os
from datetime import datetime
from openai import OpenAI

INPUT_FILE = "data/reviews.csv"
OUTPUT_FILE = "results/review_result.json"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")


def read_reviews(file_name):
    reviews = []

    with open(file_name, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                "id": str(row.get("id", "")).strip(),
                "review": str(row.get("review", "")).strip()
            }

            if item["id"] and item["review"]:
                reviews.append(item)

    return reviews


def make_prompt(reviews):
    text = "Нужно разобрать отзывы покупателей.\n"
    text += "Для каждого отзыва определи тональность, основную тему и коротко объясни причину.\n"
    text += "Отзывы:\n"

    for item in reviews:
        text += f'{item["id"]}. {item["review"]}\n'

    return text


def get_schema():
    return {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "sentiment": {
                            "type": "string",
                            "enum": ["positive", "negative", "neutral"]
                        },
                        "topic": {
                            "type": "string",
                            "enum": ["service", "price", "quality", "delivery", "assortment", "other"]
                        },
                        "short_reason": {"type": "string"}
                    },
                    "required": ["id", "sentiment", "topic", "short_reason"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["items"],
        "additionalProperties": False
    }


def ask_model(reviews):
    client = OpenAI()
    prompt = make_prompt(reviews)

    completion = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Ты помогаешь разбирать отзывы покупателей. Отвечай только по данным из отзывов."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "reviews_analysis",
                "schema": get_schema(),
                "strict": True
            }
        }
    )

    answer = completion.choices[0].message.content
    return json.loads(answer)


def save_result(data, input_file, output_file):
    folder = os.path.dirname(output_file)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    final_data = {
        "source_file": input_file,
        "model": MODEL,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": data["items"]
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(final_data, file, ensure_ascii=False, indent=2)


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Не найден OPENAI_API_KEY. Сначала добавьте API-ключ в переменные среды.")
        return

    reviews = read_reviews(INPUT_FILE)

    if len(reviews) == 0:
        print("Входной файл пустой или не найдено поле review.")
        return

    result = ask_model(reviews)
    save_result(result, INPUT_FILE, OUTPUT_FILE)

    print("Готово")
    print("Обработано отзывов:", len(result["items"]))
    print("Файл результата:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
