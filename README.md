
# Recommendation System Admin Panel

Веб-интерфейс для генерации, редактирования и сохранения рекомендованных подборок контента.

---

## Требования

Перед запуском убедитесь, что установлены:

- **Python 3.10+**
- **Node.js** (вместе с npm)

---

## Запуск проекта

### Backend

Откройте **первый терминал** и выполните:

```bash
cd <ПУТЬ_ДО_ПРОЕКТА>
.\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
python -m uvicorn app.main:app --reload
````

После запуска backend будет доступен по адресам:

* **API:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Swagger:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Frontend

Откройте **второй терминал** и выполните:

```bash
cd <ПУТЬ_ДО_ПРОЕКТА>\rec-admin
npm install
npm run dev
```

После запуска frontend будет доступен по адресу:

* **UI:** [http://localhost:5173](http://localhost:5173)

---

## Важно

* Backend и Frontend запускаются **в разных терминалах**
* `npm install` требуется только при первом запуске или после обновления зависимостей



---

## Структура проекта

```text
bootcamp/
│
├── app/                # FastAPI backend
│   ├── api/
│   ├── services/
│   ├── storage/
│   └── main.py
│
├── rec-admin/          # React frontend
│
└── README.md
```

---

## Основной функционал

* Загрузка CSV-файлов с данными
* Генерация рекомендаций по алгоритму
* Drag & Drop сортировка подборок
* Сохранение финальных версий подборок
* Просмотр текущих активных топов

---

## Режим разработки

Backend:

```bash
python -m uvicorn app.main:app --reload
```

Frontend:

```bash
npm run dev
```

```
```
