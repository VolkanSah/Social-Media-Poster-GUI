import tweepy
import facebook
from instabot import Bot
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QFileDialog, QLineEdit, QCheckBox, QLabel, QTabWidget, QMessageBox
)
from PySide6.QtGui import QAction
import sys

class SocialMediaManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Media Manager Pro")
        self.setMinimumSize(800, 600)
        
        # Initialisiere UI-Komponenten
        self.init_ui()
        self.init_credentials()
        
    def init_ui(self):
        # Haupt-Tab-Widget
        tab_widget = QTabWidget()
        
        # Haupt-Post-Tab
        main_tab = QWidget()
        layout = QVBoxLayout()
        
        # Nachrichteneingabe
        self.message_entry = QTextEdit()
        self.message_entry.setPlaceholderText("Enter your message here...")
        layout.addWidget(QLabel("Message:"))
        layout.addWidget(self.message_entry)
        
        # Bildauswahl
        self.image_entry = QLineEdit()
        image_btn = QPushButton("Select Image")
        image_btn.clicked.connect(self.select_image)
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_entry)
        image_layout.addWidget(image_btn)
        layout.addLayout(image_layout)
        
        # Netzwerkauswahl
        self.network_checks = {
            'twitter': QCheckBox("Twitter"),
            'facebook': QCheckBox("Facebook"),
            'instagram': QCheckBox("Instagram")
        }
        network_group = QVBoxLayout()
        network_group.addWidget(QLabel("Select Networks:"))
        for check in self.network_checks.values():
            network_group.addWidget(check)
        layout.addLayout(network_group)
        
        # Post-Button
        post_btn = QPushButton("Post to Selected Networks")
        post_btn.clicked.connect(self.post_message)
        layout.addWidget(post_btn)
        
        main_tab.setLayout(layout)
        
        # Log-Tab
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        # Credential-Tab
        credential_tab = self.create_credential_tab()
        
        tab_widget.addTab(main_tab, "Post")
        tab_widget.addTab(credential_tab, "Credentials")
        tab_widget.addTab(self.log_text, "Logs")
        
        self.setCentralWidget(tab_widget)
        
    def create_credential_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Twitter Credentials
        twitter_group = QVBoxLayout()
        twitter_group.addWidget(QLabel("Twitter Credentials:"))
        self.twitter_api_key = QLineEdit()
        self.twitter_api_secret = QLineEdit()
        self.twitter_access_token = QLineEdit()
        self.twitter_token_secret = QLineEdit()
        twitter_group.addWidget(QLabel("API Key:"))
        twitter_group.addWidget(self.twitter_api_key)
        twitter_group.addWidget(QLabel("API Secret:"))
        twitter_group.addWidget(self.twitter_api_secret)
        twitter_group.addWidget(QLabel("Access Token:"))
        twitter_group.addWidget(self.twitter_access_token)
        twitter_group.addWidget(QLabel("Token Secret:"))
        twitter_group.addWidget(self.twitter_token_secret)
        
        # Facebook Credentials
        facebook_group = QVBoxLayout()
        facebook_group.addWidget(QLabel("Facebook Access Token:"))
        self.facebook_token = QLineEdit()
        facebook_group.addWidget(self.facebook_token)
        
        # Instagram Credentials
        instagram_group = QVBoxLayout()
        instagram_group.addWidget(QLabel("Instagram Credentials:"))
        self.instagram_user = QLineEdit()
        self.instagram_pass = QLineEdit()
        self.instagram_pass.setEchoMode(QLineEdit.Password)
        instagram_group.addWidget(QLabel("Username:"))
        instagram_group.addWidget(self.instagram_user)
        instagram_group.addWidget(QLabel("Password:"))
        instagram_group.addWidget(self.instagram_pass)
        
        layout.addLayout(twitter_group)
        layout.addLayout(facebook_group)
        layout.addLayout(instagram_group)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
        
    def init_credentials(self):
        # Hier könnten gespeicherte Credentials geladen werden
        pass
        
    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.image_entry.setText(file_path)
            
    def validate_inputs(self):
        message = self.message_entry.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Warning", "Message cannot be empty!")
            return False
            
        selected = any(check.isChecked() for check in self.network_checks.values())
        if not selected:
            QMessageBox.warning(self, "Warning", "Select at least one network!")
            return False
            
        return True
        
    def post_message(self):
        if not self.validate_inputs():
            return
            
        message = self.message_entry.toPlainText().strip()
        image_path = self.image_entry.text() or None
        
        if self.network_checks['twitter'].isChecked():
            self.post_to_twitter(message, image_path)
            
        if self.network_checks['facebook'].isChecked():
            self.post_to_facebook(message, image_path)
            
        if self.network_checks['instagram'].isChecked():
            self.post_to_instagram(message, image_path)
            
    def post_to_twitter(self, message, image_path):
        if len(message) > 280:
            self.log(f"Twitter Error: Message exceeds 280 characters ({len(message)})")
            return
            
        try:
            auth = tweepy.OAuthHandler(
                self.twitter_api_key.text(),
                self.twitter_api_secret.text()
            )
            auth.set_access_token(
                self.twitter_access_token.text(),
                self.twitter_token_secret.text()
            )
            api = tweepy.API(auth)
            
            if image_path:
                media = api.media_upload(image_path)
                api.update_status(status=message, media_ids=[media.media_id])
            else:
                api.update_status(status=message)
                
            self.log("Successfully posted to Twitter")
        except Exception as e:
            self.log(f"Twitter Error: {str(e)}")
            
    def post_to_facebook(self, message, image_path):
        try:
            graph = facebook.GraphAPI(self.facebook_token.text())
            if image_path:
                with open(image_path, "rb") as image:
                    graph.put_photo(image=image, message=message)
            else:
                graph.put_object("me", "feed", message=message)
            self.log("Successfully posted to Facebook")
        except Exception as e:
            self.log(f"Facebook Error: {str(e)}")
            
    def post_to_instagram(self, message, image_path):
        if not image_path:
            self.log("Instagram Error: Image required for posting")
            return
            
        try:
            bot = Bot()
            bot.login(
                username=self.instagram_user.text(),
                password=self.instagram_pass.text()
            )
            bot.upload_photo(image_path, caption=message)
            self.log("Successfully posted to Instagram")
        except Exception as e:
            self.log(f"Instagram Error: {str(e)}")
            
    def log(self, message):
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def closeEvent(self, event):
        # Hier könnten Credentials gespeichert werden
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialMediaManager()
    window.show()
    sys.exit(app.exec())
