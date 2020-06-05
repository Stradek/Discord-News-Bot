# Discord-News-Bot

# main.py

#!/usr/bin/env python3

import os
import random
import requests

from datetime import date
from datetime import datetime

from string import punctuation

from discord.ext import commands
from dotenv import load_dotenv


def remove_unsafe_characters(search_phrase):
    safe_search_phrase = search_phrase.translate(str.maketrans('', '', punctuation))
    
    return safe_search_phrase


class Article:
    def __init__(self):
        self.source = ''
        self.title= ''
        self.description= ''
        self.author = ''
        self.url = ''

    def set_source(self, source):
        try:
            self.source += source
        except Exception:
            self.source = 'Unknown'
    
    def set_title(self, title):
        try:
            self.title += title
        except Exception:
            self.title = 'Unknown'

    def set_description(self, description):
        try:
            self.description += description
        except Exception:
            self.description = 'Unknown'
 
    def set_author(self, author):
        try:
            self.author += author
        except Exception:
            self.author = 'Unknown'
   
    def set_url(self, url):
        try:
            self.url += url
        except Exception:
            self.url = 'Unknown'

    def get_source(self):
        return self.source

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_author(self):
        return self.author
   
    def get_url(self):
        return self.url
    
    def get_all(self):
        all_dict = {
            'source': self.source,
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'url': self.url,
        }

        return all_dict

def article_factory(article_data):
    article = Article()
    article.set_source(article_data['source']['name'])
    article.set_author(article_data['author'])
    article.set_title(article_data['title'])
    article.set_description(article_data['description'])
    article.set_url(article_data['url'])

    print(article.get_all())

    return article

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NEWS_KEY = os.getenv('NEWS_KEY')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    print('{0.user} has connected to Discord!'.format(bot))
    print('{0.name}(id: {0.id})'.format(guild))

    
@bot.command(name='news')
async def news(ctx):
    mention = ctx.message.author.mention
    #mention = ctx.message.author.display_name
    
    search = ctx.message.content.lstrip(bot.command_prefix + ctx.command.name).lstrip()

    search_phrase = remove_unsafe_characters(search)
    search_phrase = search_phrase.replace(' ', '+')

    print(f'{ctx.message.author} is searching for {search_phrase}')

    date_today = str(date.today())

    url = f"http://newsapi.org/v2/everything?q={search_phrase}&language=en&from={date_today}&sortBy=publishedAt&apiKey={NEWS_KEY}"
    print(url)

    response = requests.get(url)
    data = response.json()

    #print(data)
    try:
        article_data = data['articles'][0]


        article = article_factory(article_data)

        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f'{mention}'+ '\n' + \
            '**' + article.get_title() + '**' + '\n' + \
            '==========================' + '\n' + \
            article.get_description() + '\n' + \
            'Author(s): ' + article.get_author() + '\n' + \
            'Source: ' + article.get_source() + '\n' + \
            'More at: ' + article.get_url() + '\n' + \
            'Search time: ' + str(datetime_now) + '\n'
            #message = 'There are no articles with this title today'
    except LookupError:
        message = f'No news about "{search}" today'

    await ctx.send(message)
    

bot.run(TOKEN)
