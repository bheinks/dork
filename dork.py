import os
import random

import psycopg2
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


class Location:
    def __init__(self, x, y, name, description, image_url):
        self.x = x
        self.y = y
        self.name = name
        self.description = description
        self.image_url = image_url
        self.items = []


class Item:
    def __init__(self, name, full_description, short_description, actions):
        self.name = name
        self.full_description = full_description
        self.short_description = short_description
        self.actions = actions


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.score = 0
        self.moves = 0
        self.x = 0
        self.y = 0
        self.locations = {}

        db = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        self.cursor = db.cursor()

        # Initialize locations
        self.cursor.execute('SELECT * FROM locations')
        for x, y, name, description, items, image_url in self.cursor.fetchall():
            location = Location(x, y, name, description, image_url)

            for item in items:
                self.cursor.execute('SELECT * FROM items WHERE name=%s', (item,))
                location.items.append(Item(*self.cursor.fetchone()))

            self.locations[(location.x, location.y)] = location

    @commands.command()
    async def new(self, ctx):
        self.moves += 1

        embed = self.get_status(discord.Embed(
            title='DORK',
            description='Welcome to DORK, a port of ZORK to Discord.',
            color=0x00ff00))

        await ctx.send(embed=embed)

    @commands.command()
    async def look(self, ctx):
        self.moves += 1
        await ctx.send(embed=self.get_status())

    def get_status(self, embed=None):
        if not embed:
            embed = discord.Embed(color=0x00ff00)

        embed.add_field(name='Score', value=self.score)
        embed.add_field(name='Moves', value=self.moves)

        location = self.get_location()

        embed.set_thumbnail(url=location.image_url)

        items = [item.full_description for item in location.items]
        embed.add_field(name=location.name, value='\n'.join(items), inline=False)

        return embed

    def get_location(self):
        return self.locations[(self.x, self.y)]


if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Game(bot))
    bot.run(DISCORD_TOKEN)
