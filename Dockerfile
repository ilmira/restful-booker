FROM cr.yandex/mirror/library/python:3.11-slim
# зеркало Яндекс из-за плохого соединения из РФ
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
CMD ["pytest", "-v", "--alluredir=/app/allure-results"]
