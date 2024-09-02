import tweepy

def post_to_twitter(api_key, api_key_secret, access_token, access_token_secret, message, image_path=None):
    try:
        # Authenticate
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Post tweet
        if image_path:
            media = api.media_upload(image_path)
            tweet = api.update_status(status=message, media_ids=[media.media_id])
        else:
            tweet = api.update_status(status=message)

        log_text.insert(tk.END, f"Posted to Twitter: {tweet.id}\n")
        return True
    except Exception as e:
        log_text.insert(tk.END, f"Error posting to Twitter: {str(e)}\n")
        return False
