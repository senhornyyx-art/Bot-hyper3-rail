import discord
from discord.ext import commands

SERVIDOR_ORIGEM_ID = 1486183507519865024
SERVIDOR_DESTINO_ID = 1484060471555264633


class CriarCores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def debug_core(self, ctx):
        origem = self.bot.get_guild(SERVIDOR_ORIGEM_ID)
        destino = self.bot.get_guild(SERVIDOR_DESTINO_ID)

        msg = "📊 **DEBUG**\n\n"
        msg += f"Origem encontrada: {origem is not None}\n"
        msg += f"Destino encontrado: {destino is not None}\n"

        if origem:
            msg += f"Servidor origem: {origem.name}\n"
            msg += f"Cargos na origem: {len(origem.roles)}\n"

        if destino:
            msg += f"Servidor destino: {destino.name}\n"
            msg += f"Cargos no destino: {len(destino.roles)}\n"

            bot_member = destino.get_member(self.bot.user.id)

            if bot_member:
                msg += (
                    f"Gerenciar cargos: "
                    f"{bot_member.guild_permissions.manage_roles}\n"
                )
                msg += (
                    f"Cargo mais alto do bot: "
                    f"{bot_member.top_role.name}\n"
                )

        await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def copiarcores(self, ctx):
        origem = self.bot.get_guild(SERVIDOR_ORIGEM_ID)
        destino = self.bot.get_guild(SERVIDOR_DESTINO_ID)

        if not origem:
            return await ctx.send(
                "❌ Bot não está no servidor de origem."
            )

        if not destino:
            return await ctx.send(
                "❌ Bot não está no servidor de destino."
            )

        bot_member = destino.get_member(self.bot.user.id)

        if not bot_member:
            return await ctx.send(
                "❌ Não consegui encontrar o bot no servidor de destino."
            )

        if not bot_member.guild_permissions.manage_roles:
            return await ctx.send(
                "❌ O bot não possui permissão de **Gerenciar Cargos**."
            )

        await ctx.send(
            f"⏳ Copiando cargos de **{origem.name}**..."
        )

        cargos_criados = []

        # Pega os cargos da origem na ordem original
        for role in origem.roles:

            # Ignora @everyone
            if role.is_default():
                continue

            # Ignora cargos sem cor
            if role.color.value == 0:
                continue

            try:
                nome_original = role.name

                # Procura pelo "✦" no cargo da ORIGEM
                if nome_original.startswith("✦ "):
                    nome_limpo = nome_original[2:]
                elif nome_original.startswith("✦"):
                    nome_limpo = nome_original[1:].strip()
                else:
                    nome_limpo = nome_original

                # Nome que será criado no DESTINO
                novo_nome = f"【🎨】 {nome_limpo}"

                # Limite máximo de caracteres do Discord
                novo_nome = novo_nome[:100]

                novo_cargo = await destino.create_role(
                    name=novo_nome,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable,
                    reason="Cópia de cargos coloridos"
                )

                cargos_criados.append(novo_cargo)

                print(
                    f"[COPIAR CORES] "
                    f"{role.name} -> {novo_cargo.name}"
                )

            except discord.Forbidden:
                print(
                    f"[ERRO] Sem permissão para criar: {role.name}"
                )

            except discord.HTTPException as e:
                print(
                    f"[ERRO DISCORD] {role.name}: {e}"
                )

            except Exception as e:
                print(
                    f"[ERRO] {role.name}: {e}"
                )

        # Reorganiza os cargos criados para manter
        # aproximadamente a mesma ordem da origem.
        if cargos_criados:

            try:
                for i, cargo in enumerate(cargos_criados):
                    try:
                        await cargo.edit(
                            position=i + 1,
                            reason="Organizando cargos copiados"
                        )

                    except discord.Forbidden:
                        print(
                            f"[ERRO] Não foi possível mover: "
                            f"{cargo.name}"
                        )

                    except discord.HTTPException as e:
                        print(
                            f"[ERRO AO MOVER] "
                            f"{cargo.name}: {e}"
                        )

            except Exception as e:
                print(
                    f"[ERRO ORGANIZANDO] {e}"
                )

        # Envia os cargos criados em mensagens separadas
        if cargos_criados:

            texto = "🎨 **Cargos criados:**\n\n"

            for cargo in cargos_criados:
                entrada = f"{cargo.mention} "

                if len(texto) + len(entrada) > 1900:
                    await ctx.send(texto)
                    texto = ""

                texto += entrada

            if texto:
                await ctx.send(texto)

        await ctx.send(
            f"✅ **{len(cargos_criados)} cargos criados!**"
        )


async def setup(bot):
    await bot.add_cog(CriarCores(bot))
