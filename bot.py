#!/usr/bin/env python3
import discord
from discord.ext import commands
from phoenix.PhoenixParser import PhoenixParser
from phoenix.RealmRanks import RealmRanks
import os
import sys
import sqlite3

discord_owner_id = int(os.environ.get('DISCORD_OWNER_ID'))
discord_token = os.environ.get('DISCORD_TOKEN')
discord_hosted_by = os.environ.get('DISCORD_HOSTED_BY')

if not discord_owner_id:
    print("Missing ENV variable DISCORD_OWNER_ID, please set and try again")
    sys.exit(1)

if not discord_hosted_by:
    print("Missing ENV variable DISCORD_HOSTED_BY, please set and try again")
    sys.exit(1)

if not discord_token:
    print("Missing ENV variable DISCORD_TOKEN, please set and try again")
    sys.exit(1)

conn = sqlite3.connect('data{}phoenix-herald.sqlite'.format(os.sep))

bot = commands.Bot(
    command_prefix='!',
    case_insensitive=True
)


async def clean_name(some_var):
    return ''.join(char for char in some_var if char.isalnum())


async def db_create_schema():
    global conn
    c = conn.cursor()
    sql = " CREATE TABLE IF NOT EXISTS me( \
              userId int not null, \
              playerName varchar(255) not null \
            );"
    c.execute(sql)
    conn.commit()


async def db_delete_char(player_id, char):
    global conn
    c = conn.cursor()
    sql = "DELETE FROM me WHERE userId={} AND playerName='{}';".format(
        player_id, await clean_name(char))
    c.execute(sql)
    conn.commit()


async def db_insert_char(player_id, char):
    global conn
    c = conn.cursor()
    sql = "INSERT INTO me (userId, playerName) VALUES ({}, '{}');".format(
        player_id, await clean_name(char))
    c.execute(sql)
    conn.commit()


async def db_get_chars(player_id):
    global conn
    c = conn.cursor()
    sql = "SELECT playerName \
            FROM me \
            WHERE userId={} \
            ORDER BY playerName ASC;".format(player_id)
    c.execute(sql)
    all_rows = c.fetchall()

    return [x[0] for x in all_rows]


async def is_owner(ctx):
    return ctx.author.id == discord_owner_id


@bot.event
async def on_ready():
    print('Discord.py Version: {}'.format(discord.__version__))
    print("I'm known as:       {}".format(bot.user.name))
    print("My masters ID is:   {}".format(discord_owner_id))
    print("Creating database schema")
    await db_create_schema()


@bot.command(name='me')
async def me(ctx, *args):
    # query db and get matches based on your id
    # we always want that list due to add/delete functions.
    in_db = await db_get_chars(ctx.author.id)

    if not args:
        if len(in_db) == 0:
            await ctx.send(
                "No saved players for your id, please use '!me add <name>'")
            return
        embed = discord.Embed(
            title="{} characters".format(
                ctx.author.name.capitalize()), color=16312092)

        for char in in_db:
            try:
                player = PhoenixParser(char)
                p = player.info

                embed.add_field(
                    name="{} (Lvl {} {} {})".format(
                        p.player_name.capitalize(),
                        p.player_level,
                        p.player_race,
                        p.player_class),
                    value="Total: {} - {} ({})".format(
                        p.rp_all_time_amount,
                        p.player_rr,
                        p.player_pretty_rr),
                    inline=False)
            except Exception:
                pass
        await ctx.send(embed=embed)
    else:
        if args[0].lower() == "add" and len(args) > 1:
            # Check if player exist by query
            # IF exist, check if not alread in db
            # If in db, just skip, else add
            characters = list(args)
            characters.pop(0)
            saved = []
            alread_added = []

            try:
                for char in characters:
                    char = char.capitalize()
                    if char not in in_db:
                        player = PhoenixParser(char)
                        saved.append(char)
                        await db_insert_char(ctx.author.id, char)
                    else:
                        alread_added.append(char)
            except Exception:
                pass

            if len(saved) > 0:
                await ctx.send("Saved: {}".format(', '.join(saved)))
                if len(alread_added) > 0:
                    await ctx.send("Already saved: {}".format(
                        ', '.join(alread_added)))
            else:
                if len(alread_added) > 0:
                    await ctx.send("Already saved: {}".format(
                        ', '.join(alread_added)))
                else:
                    await ctx.send("No valid players found")
        elif args[0].lower() == "del" and len(args) > 1:
            # check if you have the player in your db list
            # If in db, delete record
            characters = list(args)
            characters.pop(0)
            deleted = []
            for char in characters:
                char = char.capitalize()
                if char in in_db:
                    await db_delete_char(ctx.author.id, char)
                    deleted.append(char)
            if len(deleted) > 0:
                await ctx.send("Removing: {}".format(', '.join(deleted)))
            else:
                await ctx.send("Unable to delete anything")
    return


@bot.command()
@commands.check(is_owner)
async def info(ctx):
    embed = discord.Embed(
        title="{} Guild(s) Using {}".format(
            len(bot.guilds),
            bot.user.name),
        description="hosted by {}".format(discord_hosted_by),
        color=16312092)

    for guild in bot.guilds:
        embed.add_field(name="{} ({})".format(guild.name, guild.id),
                        value=guild.owner,
                        inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def who(ctx, player):
    try:
        char = PhoenixParser(player)
        p = char.info

        rr = RealmRanks(p.player_rr,
                        int(p.rp_all_time_amount.replace(",", "")))

        embed = discord.Embed(
            title="{}, ({} {})".format(
                p.player_name,
                p.player_race,
                p.player_class),
            url=p.player_url,
            description="Guild: {} - Level: {}".format(
                p.player_guild,
                p.player_level),
            color=p.realm_color
        )

        embed.add_field(
            name="Total: {} - {} ({})".format(
                p.rp_all_time_amount,
                p.player_rr,
                p.player_pretty_rr),
            value="Left to, {}: {}, {}: {}\nServer: #{} - {}: #{} - {}: #{}"
            .format(
                rr.next_rank(pretty=True),
                rr.next_rank(),
                rr.next_level(pretty=True),
                rr.next_level(),
                p.rp_all_time_server,
                p.player_realm,
                p.rp_all_time_realm,
                p.player_class,
                p.rp_all_time_class),
            inline=False)

        embed.add_field(
            name="Last Week: {}".format(
                p.rp_last_week_amount),
            value="Server: #{} - {}: #{} - {}: #{}".format(
                p.rp_last_week_server,
                p.player_realm,
                p.rp_last_week_realm,
                p.player_class,
                p.rp_last_week_class),
            inline=False)

        embed.add_field(
            name="This Week: {}".format(
                p.rp_this_week_amount),
            value="Server: #{} - {}: #{} - {}: #{}".format(
                p.rp_this_week_server,
                p.player_realm,
                p.rp_this_week_realm,
                p.player_class,
                p.rp_this_week_class),
            inline=False)

        embed.add_field(
            name="Last 48 hours: {}".format(
                p.rp_last_48h_amount),
            value="Server: #{} - {}: #{} - {}: #{}".format(
                p.rp_last_48h_server,
                p.player_realm,
                p.rp_last_48h_realm,
                p.player_class,
                p.rp_last_48h_class),
            inline=False)

        embed.set_footer(text="Updated: {}".format(p.last_updated))
        await ctx.send(embed=embed)
    except Exception:
        embed = discord.Embed(
            title="Unable to find player {}".format(player),
            description="This player does not exist or was misspelled",
            color=16312092
        )
        await ctx.send(embed=embed)

bot.run(discord_token)
