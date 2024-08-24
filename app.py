import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget,
    QAction, QMenu, QDialog, QListWidget, QFormLayout, QLabel, QComboBox, QCheckBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPalette, QColor

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicialización de variables
        self.history = []
        self.favorites = []

        # Configuración del modo oscuro
        self.set_dark_mode()

        # Configuración de la interfaz de usuario
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        
        # Añadir la primera pestaña con la página de inicio personalizada
        self.add_new_tab(QUrl("https://privsearch.pages.dev/"), "PrivSearch")

        # Barra de URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Ingrese URL")

        # Configuración del menú
        self.setup_menu()

        # Layout de la ventana principal
        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.showMaximized()

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        palette.setColor(QPalette.WindowText, QColor("#E0E0E0"))
        palette.setColor(QPalette.Base, QColor("#1E1E1E"))
        palette.setColor(QPalette.AlternateBase, QColor("#2E2E2E"))
        palette.setColor(QPalette.ToolTipBase, QColor("#E0E0E0"))
        palette.setColor(QPalette.ToolTipText, QColor("#E0E0E0"))
        palette.setColor(QPalette.Text, QColor("#E0E0E0"))
        palette.setColor(QPalette.Button, QColor("#2E2E2E"))
        palette.setColor(QPalette.ButtonText, QColor("#E0E0E0"))
        palette.setColor(QPalette.BrightText, QColor("#FF0000"))
        palette.setColor(QPalette.Link, QColor("#1E90FF"))
        self.setPalette(palette)

        self.setStyleSheet("""
            QLineEdit {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #333;
            }
            QPushButton {
                background-color: #333;
                color: #E0E0E0;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QTabWidget::pane {
                border: 1px solid #555;
            }
            QTabBar::tab {
                background: #333;
                color: #E0E0E0;
                border: 1px solid #555;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background: #1E1E1E;
            }
        """)

    def setup_menu(self):
        self.incognito_action = QAction("Nueva ventana incógnito", self)
        self.incognito_action.triggered.connect(self.open_incognito_window)
        
        self.add_favorites_action = QAction("Añadir a favoritos", self)
        self.add_favorites_action.triggered.connect(self.add_to_favorites)

        self.show_favorites_action = QAction("Mostrar Favoritos", self)
        self.show_favorites_action.triggered.connect(self.show_favorites_dialog)

        self.show_extensions_action = QAction("Mostrar Extensiones", self)
        self.show_extensions_action.triggered.connect(self.show_extensions_dialog)

        self.settings_action = QAction("Configuración", self)
        self.settings_action.triggered.connect(self.show_settings_dialog)

        self.refresh_action = QAction("Refrescar", self)
        self.refresh_action.triggered.connect(self.refresh_page)

        self.stop_action = QAction("Detener", self)
        self.stop_action.triggered.connect(self.stop_page_load)

        file_menu = self.menuBar().addMenu("Archivo")
        file_menu.addAction(self.incognito_action)
        file_menu.addAction(self.add_favorites_action)
        file_menu.addAction(self.show_favorites_action)
        file_menu.addAction(self.show_extensions_action)
        file_menu.addAction(self.settings_action)
        file_menu.addAction(self.refresh_action)
        file_menu.addAction(self.stop_action)

    def add_new_tab(self, qurl=None, label="Nueva Pestaña"):
        browser = QWebEngineView()
        self.configure_browser_settings(browser)
        if qurl:
            browser.setUrl(qurl)
        else:
            browser.setUrl(QUrl("https://privsearch.pages.dev/"))
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(self.update_url_bar)
        browser.loadFinished.connect(self.add_to_history)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        q = QUrl(url)
        self.tabs.currentWidget().setUrl(q)

    def update_url_bar(self):
        qurl = self.tabs.currentWidget().url()
        self.url_bar.setText(qurl.toString())

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def add_to_history(self):
        current_url = self.tabs.currentWidget().url().toString()
        if current_url not in self.history:
            self.history.append(current_url)

    def add_to_favorites(self):
        current_url = self.tabs.currentWidget().url().toString()
        if current_url not in self.favorites:
            self.favorites.append(current_url)

    def show_favorites_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Favoritos")
        layout = QVBoxLayout()
        
        list_widget = QListWidget()
        list_widget.addItems(self.favorites)
        list_widget.itemDoubleClicked.connect(self.open_favorite)

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec_()

    def open_favorite(self, item):
        url = QUrl(item.text())
        self.add_new_tab(url, "Favorito")

    def show_extensions_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Extensiones")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Panel de Extensiones - Aquí podrías agregar funcionalidades"))

        dialog.setLayout(layout)
        dialog.exec_()

    def show_settings_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuración")
        layout = QFormLayout()
        
        self.search_engine_combo = QComboBox()
        self.search_engine_combo.addItems(["DuckDuckGo", "Google", "Bing"])
        layout.addRow(QLabel("Motor de búsqueda predeterminado:"), self.search_engine_combo)
        
        self.enable_js_checkbox = QCheckBox("Habilitar JavaScript")
        self.enable_js_checkbox.setChecked(True)
        layout.addRow(self.enable_js_checkbox)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def save_settings(self):
        # Aquí puedes guardar las configuraciones, por ahora solo se imprime en consola
        print("Motor de búsqueda:", self.search_engine_combo.currentText())
        print("JavaScript habilitado:", self.enable_js_checkbox.isChecked())

    def refresh_page(self):
        self.tabs.currentWidget().reload()

    def stop_page_load(self):
        self.tabs.currentWidget().stop()

    def open_incognito_window(self):
        incognito_browser = QWebEngineView()
        incognito_profile = QWebEngineProfile("IncognitoProfile", incognito_browser.page())
        incognito_profile.setHttpUserAgent("MyCustomBrowser/1.0")
        incognito_profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        incognito_browser.page().setProfile(incognito_profile)
        incognito_browser.setUrl(QUrl("https://privsearch.pages.dev/"))
        incognito_browser.show()

    def configure_browser_settings(self, browser):
        profile = QWebEngineProfile.defaultProfile()
        settings = browser.settings()
        
        # Modificar el User-Agent
        profile.setHttpUserAgent("MyCustomBrowser/1.0")

        # Configurar otras opciones de privacidad
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
