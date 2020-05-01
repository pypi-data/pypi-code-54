
import tweepy
from twitter_makeup import MakeUp
from secrets import consumer_key, consumer_secret, access_token, access_secret

# Configure Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# Make up your profile 🦄
makeup = MakeUp(api)

if False:
    banner_path = 'data/banner-night.jpg'
    banner_path = 'data/banner-morning.jpg'
    makeup.change_banner_picture(banner_path)
    print('Banner picture has been changed using "'+ banner_path + '" 🦄')

if False:
    profile_path = 'data/profile-xmas.jpg'
    profile_path = 'data/profile-regular.jpg'
    makeup.change_profile_picture(profile_path)
    print('Profile picture has been changed using "'+ profile_path + '" 🦄')

if False:
    profile_name = 'Nicolas Dupont 💻'
    profile_name = 'Nicolas Dupont ☕'
    profile_name = 'Nicolas Dupont 📝'
    makeup.change_profile_name(profile_name)
    print('Profile name has been changed by "' + profile_name + '" 🦄')

if False:
    profile_location = 'Boston'
    profile_location = 'Nantes'
    makeup.change_profile_location(profile_location)
    print('Profile location has been changed by "' + profile_location + '" 🦄')

if False:
    profile_description = "Co-founder and CPO at @akeneopim\
\n❤️ crafting products to create value for users and businesses\
\n💬 and 📝 about product, engineering, teamwork, learnings"
    makeup.change_profile_description(profile_description)
    print('Profile description has been changed by "' + profile_description + '" 🦄')

print('You have to uncomment tests in tests.py, be careful to not publish test data on your profile 🐴')
