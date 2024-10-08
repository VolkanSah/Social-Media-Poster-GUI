import tweepy
import facebook
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QFileDialog, QLineEdit, QCheckBox, QLabel, QTabWidget
)
from PySide6.QtGui import QAction, QIcon
import sys

# Funktionen für Social Media Posts
def post_to_twitter(api_key, api_key_secret, access_token, access_token_secret, message, image_path=None):
    try:
        # Authentifizierung mit Twitter API
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        if image_path:
            # Post mit Bild
            media = api.media_upload(image_path)
            api.update_status(status=message, media_ids=[media.media_id])
        else:
            # Post ohne Bild
            api.update_status(status=message)
        return "Erfolgreich auf Twitter gepostet"
    except Exception as e:
        return f"Fehler beim Posten auf Twitter: {str(e)}"

def post_to_facebook(access_token, page_id, message, image_path=None):
    try:
        graph = facebook.GraphAPI(access_token)
        if image_path:
            with open(image_path, "rb") as image:
                # Post mit Bild auf der Seite
                graph.put_photo(image=image, album_path=f"{page_id}/photos", message=message)
        else:
            # Post ohne Bild auf der Seite
            graph.put_object(parent_object=f"{page_id}", connection_name="feed", message=message)
        return "Erfolgreich auf der Facebook-Seite gepostet"
    except facebook.GraphAPIError as e:
        return f"Fehler beim Posten auf der Facebook-Seite: {str(e)}"

def post_to_instagram(username, password, message, image_path):
    from instabot import Bot
    bot = Bot()
    try:
        bot.login(username=username, password=password)
        if image_path:
            # Instagram erfordert ein Bild für Posts
            bot.upload_photo(image_path, caption=message)
            return "Erfolgreich auf Instagram gepostet"
        else:
            return "Fehler: Instagram erfordert ein Bild für Posts"
    except Exception as e:
        return f"Fehler beim Posten auf Instagram: {str(e)}"

# GUI-Design mit PySide6
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Network Poster")

        # Menüleiste
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        about_action = QAction("About", self)
        about_action.triggered.connect(show_about)
        file_menu.addAction(about_action)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Hauptlayout
        main_layout = QHBoxLayout()

        # Linkes Widget für Netzwerkeinstellungen
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        left_layout.addWidget(QLabel("Netzwerke:"))

        self.twitter_var = QCheckBox("Twitter")
        self.facebook_var = QCheckBox("Facebook")
        self.instagram_var = QCheckBox("Instagram")  # Placeholder for future Instagram integration
        left_layout.addWidget(self.twitter_var)
        left_layout.addWidget(self.facebook_var)
        left_layout.addWidget(self.instagram_var)

        # Neues Eingabefeld für Seiten-ID
        self.page_id_entry = QLineEdit()
        self.page_id_entry.setPlaceholderText("Seiten-ID (für Facebook)")
        left_layout.addWidget(self.page_id_entry)

        main_layout.addWidget(left_widget)

        # Rechtes Widget für Nachrichteneingabe und Bildauswahl
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        self.message_entry = QTextEdit()
        self.message_entry.setPlaceholderText("Enter your message here...")
        right_layout.addWidget(self.message_entry)

        self.image_entry = QLineEdit()
        image_button = QPushButton("Browse")
        image_button.clicked.connect(self.select_image)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_entry)
        image_layout.addWidget(image_button)

        right_layout.addLayout(image_layout)

        send_button = QPushButton("Send Message")
        send_button.clicked.connect(self.send_message)
        right_layout.addWidget(send_button)

        main_layout.addWidget(right_widget)

        # Hauptwidget setzen
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Log-Tab
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        tab_widget = QTabWidget()
        tab_widget.addTab(main_widget, "Main")
        tab_widget.addTab(self.log_text, "Logs")
        self.setCentralWidget(tab_widget)

    def send_message(self):
        message = self.message_entry.toPlainText().strip()
        image_path = self.image_entry.text()

        if not message:
            self.log_text.append("Fehler: Nachricht ist leer.")
            return

        if len(message) > 280:
            self.log_text.append("Fehler: Nachricht zu lang für Twitter (max 280 Zeichen)")
            return

        if self.twitter_var.isChecked():
            if not twitter_api_key or not twitter_api_key_secret or not twitter_access_token or not twitter_access_token_secret:
                self.log_text.append("Fehler: Twitter-API-Schlüssel fehlen.")
            else:
                result = post_to_twitter(twitter_api_key, twitter_api_key_secret, twitter_access_token, twitter_access_token_secret, message, image_path)
                self.log_text.append(result)

        if self.facebook_var.isChecked():
            page_id = self.page_id_entry.text().strip()
            if not facebook_access_token:
                self.log_text.append("Fehler: Facebook-Zugangstoken fehlt.")
            elif not page_id:
                self.log_text.append("Fehler: Seiten-ID für Facebook fehlt.")
            else:
                result = post_to_facebook(facebook_access_token, page_id, message, image_path)
                self.log_text.append(result)

        if self.instagram_var.isChecked():
            if not instagram_username or not instagram_password:
                self.log_text.append("Fehler: Instagram-Zugangsdaten fehlen.")
            else:
                result = post_to_instagram(instagram_username, instagram_password, message, image_path)
                self.log_text.append(result)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.image_entry.setText(file_path)

def show_about():
    # Display an about message
    pass

# Dummy API keys for testing - replace with your actual keys
twitter_api_key = "your_api_key"
twitter_api_key_secret = "your_api_key_secret"
twitter_access_token = "your_access_token"
twitter_access_token_secret = "your_access_token_secret"
facebook_access_token = "your_facebook_page_access_token"  # Hier muss der Page Access Token angegeben werden
instagram_username = "your_instagram_username"
instagram_password = "your_instagram_password"

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
