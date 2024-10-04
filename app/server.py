import logging
from flask import Flask, request, jsonify
from model import ToxicityModel

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация модели
toxicity_model = ToxicityModel()


@app.before_request
def log_request_info():
    app.logger.info(f'Получен запрос: {request.method} {request.url}')
    app.logger.info(f'Данные запроса: {request.get_json()}')


@app.after_request
def log_response_info(response):
    app.logger.info(f'Ответ сервера: {response.status} {response.data}')
    return response


@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    if 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    message = data['message']

    # Используем метод предсказания токсичности
    toxicity_score = toxicity_model.predict_toxicity(message)

    # Определяем метку (токсично или нет)
    toxicity_label = 'toxic' if toxicity_score > 0.5 else 'non-toxic'

    return jsonify({'toxicity_label': toxicity_label, 'score': toxicity_score})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
