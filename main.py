import twitter_bot as tb
import mongo_db as mongo


def get_highlights(email, username, password):
    try:
        bot = tb.Twitterbot(email, username, password)
        # logging in
        bot.login()

        if bot.is_logged_in():
            # Login successful Now go to home page
            bot.bot.get('https://x.com/home')
            # Click on show more btn
            bot.click_on_show_more_btn()
            # Get top trending
            trend_li = bot.get_top_trend_items()
            # print(trend_li)
            mongo_client = mongo.MongoClient()
            ip_address = bot.get_bot_ip()
            inserted_data = mongo_client.insert_data(trend_li, ip_address)
            bot.close_bot()
            return {"code": 1, "data": inserted_data, "message": "Fetched list of trending topics."}
        else:
            print("Failed to login")
            bot.close_bot()
            return {"code": 0, "message": "Failed to login to Twitter(X) due to security code verification."}
    except Exception as e:
        return {"code": -1, "message": f"Failed to get highlights due to: {str(e)}"}
