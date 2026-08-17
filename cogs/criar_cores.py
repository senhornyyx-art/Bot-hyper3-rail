import discord
from discord.ext import commands

SERVIDOR_ORIGEM_ID = 1486183507519865024
SERVIDOR_DESTINO_ID = 1484060471555264633

CARGO_BASE_NOME = "carl-bot"


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
            msg += f"Nome da origem: {origem.name}\n"
            msg += f"Cargos na origem: {len(origem.roles)}\n"

        if destino:
            msg += f"Nome do destino: {destino.name}\n"
            msg += f"Cargos no destino: {len(destino.roles)}\n"

            cargo_base = discord.utils.get(
                destino.roles,
                name=CARGO_BASE_NOME
            )

            msg += f"Cargo '{CARGO_BASE_NOME}' existe: {cargo_base is not None}\n"

            bot_member = destino.get_member(self.bot.user.id)

            if bot_member:
                msg += (
                    f"Permissão gerenciar cargos: "
                    f"{bot_member.guild_permissions.manage_roles}\n"
                )
                msg += (
                    f"Cargo mais alto do bot: "
                    f"{bot_member.top_role.name} "
                    f"(posição {bot_member.top_role.position})\n"
                )

                if cargo_base:
                    msg += (
                        f"Posição do '{CARGO_BASE_NOME}': "
                        f"{cargo_base.position}\n"
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

        cargo_base = discord.utils.get(
            destino.roles,
            name=CARGO_BASE_NOME
        )

        if not cargo_base:
            return await ctx.send(
                f"❌ Cargo `{CARGO_BASE_NOME}` não encontrado no destino."
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

        if bot_member.top_role.position <= cargo_base.position:
            return await ctx.send(
                "❌ O cargo mais alto do bot precisa estar acima "
                f"do cargo `{CARGO_BASE_NOME}`."
            )

        await ctx.send(
            f"⏳ Copiando cargos de **{origem.name}** para **{destino.name}**..."
        )

        cargos_criados = []

        # Percorre os cargos da origem do mais baixo para o mais alto
        for role in origem.roles:
            # Ignora @everyone
            if role.is_default():
                continue

            # Ignora cargos sem cor
            if role.color.value == 0:
                continue

            try:
                nome_original = role.name

                # Se o cargo tiver "✦ " no começo,
                # remove antes de criar o novo nome.
                if nome_original.startswith("✦ "):
                    nome_limpo = nome_original[2:]
                elif nome_original.startswith("✦"):
                    nome_limpo = nome_original[1:].strip()
                else:
                    nome_limpo = nome_original

                novo_nome = f"【🎨】 {nome_limpo}"

                # Evita nomes maiores que o limite do Discord
                novo_nome = novo_nome[:100]

                novo = await destino.create_role(
                    name=novo_nome,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=True,
                    reason=(
                        f"Copiando cargo de {origem.name}"
                    )
                )

                cargos_criados.append(novo)

                print(
                    f"[COPIAR CORES] "
                    f"{role.name} -> {novo.name}"
                )

            except discord.Forbidden:
                print(
                    f"[ERRO] Sem permissão para criar o cargo: "
                    f"{role.name}"
                )

            except discord.HTTPException as e:
                print(
                    f"[ERRO DISCORD] {role.name}: {e}"
                )

            except Exception as e:
                print(
                    f"[ERRO] {role.name}: {e}"
                )

        # Organiza os cargos criados abaixo do carl-bot
        if cargos_criados:
            try:
                # O Discord trabalha com posições crescentes.
                # Colocamos os cargos na ordem correspondente
                # aos cargos da origem.
                cargos_criados.reverse()

                base_position = cargo_base.position

                for i, cargo in enumerate(cargos_criados):
                    nova_posicao = base_position - i - 1

                    if nova_posicao < 1:
                        break

                    try:
                        await cargo.edit(
                            position=nova_posicao,
                            reason="Organizando cargos copiados"
                        )

                    except discord.Forbidden:
                        print(
                            f"[ERRO] Sem permissão para mover: "
                            f"{cargo.name}"
                        )

                    except discord.HTTPException as e:
                        print(
                            f"[ERRO AO MOVER] "
                            f"{cargo.name}: {e}"
                        )

            except Exception as e:
                print(
                    f"[ERRO ORGANIZANDO CARGOS] {e}"
                )

        # Lista os cargos criados
        if cargos_criados:
            texto = "🎨 **Cargos criados:**\n\n"

            for cargo in cargos_criados:
                entrada = f"{cargo.mention} "

                # Mantém a mensagem abaixo de 2000 caracteres
                if len(texto) + len(entrada) > 1900:
                    await ctx.send(texto)
                    texto = ""

                texto += entrada

            if texto:
                await ctx.send(texto)

        await ctx.send(
            f"✅ **{len(cargos_criados)} cargos criados com sucesso!**"
        )


async def setup(bot):
    await bot.add_cog(CriarCores(bot))
