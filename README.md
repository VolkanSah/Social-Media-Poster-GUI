
# Social Media Post Tool v0.4

## Overview
Tired of manually posting to multiple social networks every time there's an important update? This tool is designed to simplify that process. With this lightweight application, you can post messages simultaneously to Twitter (X), Facebook, and Instagram directly from your desktop, without needing to load up each platform individually.

### Why This Tool?
Managing multiple social media accounts can be a hassle, especially during critical times like server outages or when urgent updates need to be communicated. This tool was born out of the need for a quick and efficient way to post to several platforms without cluttering your system with unnecessary software.

### Features
- **Multi-Network Posting**: Post to Twitter, Facebook, and Instagram all at once.
- **Image Upload**: Attach images to your posts effortlessly.
- **Character Count Validation**: Ensures your message fits within Twitter's 280-character limit.
- **Log Tab**: Keeps track of successful posts and any errors encountered.
- **Lightweight and Simple**: No unnecessary bloat—just the features you need.

### Installation
You need tweepy, requests
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/social-media-post-tool.git
   ```
2. Navigate to the project directory:
   ```
   cd social-media-post-tool
   ```
3. Run the application:
   ```
   python run.py
   ```

### Usage
1. Open the application.
2. Write your message in the text box.
3. Optionally, select an image to attach.
4. Choose the social networks you want to post to (Twitter, Facebook, Instagram).
5. Click "Send Message" to post your update.

### Configuration
Before using the tool, ensure you have configured your API keys and tokens:
- **Twitter**: Set up your `api_key`, `api_key_secret`, `access_token`, and `access_token_secret`.
- **Facebook**: Use your `page_access_token` and `page_id`.
- **Instagram**: Use your `instagram_user_id` and `instagram_access_token`.

These can be configured directly in the `run.py` file under the respective placeholders.

### Contributions
Feel free to fork this repository and contribute to its development! If you have suggestions for new features or improvements, please submit a pull request.

### Download
You can download the latest release directly from [here](https://github.com/yourusername/social-media-post-tool/releases).

---

This tool was created out of a personal need to streamline social media communications, and it’s now available for everyone who faces the same challenges. Enjoy a more efficient way to stay connected!
