import sys
import random
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QMessageBox,
    QRadioButton,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt

# Импорт вопросов из отдельного файла
from questions import questions  # questions.py должен содержать список questions

class HEXACOTest(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Тест HEXACO")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Случайный порядок вопросов
        self.questions = random.sample(questions, len(questions))

        # Словарь для хранения результатов
        self.results = {}

        # Создание элементов UI
        self.question_label = QLabel(self.questions[0]["text"])
        self.question_label.setAlignment(Qt.AlignCenter)

        self.options_layout = QVBoxLayout()
        self.options = []
        for i, option in enumerate(self.questions[0]["options"]):
            radio_button = QRadioButton(option)
            radio_button.clicked.connect(lambda checked, index=i: self.answer_clicked(index))
            self.options.append(radio_button)
            self.options_layout.addWidget(radio_button)

        self.next_button = QPushButton("Следующий вопрос")
        self.next_button.clicked.connect(self.next_question)

        # Добавление элементов в layout
        self.layout.addWidget(self.question_label, 0, 0, 1, 2)
        self.layout.addLayout(self.options_layout, 1, 0, 1, 2)
        self.layout.addWidget(self.next_button, 2, 0, 1, 2)

        self.current_question = 0

    def answer_clicked(self, index):
        # Сохранение выбранного ответа
        self.results[self.current_question] = index

    def next_question(self):
        # Проверка, был ли выбран ответ
        if self.current_question not in self.results:
            QMessageBox.warning(self, "Внимание!", "Выберите ответ на текущий вопрос.")
            return

        # Переход к следующему вопросу
        self.current_question += 1
        if self.current_question < len(self.questions):
            # Обновление текста вопроса
            self.question_label.setText(
                f"Вопрос {self.current_question + 1}: {self.questions[self.current_question]['text']}"
            )

            # Обновление радио-кнопок
            for i, button in enumerate(self.options):
                button.setText(
                    self.questions[self.current_question]["options"][i]
                )
                # Сбрасываем выбор
                button.setChecked(False)  # Сбрасываем выбор
                button.setEnabled(True)  # Включаем кнопку

        else:
            # Обработка результатов
            self.process_results()

    def process_results(self):
        # Обработка результатов теста
        scale_scores = {
            scale: 0
            for scale in [
                "Honesty-Humility",
                "Emotionality",
                "Extraversion",
                "Agreeableness",
                "Conscientiousness",
                "Openness to Experience",
            ]
        }

        for question_index, answer_index in self.results.items():
            question = self.questions[question_index]
            scale = question["scale"]
            reverse = question["reverse"]
            if reverse:
                answer_index = 6 - answer_index  # Переворачиваем значение

            scale_scores[scale] += answer_index

        # Вычисляем среднее значение для каждой шкалы
        for scale in scale_scores:
            scale_scores[scale] /= len(self.questions)  # Делим на количество вопросов в шкале

        # Выводим результаты в диалоговое окно
        results_text = "\n".join(
            f"{scale}: {score:.2f}" for scale, score in scale_scores.items()
        )
        QMessageBox.information(self, "Результаты теста HEXACO", results_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HEXACOTest()
    ex.show()
    sys.exit(app.exec_())