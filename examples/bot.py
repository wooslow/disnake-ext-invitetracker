import disnake
from disnake.ext import commands
from disnake.ext.invitetracker import InviteLogger


bot = commands.InteractionBot(intents=disnake.Intents.all())
invite = InviteLogger(bot)

@bot.event
async def on_member_join(member):
    data: disnake.Invite = await invite.get_invite(member)
    print(data.inviter)

bot.run("TOKEN")