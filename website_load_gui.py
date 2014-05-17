# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from website_load import *


def fill_params():
    interface.read_useragents()
    if not window.checkBox_readurl_from_file.isChecked():
        interface.url.clear()
        interface.url.append(window.target_lineEdit.text())
    else:
        interface.read_urls()
    if not window.checkBox_read_proxies.isChecked():
        interface.proxies.clear()
    else:
        interface.read_proxies()
    interface.referrer = window.referrer.text()
    interface.thread_limit = window.spinBox_Threads.value()
    interface.request_methods.clear()
    interface.request_methods.append("GET") if window.checkBox_Get.isChecked() else None
    interface.request_methods.append("HEAD") if window.checkBox_Head.isChecked() else None
    interface.request_methods.append("POST") if window.checkBox_Post.isChecked() else None
    interface.min_timeout = int(window.timeout_min.text())
    interface.max_timeout = int(window.timeout_max.text())
    interface.wait_for_response = window.wait_for_response.isChecked()
    interface.append_rand_string_to_url = window.append_random_chars.isChecked()


def clickstart_handler():
    fill_params()
    window.setWindowTitle('working')
    interface.start_flood()


def read_url_from_file_handler():
    window.target_lineEdit.setDisabled(
        True) if window.checkBox_readurl_from_file.isChecked() else window.target_lineEdit.setDisabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = uic.loadUi('MainWindow.ui')
    window.startButton.clicked.connect(clickstart_handler)
    window.checkBox_readurl_from_file.stateChanged.connect(read_url_from_file_handler)
    window.target_lineEdit.returnPressed.connect(clickstart_handler)
    window.show()
    sys.exit(app.exec_())
