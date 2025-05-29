import sys
import os
import re
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDateEdit, QPushButton, QDialog, QHBoxLayout,
    QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QDate
from datetime import date


def edit_numb(numb):
    return numb if numb <= 22 else edit_numb(numb - 22)


def calculate(input_data):
    day = input_data.day()
    month = input_data.month()
    year = input_data.year()

    day_str = f"{day:02d}"
    month_str = f"{month:02d}"
    year_str = str(year)

    full_date = f"{day_str}.{month_str}.{year_str}"
    pure = full_date.replace('.', '').replace('0', '')
    destiny = str(sum([int(i) for i in pure]))
    while len(destiny) > 1:
        destiny = str(sum([int(i) for i in destiny]))

    birth_date = date(year, month, day)
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    arkan = sum([int(i) for i in pure])
    arkan = edit_numb(arkan)

    a = day
    b = month
    c = sum([int(i) for i in year_str])
    if a > 22: a = edit_numb(a)
    if c > 22: c = edit_numb(c)
    d = a + b + c
    d = edit_numb(d)

    ch_d1 = edit_numb(abs(a + b))
    ch_d2 = edit_numb(abs(a + c))
    ch_d3 = edit_numb(abs(ch_d1 + ch_d2))
    ch_d4 = edit_numb(abs(b + c))

    karmic1 = edit_numb(abs(a - b))
    karmic2 = edit_numb(abs(a - c))
    karmic3 = edit_numb(abs(karmic1 - karmic2))
    karmic4 = edit_numb(abs(b - c))
    karmic5 = edit_numb(abs(karmic1 + karmic2 + karmic3 + karmic4))

    period1 = 36 - int(destiny)
    period2 = period1 + 9
    period3 = period2 + 9

    def reduce(num):
        while len(num) > 1:
            num = str(sum([int(i) for i in num]))
        return num

    day_r = reduce(str(day))
    month_r = reduce(str(month))
    year_r = reduce(year_str)
    concat = reduce(day_r + month_r + year_r)
    money_code = day_r + month_r + year_r + concat
    num_1 = reduce(str(int(month_r) + int(year_r)))
    num_5 = reduce(str(int(year_r) + int(concat)))
    num_2 = reduce(str(int(num_1) + int(year_r)))
    num_4 = reduce(str(int(year_r) + int(num_5)))
    num_6 = reduce(str(int(num_1) + int(num_5)))
    fin_code = num_1 + num_2 + year_r + num_4 + num_5 + num_6

    table = [
        [f"Супер сила ({a})", f"ЧД 1 ({ch_d1})", f"КУ 1 ({karmic1})", f"0 - {period1}"],
        [f"Задача на жизнь ({b})", f"ЧД 2 ({ch_d2})", f"КУ 2 ({karmic2})", f"{period1} - {period2}"],
        [f"Энергия года ({c})", f"ЧД 3 ({ch_d3})", f"КУ 3 ({karmic3})", f"{period2} - {period3}"],
        [f"Предназначение ({d})", f"ЧД 4 ({ch_d4})", f"КУ 4 ({karmic4})", f"{period3} - ∞"],
        [f"Денежный код: {money_code}", f"Число судьбы {destiny}", f"КУ 5 ({karmic5})", f"Возраст: {age}"],
        [f"Денежный канал: {fin_code}", f"Ведическое число: {day_r}", f"Аркан: ({arkan})", f"Дата рождения: {full_date}"]
    ]
    return full_date, table


class PdfViewerDialog(QDialog):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle("А ну ка посмотрим что тут интересного")
        self.resize(1200, 800)

        self.layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)

        btn_layout = QHBoxLayout()

        # Кнопки масштабирования
        self.zoom_out_btn = QPushButton("-")
        self.zoom_out_btn.setFixedWidth(40)
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedWidth(40)

        self.prev_btn = QPushButton("← Назад")
        self.next_btn = QPushButton("Вперёд →")
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignCenter)

        btn_layout.addWidget(self.zoom_out_btn)
        btn_layout.addWidget(self.zoom_in_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.page_label)
        btn_layout.addWidget(self.next_btn)

        self.layout.addLayout(btn_layout)

        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        try:
            self.doc = fitz.open(pdf_path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть PDF файл.\n{e}")
            self.close()
            return

        self.current_page = 0
        self.num_pages = self.doc.page_count
        self.zoom = 0.6  # начальный масштаб

        self.show_page()

    def show_page(self):
        page = self.doc.load_page(self.current_page)
        mat = fitz.Matrix(self.zoom, self.zoom)
        pix = page.get_pixmap(matrix=mat)

        img_format = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, img_format)
        pixmap = QPixmap.fromImage(img)

        self.image_label.setPixmap(pixmap)
        self.page_label.setText(f"Страница {self.current_page + 1} из {self.num_pages}")

        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < self.num_pages - 1)

    def next_page(self):
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def zoom_in(self):
        self.zoom = min(self.zoom + 0.2, 3.0)  # максимум зума 3.0
        self.show_page()

    def zoom_out(self):
        self.zoom = max(self.zoom - 0.2, 0.2)  # минимум зума 0.2
        self.show_page()



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт Кармической матрицы по дате рождения")
        self.resize(1200, 500)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Выберите дату рождения:")
        self.label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.label)

        self.date_picker = QDateEdit(calendarPopup=True)
        self.date_picker.setDisplayFormat("dd.MM.yyyy")
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setFont(QFont("Arial", 12))
        self.date_picker.setFixedWidth(self.width() // 6)
        self.layout.addWidget(self.date_picker)

        self.button = QPushButton("Рассчитать")
        self.button.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.button)

        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget::item {
                border: 2px solid blue;
                padding: 4px;
            }
            QTableWidget::item:selected {
                color: black;
            }
            QHeaderView::section {
                font-weight: bold;
                background-color: #e0eaff;
                border: 1px solid #999;
            }
        """)
        self.table.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.table)

        self.button.clicked.connect(self.calculate)
        self.table.cellClicked.connect(self.cell_clicked)

    def calculate(self):
        selected_date = self.date_picker.date()
        try:
            full_date, data = calculate(selected_date)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Что-то пошло не так\n{str(e)}")
            return

        headers = ["Путь", "Число Достижений", "Кармический Узел", "Период"]
        self.table.setColumnCount(4)
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        for i, row in enumerate(data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.calculate()

    def cell_clicked(self, row, column):
        item = self.table.item(row, column)
        if not item:
            return
        text = item.text()

        # Не открывать файлы для этих ключевых значений
        if any(s in text for s in ["Возраст", "Дата рождения", "Денежный код, Число судьбы"]):
            return

        match = re.search(r"\(([\d]+)\)", text)
        if match:
            number = match.group(1)
            file_path = os.path.join("arkana", f"{number}.pdf")
            if os.path.exists(file_path):
                viewer = PdfViewerDialog(file_path)
                viewer.exec_()
            else:
                QMessageBox.warning(self, "Ошибка", f"Файл {number}.pdf не найден.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
