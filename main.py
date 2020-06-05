# Discord-News-Bot

# main.py

#!/usr/bin/env python3

import os
import random
import requests

from datetime import date

from discord.ext import commands
from dotenv import load_dotenv

class Article:
    def __init__(self):
        pass

    def set_source(self, source):
        self.source = source
    
    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description
 
    def set_author(self, author):
        self.author = author
   
    def set_url(self, url):
        self.url = url

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
    search_phrase = ctx.message.content.lstrip(bot.command_prefix + ctx.command.name).lstrip().replace(' ', '+')
    print(f'{ctx.message.author} is searching for {search_phrase}')

    date_today = str(date.today())

    response = requests.get(f"http://newsapi.org/v2/everything?q={search_phrase}&language=en&from={date_today}&sortBy=publishedAt&apiKey={NEWS_KEY}")
    data = response.json()

    print(data)
    try:
        article_data = data['articles'][0]


        article = article_factory(article_data)

        message = ctx.message.author.mention + '\n' + \
            '**' + article.get_title() + '**' + '\n' + \
            '==========================' + '\n' + \
            article.get_description() + '\n' + \
            'Author(s): ' + article.get_author() + '\n' + \
            'Source: ' + article.get_source() + '\n' + \
            'More at: ' + article.get_url() + '\n'
            #message = 'There are no articles with this title today'
    except IndexError:
        message = f'No news about {search_phrase} today'
    except KeyError:
        pass

    await ctx.send(message)
    

bot.run(TOKEN)
