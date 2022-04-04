

import tweepy
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

engine = create_engine('mysql+pymysql://root:kyle112358@localhost:3306/db?charset=utf8')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

consumer_key = 'Z3ZwF3ngbyP4uxlf5Ep18CdXx'
consumer_secret = 'vac20lxsDpmKTvyMxySK0gGPZ2Ic6okUpWINy1KjzcmLDcNBhB'

key = '709699099474276353-XtWs6Ca3EnUCpSi44e2pcFpnyVTKQtk'
secret = 'X3uBdvpMQtYe9u8t8ZyZD7Vq8KXakOo5WxYMp7nMFJcAj'

auth = tweepy.OAuthHandler(consumer_key,
                           consumer_secret)
auth.set_access_token(key,
                      secret)

api = tweepy.API(auth)


class TwitterBot(Base):
    __tablename__ = "twitter_giveaway"  # 数据库中保存的表名字

    id = Column(Integer, index=True, primary_key=True)
    tweet_id = Column(Integer, nullable=True)
    screen_name = Column(String(200), nullable=True)
    url = Column(String(300), nullable=True)
    updated_at = Column(DateTime, default=datetime.now)


while True:
    print("@@@@@@@@@@@@@@@@@@@@Start@@@@@@@@@@@@@@@@@@@@@@")
    print(datetime.utcnow())

    public_tweets = []

    try:
        public_tweets = api.home_timeline(count=50, tweet_mode='extended')
        # public_tweets = api.user_timeline(screen_name='reinkerte31', count=3, tweet_mode='extended')
        #public_tweets = api.list_timeline(list_id=1510735697371615232, count=100, tweet_mode='extended')

    except Exception as e:
        print(str(e))
        print("sleep 60s")
        time.sleep(60)
        continue

    for tweet in public_tweets:

        if session.query(TwitterBot).filter(TwitterBot.tweet_id == tweet.id).count() > 0:
            print(str(tweet.id) + "已存在。")
            continue

        print("id=" + str(tweet.id))
        print("created_at=" + str(tweet.created_at))

        p = tweet.full_text
        keywords = 'Follow,Like,RT,Tag,Retweet,FOLLOW,LIKE,RETWEET,TAG,关注,转推,喜欢'

        count = sum([1 if w in p and w else 0 for w in keywords.split(',')])
        if count > 1:
            print("---------------------Found 白名单推文")
            print(tweet.full_text)

            user_mentions = tweet.entities['user_mentions']
            for friend in user_mentions:
                screen_name = friend['screen_name']
                screen_names = ["zlexdl", screen_name]
                friendships = api.lookup_friendships(screen_name=screen_names)

                if len(friendships) > 1:

                    if not friendships[1].is_following:
                        print("Following <" + screen_name + "> ")
                        api.create_friendship(screen_name=screen_name)

                        print("Follow <" + screen_name + "> success!")
                    else:
                        print("Already following <" + screen_name + "> !")

            try:
                api.create_favorite(id=tweet.id_str)
            except Exception as e:
                print(str(e))
            tweets = [
                'It would be an honor to be a part of your project! You are frontrunners in the game, you have in me a loyal supporter who always gives. Keep it up, much love! @wl02058381 @demi_yooo @yerrr42069 @ElliottLu0616 @MarkLU42725909 ',
                '@wl02058381 @demi_yooo @yerrr42069 @ElliottLu0616 @MarkLU42725909   if my luck could ever carry me now would be the time',
                '@wl02058381 @demi_yooo @yerrr42069 @ElliottLu0616 @MarkLU42725909  Excited to be a part of it. Hopefully your first following will be WL and OGd for appreciation 🙏']

            message = random.choice(tweets)
            url = str("https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str)
            print(url)
            re = api.update_status(message, attachment_url=url)
            print("转推结果：" + str(re.is_quote_status))

            twitterBot = TwitterBot(
                screen_name=tweet.user.screen_name,
                url=url,
                tweet_id=tweet.id)
            print(tweet.id)
            session.add(twitterBot)
            session.commit()

            print("time.sleep(300) start time=" + str(datetime.utcnow()))
            time.sleep(300)

    print("time.sleep(300) start time=" + str(datetime.utcnow()))
    time.sleep(300)
    print("@@@@@@@@@@@@@@@@@@@@END@@@@@@@@@@@@@@@@@@@@@@")
