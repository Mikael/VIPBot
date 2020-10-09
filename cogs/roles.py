from discord import user
from discord import channel
from discord.ext import commands
from .utils.checks import is_admin
import discord
import json


class RolesCog(commands.Cog, name='Roles'):
    """Commands for enabling automatic role assignments"""

    def __init__(self, bot):
        self.bot = bot
        cursor = self.bot.database.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS roles("guild_id" INT, "role_id" INT, "channel_id" INT, "member_ids" TEXT)')
        self.bot.database.commit()
        
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.bot.config["on_join"]:
            return
        notified_channels = []
        cursor = self.bot.database.cursor()
        cursor.execute("SELECT role_id, member_ids, channel_id FROM roles WHERE guild_id = ?", (member.guild.id,))
        self.bot.database.commit()
        rows = cursor.fetchall()
        for row in rows:
            role_id = row[0]
            role = member.guild.get_role(role_id)
            member_ids = json.loads(row[1])
            if role == None:
                self.bot.logger.error("Role with ID %s unavailable!" % str(role_id))
                continue
            if member.id in member_ids:
                try:
                    await member.add_roles(role, reason="Automatic role assignment")
                except discord.errors.Forbidden:
                    self.bot.logger.error("Missing permissions for giving %s (ID: %s) the role %s (ID: %s)" % (str(member), str(member.id), str(role), str(role_id)))
                else:
                    channel = member.guild.get_channel(row[2])
                    if channel == None:
                        self.bot.logger.error("Channel not found: %s" % str(row[2]))
                        continue
                    if not channel.id in notified_channels:
                        await channel.send(self.bot.config["role_received_message"].replace("$MENTION", member.mention))
                        notified_channels.append(channel.id)
                        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not self.bot.config["on_role_change"] or len(before.roles) == len(after.roles):
            return
        notified_channels = []
        cursor = self.bot.database.cursor()
        cursor.execute("SELECT role_id, member_ids, channel_id FROM roles WHERE guild_id = ?", (after.guild.id,))
        self.bot.database.commit()
        rows = cursor.fetchall()
        for row in rows:
            role_id = row[0]
            role = after.guild.get_role(role_id)
            member_ids = json.loads(row[1])
            if role == None:
                self.bot.logger.error("Role with ID %s unavailable!" % str(role_id))
                continue
            if after.id in member_ids and role not in after.roles:
                try:
                    await after.add_roles(role, reason="Automatic role assignment")
                except discord.errors.Forbidden:
                    self.bot.logger.error("Missing permissions for giving %s (ID: %s) the role %s (ID: %s)" % (str(after), str(after.id), str(role), str(role_id)))
                else:
                    channel = after.guild.get_channel(row[2])
                    if channel == None:
                        self.bot.logger.error("Channel not found: %s" % str(row[2]))
                        continue
                    if not channel.id in notified_channels:
                        await channel.send(self.bot.config["role_received_message"].replace("$MENTION", after.mention))
                        notified_channels.append(channel.id)
                        
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.config["on_bootup"]:
            return
        cursor = self.bot.database.cursor()
        for g in self.bot.guilds:
            cursor.execute("SELECT role_id, member_ids, channel_id FROM roles WHERE guild_id = ?", (g.id,))
            self.bot.database.commit()
            rows = cursor.fetchall()
            for row in rows:
                role_id = row[0]
                role = g.get_role(role_id)
                member_ids = json.loads(row[1])
                if role == None:
                    self.bot.logger.error("Role with ID %s unavailable!" % str(role_id))
                    continue
                for m in g.members:
                    if m.id in member_ids and role not in m.roles:
                        try:
                            await m.add_roles(role, reason="Automatic role assignment")
                        except discord.errors.Forbidden:
                            self.bot.logger.error("Missing permissions for giving %s (ID: %s) the role %s (ID: %s)" % (str(m), str(m.id), str(role), str(role_id)))
                        else:
                            channel = m.guild.get_channel(row[2])
                            if channel == None:
                                self.bot.logger.error("Channel not found: %s" % str(row[2]))
                                continue
                            await channel.send(self.bot.config["role_received_message"].replace("$MENTION", m.mention))
    
    @commands.command(name="add-role", aliases=["setup"])
    @is_admin()
    async def add_role(self, ctx, role: discord.Role, channel: discord.TextChannel):
        """Adds a role for automatic role assignment"""
        cursor = self.bot.database.cursor()
        cursor.execute("SELECT role_id FROM roles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
        self.bot.database.commit()
        row = cursor.fetchone()
        if row != None:
            return await ctx.send(":no_entry:  This role has already been added!")
        cursor.execute("INSERT INTO roles(guild_id, role_id, channel_id, member_ids) VALUES (?, ?, ?, ?)", (ctx.guild.id, role.id, channel.id, "[]"))
        self.bot.database.commit()
        await ctx.send(":white_check_mark:  The role has been added.")
        
    @commands.command(name='set-channel', aliases=["change-channel"])
    @is_admin()
    async def set_channel(self, ctx, role: discord.Role, channel: discord.TextChannel):
        """Changes a channel for automatic role assignment"""
        cursor = self.bot.database.cursor()
        cursor.execute("SELECT member_ids FROM roles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
        self.bot.database.commit()
        row = cursor.fetchone()
        if row == None:
            return await ctx.send(":no_entry:  This role hasn't been added!")
        cursor.execute("UPDATE roles SET channel_id = ? WHERE guild_id = ? AND role_id = ?", (channel.id, ctx.guild.id, role.id))
        self.bot.database.commit()
        await ctx.send(":white_check_mark:  The channel has been changed!")
        
    @commands.command(name="remove-role", aliases=["delete-role"])
    @is_admin()
    async def remove(self, ctx, role: discord.Role):
        """Removes a role automatic role assignment"""
        cursor = self.bot.database.cursor()
        cursor.execute("SELECT role_id FROM roles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
        self.bot.database.commit()
        row = cursor.fetchone()
        if row == None:
            return await ctx.send(":no_entry:  This role hasn't been added!")
        cursor.execute("DELETE FROM roles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
        self.bot.database.commit()
        await ctx.send(":white_check_mark:  The role has been removed.")
    
    @commands.command(name="add-member")
    @is_admin()
    async def add_member(self, ctx, role: discord.Role, member: discord.Member):
        """Adds a member for automatic role assignment"""
        cursor = self.bot.database.cursor()
        cursor.execute("SELECT member_ids, channel_id FROM roles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
        self.bot.database.commit()
        row = cursor.fetchone()
        if row == None:
            return await ctx.send(":no_entry:  This role hasn't been added!")
        member_ids = json.loads(row[0])
        if member.id in member_ids:
            return await ctx.send(":no_entry:  This user has already been added to this role!")
        member_ids.append(member.id)
        cursor.execute("UPDATE roles SET member_ids = ? WHERE guild_id = ? AND role_id = ?", (json.dumps(member_ids), ctx.guild.id, role.id))
        self.bot.database.commit()
        await ctx.send(":white_check_mark:  The user has been added to this role!")
        if not role in member.roles:
            try:
                await member.add_roles(role, reason="Automatic role assignment")
            except discord.errors.Forbidden:
                self.bot.logger.error("Missing permissions for giving %s (ID: %s) the role %s (ID: %s)" % (str(member), str(member.id), str(role), str(role_id)))
            else:
                channel = ctx.guild.get_channel(row[1])
                if channel == None:
                    self.bot.logger.error("Channel not found: %s" % str(row[1]))
                    return
                await channel.send(self.bot.config["role_received_message"].replace("$MENTION", member.mention))
    
    @commands.command(name="remove-member", aliases=["delete-member"])
    @is_admin()
    async def remove_member(self, ctx, role: discord.Role, user_id: int):
        """Removes a member from automatic role assignment"""
        cursor = self.bot.database.cursor()
        cursor.execute("SELECT member_ids FROM roles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
        self.bot.database.commit()
        row = cursor.fetchone()
        if row == None:
            return await ctx.send(":no_entry:  This role hasn't been added!")
        member_ids = json.loads(row[0])
        if user_id not in member_ids:
            return await ctx.send(":no_entry:  This user hasn't been added to this role!")
        member_ids.remove(user_id)
        cursor.execute("UPDATE roles SET member_ids = ? WHERE guild_id = ? AND role_id = ?", (json.dumps(member_ids), ctx.guild.id, role.id))
        self.bot.database.commit()
        await ctx.send(":white_check_mark:  The user has been added removed from role!")
        
        
def setup(bot):
    bot.add_cog(RolesCog(bot))