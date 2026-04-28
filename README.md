Порядок запуска:

В одном терминале:
Бэкенд:
cd Путь до проекта
.\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
python -m uvicorn app.main:app --reload


В втором терминале:
Фронтенд:
cd Путь до проекта\rec-admin
npm install
npm run dev

Должен быть установлен node.js
