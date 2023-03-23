import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox


class CurrencyConverter(QWidget):

    def __init__(self):
        super().__init__()

        # Get supported currencies from API
        self.currencies = []
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        for currency_code in data['rates'].keys():
            self.currencies.append(currency_code + ' - ' + currency_code)

        # Initialize GUI elements
        self.initUI()

    def initUI(self):
        # Labels
        self.label1 = QLabel('From:')
        self.label2 = QLabel('To:')
        self.label3 = QLabel('Amount:')
        self.label4 = QLabel('Result:')

        # Dropdown menus
        self.from_currency = QComboBox()
        self.to_currency = QComboBox()
        self.from_currency.addItems(self.currencies)
        self.to_currency.addItems(self.currencies)

        # Text fields
        self.amount = QLineEdit()
        self.result = QLineEdit()
        self.result.setReadOnly(True)

        # Convert button
        self.convert_btn = QPushButton('Convert')
        self.convert_btn.clicked.connect(self.convert)

        # Layouts
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label1)
        vbox1.addWidget(self.from_currency)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label2)
        vbox2.addWidget(self.to_currency)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.label3)
        vbox3.addWidget(self.amount)

        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.label4)
        vbox4.addWidget(self.result)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)
        hbox.addLayout(vbox4)

        hbox.addWidget(self.convert_btn)

        self.setLayout(hbox)

        # Window settings
        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle('Currency Converter')
        self.show()

    def convert(self):
        try:
            # Get currency codes
            from_cur = self.from_currency.currentText().split(' - ')[0]
            to_cur = self.to_currency.currentText().split(' - ')[0]

            # Make API request to get exchange rate
            url = f'https://api.exchangerate-api.com/v4/latest/{from_cur}'
            response = requests.get(url)
            data = response.json()
            rate = data['rates'][to_cur]

            # Convert the amount
            amount = float(self.amount.text())
            converted_amount = amount * rate

            # Update the result field
            self.result.setText(str(round(converted_amount, 2)))
        except:
            QMessageBox.warning(self, 'Error', 'Invalid input or unable to convert.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = CurrencyConverter()
    sys.exit(app.exec_())
