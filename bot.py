#!/usr/bin/env python3
import discord
from phoenix.PhoenixParser import PhoenixParser
from phoenix.RealmRanks import RealmRanks
import os
import sys
import re

pattern = re.compile("^[!,?]{1}who ([a-z0-9]+)$")

discord_token = os.environ.get('DISCORD_TOKEN')
discord_hosted_by = os.environ.get('DISCORD_HOSTED_BY')

if not discord_token:
    print("Missing ENV variable DISCORD_TOKEN, please set and try again")
    sys.exit(1)

if not discord_token:
    print("Missing ENV variable DISCORD_TOKEN, please set and try again")
    sys.exit(1)

client = discord.Client()


@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)
    print('Discord.py Version: {}'.format(discord.__version__))
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!server':
        embed = discord.Embed(
                title="Guilds Using Phoenix-Bot",
                description="hosted by {}".format(discord_hosted_by),
                color=16312092)

        for guild in client.guilds:
            embed.add_field(name=guild.name, value=guild.owner, inline=False)

        await message.channel.send(embed=embed)

    m = re.match(pattern, message.content.lower())

    if m:
        search_for = m.group(1)

        try:
            char = PhoenixParser(search_for)
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
                value="Left to, {}: {}, {}: {}\n\
    Server: #{} - {}: #{} - {}: #{}".format(
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
            await message.channel.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Unable to find player {}".format(search_for),
                description="This player does not exist or was misspelled",
                color=16312092
            )
            await message.channel.send(embed=embed)

client.run(discord_token)
