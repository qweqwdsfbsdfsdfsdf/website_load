# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import sys
import website_load


def fill_params():
    website_load.user_agents = website_load.read_useragents()
    website_load.cur_header = website_load.set_header()
    if not window.checkBox_readurl_from_file.isChecked():
        website_load.url.clear()
        website_load.url.append(window.target_lineEdit.text())
    else:
        website_load.url = website_load.read_urls()
    if not window.checkBox_read_proxies.isChecked():
        website_load.proxies.clear()
    else:
        website_load.proxies = website_load.read_proxies()
    website_load.referrer = window.referrer.text()
    website_load.thread_limit = window.spinBox_Threads.value()
    website_load.request_methods.clear()
    website_load.request_methods.append("GET") if window.checkBox_Get.isChecked() else None
    website_load.request_methods.append("HEAD") if window.checkBox_Head.isChecked() else None
    website_load.request_methods.append("POST") if window.checkBox_Post.isChecked() else None
    website_load.min_timeout = int(window.timeout_min.text())
    website_load.max_timeout = int(window.timeout_max.text())
    website_load.wait_for_response = window.wait_for_response.isChecked()
    website_load.append_rand_string_to_url = window.append_random_chars.isChecked()


def clickstart_handler():
    fill_params()
    window.setWindowTitle('working')
    website_load.start_flood()


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
