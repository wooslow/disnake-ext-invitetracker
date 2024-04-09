import disnake
from disnake.ext import commands
from disnake.ext.invitetracker import InviteTracker

bot = commands.InteractionBot(intents=disnake.Intents.all())
invite = InviteTracker(bot)


@bot.event
async def on_member_join(member: disnake.Member):
    original_invite: disnake.Invite = await invite.get_invite(member)
    print(f"{member} joined using {original_invite.code}")

bot.run("TOKEN")
