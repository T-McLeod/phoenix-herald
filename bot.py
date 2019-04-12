#!/usr/bin/env python3
import discord
from phoenix import PhoenixParser
import os
import sys

discord_token = os.environ.get('DISCORD_TOKEN')
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

    if message.content.startswith("!who"):
        char = PhoenixParser(message.content.replace("!who ", ""))
        p = char.info
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
            value="Server: #{} - Realm: #{} - {}: #{}".format(
                p.rp_all_time_server,
                p.rp_all_time_realm,
                p.player_class,
                p.rp_all_time_class),
            inline=False)

        embed.add_field(
            name="Last Week: {}".format(
                p.rp_last_week_amount),
            value="Server: #{} - Realm: #{} - {}: #{}".format(
                p.rp_last_week_server,
                p.rp_last_week_realm,
                p.player_class,
                p.rp_last_week_class),
            inline=False)

        embed.add_field(
            name="This Week: {}".format(
                p.rp_this_week_amount),
            value="Server: #{} - Realm: #{} - {}: #{}".format(
                p.rp_this_week_server,
                p.rp_this_week_realm,
                p.player_class,
                p.rp_this_week_class),
            inline=False)

        embed.add_field(
            name="Last 48 hours: {}".format(
                p.rp_last_48h_amount),
            value="Server: #{} - Realm: #{} - {}: #{}".format(
                p.rp_last_48h_server,
                p.rp_last_48h_realm,
                p.player_class,
                p.rp_last_48h_class),
            inline=False)

        embed.set_footer(text="Updated: {}".format(p.last_updated))
        await message.channel.send(embed=embed)

client.run(discord_token)
