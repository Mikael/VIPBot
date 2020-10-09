# -*- coding: utf-8 -*-
import aiohttp
import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import io
import json
import logging
import os
from os import listdir
from os.path import isdir, isfile, join
import signal
import sqlite3
import sys
import traceback



class Bot(commands.AutoShardedBot):

    def hex_to_rgb(self, value):
        h = value.replace("#", "")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def __init__(self):

        self.bot_name = "AutoRoleBot"

        self.logger = logging.getLogger(self.bot_name)
        self.logger.setLevel(logging.DEBUG)

        self.start_time = datetime.now()

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

        # Load config
        try:
            with open("config.json", encoding="utf-8") as f:
                self.config = json.load(f)
        except json.decoder.JSONDecodeError:
            self.logger.exception("Unable to decode config.json, please see the following traceback for more information. Exiting.")
            exit(1)
        except FileNotFoundError:
            self.logger.exception("Unable to find config.json. Make sure it's in the same directory as main.py. Exiting.")
            exit(1)
        except:
            self.logger.exception("Unexpected error while reading or decoding config.json. Please see the following traceback for more information. Exiting.")
            exit(1)
        else:
            self.logger.debug("Loaded config.json")

        # Set the log file handler
        fh = logging.FileHandler(join(self.config["logs_folder"], datetime.now().strftime(self.config["log_filename"])))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

        # Connect to database
        self.database = sqlite3.connect(self.config["database"])

        # Set the embed color
        rgb = self.hex_to_rgb(self.config["embed_color"])
        self.embed_color = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])

        super().__init__(command_prefix=self.config["prefix"], case_insensitive=True, description=self.config["description"])

        self.load_cogs()

        self.add_check(self.no_bot_interaction)
        self.add_check(self.send_permission)


    def load_cogs(self):
        for extension in [f.replace('.py', '') for f in listdir("cogs") if isfile(join("cogs", f))]:
            try:
                self.load_extension("cogs." + extension)
            except(discord.ClientException, ImportError):
                self.logger.exception("Failed to load extension " + str(extension))
                continue
            except(discord.ext.commands.errors.NoEntryPointError):
                self.logger.exception(str(extension) + " doesn't have a 'setup' function, ignoring")
                continue
            else:
                self.logger.debug("Loaded cogs/" + extension + ".py")


    async def on_ready(self):
        self.logger.info("%s is ready." % self.bot_name)


    async def on_message(self, message):
        await bot.process_commands(message)


    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        traceback_text = "".join(traceback.format_exception(type(error), error, error.__traceback__, 8))
        self.logger.error("Exception in command %s: %s" % (ctx.command, str(error)))
        self.logger.error(traceback_text)

        if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **This command is currently disabled.**", color=self.embed_color))
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **This command is on cooldown for another " + str("%.2f" % error.retry_after) + " seconds!**", color=self.embed_color))
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **You need the administrator permission on your server to do that!**", color=self.embed_color))
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **This command cannot be used in DMs!**", color=self.embed_color))
        elif isinstance(error, commands.NotOwner):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **This command is exclusive to the administration of the bot!**", color=self.embed_color))
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **The bot does not have sufficient permissions to run this command!**", color=self.embed_color))
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **Invalid argument(s)! Refer to the help command for more information on how to use this command.**", color=self.embed_color))
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=discord.Embed(title=":no_entry:  **There's an argument missing! Refer to the help command for more information on how to use this command.**", color=self.embed_color))

        await ctx.send(embed=discord.Embed(title=":no_entry:  **There was an unexpected error when running this command! Sorry about that. :(**", color=self.embed_color))


    # GLOBAL CHECKS
    ## Disable bot interaction
    def no_bot_interaction(self, ctx):
        return not ctx.author.bot


    ## Look for send permissions first to avoid unnecessary exceptions
    def send_permission(self, ctx):
        return ctx.channel.permissions_for(ctx.me).send_messages


    def run(self):
        super().run(self.config["token"], reconnect=True)


    async def close(self):
        self.logger.info("Exiting gracefully...")
        await super().close()



if __name__ == "__main__":
    bot = Bot()
    bot.run()
