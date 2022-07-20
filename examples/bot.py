from disnake.ext import commands
from disnake.ext.invitetracker import InviteLogger


bot = commands.InteractionBot()
invite = InviteLogger(bot)

@bot.event
async def on_member_join(member):
    data = invite.get_invite(member)
    await member.guild.text_channels[0].send(data.inviter)

bot.run("TOKEN")
