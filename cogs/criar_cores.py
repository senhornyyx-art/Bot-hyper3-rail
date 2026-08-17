import discord
from discord.ext import commands

SERVIDOR_ORIGEM_ID = 1486183507519865024
SERVIDOR_DESTINO_ID = 1538601853632118877


class CriarCores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def encontrar_guild(self, guild_id):
        for guild in self.bot.guilds:
            if guild.id == guild_id:
                return guild
        return None

    @commands.command()
    async def debug_core(self, ctx):
        msg = "📊 **DEBUG — SERVIDORES DO BOT**\n\n"
        msg += f"Total: `{len(self.bot.guilds)}`\n\n"

        encontrou_origem = False
        encontrou_destino = False

        for guild in self.bot.guilds:
            marcador = ""

            if guild.id == SERVIDOR_ORIGEM_ID:
                marcador = " ⬅️ **ORIGEM**"
                encontrou_origem = True

            if guild.id == SERVIDOR_DESTINO_ID:
                marcador = " ⬅️ **DESTINO**"
                encontrou_destino = True

            msg += (
                f"**{guild.name}**\n"
                f"🆔 `{guild.id}`{marcador}\n\n"
            )

            if len(msg) >= 1800:
                await ctx.send(msg)
                msg = ""

        if msg:
            await ctx.send(msg)

        await ctx.send(
            "🔎 **RESULTADO**\n\n"
            f"📥 Origem: `{encontrou_origem}`\n"
            f"📤 Destino: `{encontrou_destino}`"
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def copiarcores(self, ctx):

        origem = self.encontrar_guild(SERVIDOR_ORIGEM_ID)
        destino = self.encontrar_guild(SERVIDOR_DESTINO_ID)

        if origem is None:
            return await ctx.send(
                f"❌ Não encontrei a origem `{SERVIDOR_ORIGEM_ID}`."
            )

        if destino is None:
            return await ctx.send(
                f"❌ Não encontrei o destino `{SERVIDOR_DESTINO_ID}`.\n"
                f"Use `.debug_core` para ver os servidores."
            )

        bot_member = destino.get_member(self.bot.user.id)

        if bot_member is None:
            return await ctx.send(
                "❌ O bot está no servidor, mas não consegui "
                "encontrar o membro do bot dentro dele."
            )

        if not bot_member.guild_permissions.manage_roles:
            return await ctx.send(
                "❌ O bot não possui **Gerenciar Cargos**."
            )

        await ctx.send(
            f"⏳ Copiando cargos de **{origem.name}** "
            f"para **{destino.name}**..."
        )

        cargos_criados = []

        for role in origem.roles:

            if role.is_default():
                continue

            if role.color.value == 0:
                continue

            try:
                nome = role.name

                # Remove ✦ apenas da origem
                if nome.startswith("✦ "):
                    nome = nome[2:]
                elif nome.startswith("✦"):
                    nome = nome[1:].strip()

                novo_nome = f"【🎨】 {nome}"[:100]

                novo = await destino.create_role(
                    name=novo_nome,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable,
                    reason="Cópia de cargos coloridos"
                )

                cargos_criados.append(novo)

            except Exception as e:
                print(f"[ERRO] {role.name}: {e}")

        await ctx.send(
            f"✅ **{len(cargos_criados)} cargos criados!**"
        )


async def setup(bot):
    await bot.add_cog(CriarCores(bot))
