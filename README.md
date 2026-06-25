# API-пайплайн для анализа отзывов

Небольшой скрипт на Python, который читает отзывы из CSV-файла, отправляет их в LLM через API и сохраняет структурированный результат в JSON.

## Что делает скрипт

Скрипт берет файл `data/reviews.csv`, где есть id отзыва и текст отзыва. Потом отправляет эти отзывы в модель через OpenAI API. Модель для каждого отзыва определяет:

- тональность: `positive`, `negative` или `neutral`;
- основную тему: `service`, `price`, `quality`, `delivery`, `assortment` или `other`;
- короткую причину классификации.

Результат сохраняется в файл `results/review_result.json`.

## Структура проекта

```text
review_llm_pipeline/
├── data/
│   └── reviews.csv
├── results/
│   └── review_result.json
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Как запустить

Нужен Python 3.10 или новее.

Сначала установить зависимости:

```bash
pip install -r requirements.txt
```

Потом добавить API-ключ в переменные среды.

Для Windows PowerShell:

```powershell
setx OPENAI_API_KEY "ваш_ключ"
```

После этого надо закрыть и открыть терминал заново.

Для macOS или Linux:

```bash
export OPENAI_API_KEY="ваш_ключ"
```

Запуск:

```bash
python main.py
```

После запуска появится файл:

```text
results/review_result.json
```

## Пример

В качестве входных данных используется небольшой CSV-файл с отзывами пользователей.
Скрипт читает файл data/reviews.csv, отправляет текст каждого отзыва в LLM через API и сохраняет структурированный результат в results/review_result.json. Скрипт молодец!!

