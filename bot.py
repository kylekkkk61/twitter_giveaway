import tweepy
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('mysql+pymysql://root:kyle112358@localhost:3306/twitter_giveaway?charset=utf8')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

consumer_key = '自己的！'
consumer_secret = '自己的！'

key = '自己的！'
secret = '自己的！'

auth = tweepy.OAuthHandler(consumer_key,
                           consumer_secret)
auth.set_access_token(key,
                      secret)

api = tweepy.API(auth)


class TwitterBot(Base):
    __tablename__ = "twitter_giveaway"  # 數據庫中的表格名字

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
        public_tweets = api.home_timeline(count=100, tweet_mode='extended')
        

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
        keywords = 'Follow,Like,RT,Tag,Retweet,FOLLOW,LIKE,RETWEET,TAG,关注,转推,喜欢,關注,喜歡,轉推,點讚,三連'
        #上面可以新增其他抽獎關鍵字

        count = sum([1 if w in p and w else 0 for w in keywords.split(',')])
        if count > 2:
            print("-----------Found 白單抽獎-----------")
            print(tweet.full_text)

            user_mentions = tweet.entities['user_mentions']
            for friend in user_mentions:
                screen_name = friend['screen_name']
                screen_names = ["kylekkkk", screen_name]
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
            tweets = 'LFG! @wl02058381 @demi_yooo @yerrr42069 @ElliottLu0616 @MarkLU42725909 '
            #以上改成想要的回覆內容 tag記得換成自己朋友～

            url = str("https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str)
            print(url)
            try:
                re = api.retweet(tweet.id)
            except Exception as e:
                print(str(e))
                continue
            
            
            api.update_status(status = tweets, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)

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
