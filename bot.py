#!/usr/bin/env python3
import discord
from discord.ext import commands
from phoenix.PhoenixParser import PhoenixParser
from phoenix.RealmRanks import RealmRanks
import os
import sys

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

bot = commands.Bot(
    command_prefix='!',
    case_insensitive=True
)


async def is_owner(ctx):
    return ctx.author.id == discord_owner_id


@bot.event
async def on_ready():
    print('Discord.py Version: {}'.format(discord.__version__))
    print("I'm known as:       {}".format(bot.user.name))
    print("My masters ID is:   {}".format(discord_owner_id))


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
