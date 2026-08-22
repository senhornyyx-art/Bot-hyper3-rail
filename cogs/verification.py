import discord
from discord.ext import commands
from discord import app_commands

# =========================================================
# CONFIGURAÇÕES
# =========================================================

ROLE_ID = 1538708137748594799
CHANNEL_ID = 1539108037120229486
GUILD_ID = 1538601853632118877

IMAGE_URL = "https://cdn.discordapp.com/attachments/1538607175004455012/1539405747538890812/UQjECAI.png?ex=6a8632d2&is=6a84e152&hm=aacfad9292ca73220b574db55e6b67707c913196c4b6a8fcc488b80c826b6460&"

# Mensagem que possui o tópico
TOPIC_MESSAGE_ID = 1539497894816514120

EMOJI_CONVITE = "<:convite:1526352250837143552>"
EMOJI_VERIFY = "<:verify:1526360202197209128>"

ENGLISH_BUTTON_ID = "english_verification_btn"


# =========================================================
# TEXTOS
# =========================================================

TEXTO_PORTUGUES = """# <:topic1:1526287141775343656> <:convite:1526352250837143552> Convide 2 pessoas
> - Convide 2 pessoas usando seu convite e quando atingir a meta, clique em "Validar verificação".

# <:topicopen:1526287216954052719> <:verify:1526360202197209128> Benefícios:
> - 🎁 Presets, Project Files & softwares (After Effects, Alight Motion, After Motion Z)
> - 💻 CC's, Packs, Fontes, Overlays, Clipes, Músicas e muito mais recursos de edição em todos os estilos.
> - ⭐ Suporte e canal de dúvidas para editores.

# <:topicopen:1526287216954052719> <:__:1526354605028413440> Como ver seus convites:
> - Clique em "Meus convites" para acompanhar seu progresso. Observação: para validar a pessoa precisa entrar no servidor.
> - Clique em "Criar convite" para gerar seu link de convite e enviar para duas pessoas.

-# <:prints:1526358671691612200> Dúvidas ou problemas com a verificação? Anexe prints como provas, ou tire sua dúvida no tópico abaixo. O suporte é voluntáriado, então aguarde com paciência."""


TEXTO_INGLES = """# <:topic1:1526287141775343656> <:convite:1526352250837143552> Invite 2 people
> - Invite 2 people using your invite and once you reach the goal, click "Verify".

# <:topicopen:1526287216954052719> <:verify:1526360202197209128> Benefits:
> - 🎁 Presets, Project Files & software (After Effects, Alight Motion, After Motion Z)
> - 💻 CC's, Packs, Fonts, Overlays, Clips, Music and many more editing resources in all styles.
> - ⭐ Support and a help channel for editors.

# <:topicopen:1526287216954052719> <:__:1526354605028413440> How to check your invites:
> - Click "My Invites" to check your progress. Note: the person must join the server for the invite to be validated.
> - Click "Create Invite" to generate your invite link and send it to two people.

-# <:prints:1526358671691612200> Questions or problems with verification? Attach screenshots as proof or ask your question in the thread below. Support is voluntary, so please be patient."""


# =========================================================
# MENSAGEM DO TÓPICO
# =========================================================

TOPICO_PORTUGUES = """## <:book:1539496360061968484> **・ Utilize este tópico corretamente:**
 * **Use este tópico** para **tirar dúvidas, comentar ou discutir** sobre o sistema de convites.
 * **A pessoa convidada precisa entrar** no servidor para validar o convite na verificação.
 * **Evite mensagens fora de contexto** para manter a organização do tópico"""

TOPICO_INGLES = """## <:book:1539496360061968484> **・ Use this thread correctly:**
 * **Use this thread** to **ask questions, comment or discuss** the invite system.
 * **The invited person must join** the server for the invite to be validated.
 * **Avoid off-topic messages** to keep the thread organized."""


# =========================================================
# VIEW PRINCIPAL
# =========================================================

class VerificationView(discord.ui.LayoutView):

    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

        container = discord.ui.Container(

            discord.ui.MediaGallery(
                discord.MediaGalleryItem(IMAGE_URL)
            ),

            discord.ui.Separator(),

            discord.ui.TextDisplay(
                TEXTO_PORTUGUES
            ),

            discord.ui.Separator(),

            discord.ui.ActionRow(

                discord.ui.Button(
                    label="Validar verificação",
                    style=discord.ButtonStyle.green,
                    custom_id="verify_btn",
                    emoji=discord.PartialEmoji.from_str(
                        EMOJI_VERIFY
                    )
                ),

                discord.ui.Button(
                    label="Meus convites",
                    style=discord.ButtonStyle.blurple,
                    custom_id="my_invites_btn",
                    emoji=discord.PartialEmoji.from_str(
                        EMOJI_CONVITE
                    )
                ),

                discord.ui.Button(
                    label="Criar convite",
                    style=discord.ButtonStyle.gray,
                    custom_id="create_invite_btn",
                    emoji="🔗"
                ),

                discord.ui.Button(
                    label="English Instructions",
                    style=discord.ButtonStyle.gray,
                    custom_id=ENGLISH_BUTTON_ID,
                    emoji="🇺🇸"
                )
            ),

            accent_color=discord.Color.from_str(
                "#3F4147"
            )
        )

        self.add_item(container)

    # =====================================================
    # INTERACTIONS
    # =====================================================

    async def interaction_check(
        self,
        interaction: discord.Interaction
    ) -> bool:

        custom_id = (
            interaction.data.get("custom_id")
            if interaction.data
            else None
        )

        if custom_id == "verify_btn":
            await self.verify(interaction)

        elif custom_id == "my_invites_btn":
            await self.my_invites(interaction)

        elif custom_id == "create_invite_btn":
            await self.create_invite(interaction)

        elif custom_id == ENGLISH_BUTTON_ID:
            await self.english_instructions(interaction)

        return False

    # =====================================================
    # BOTÃO ENGLISH INSTRUCTIONS
    # =====================================================

    async def english_instructions(
        self,
        interaction: discord.Interaction
    ):

        # -------------------------------------------------
        # PRIMEIRO: RESPONDE AO CLIQUE COM A VERSÃO INGLESA
        # EM EPHEMERAL
        # -------------------------------------------------

        view = discord.ui.LayoutView(
            timeout=60
        )

        container = discord.ui.Container(
            discord.ui.TextDisplay(
                TEXTO_INGLES
            ),
            accent_color=discord.Color.from_str(
                "#3F4147"
            )
        )

        view.add_item(container)

        await interaction.response.send_message(
            view=view,
            ephemeral=True
        )

        # -------------------------------------------------
        # PROCURA A MENSAGEM QUE POSSUI O TÓPICO
        # -------------------------------------------------

        try:
            canal = await self.bot.fetch_channel(
                CHANNEL_ID
            )

            mensagem = await canal.fetch_message(
                TOPIC_MESSAGE_ID
            )

        except Exception as e:
            print(
                f"❌ Erro ao localizar mensagem do tópico: {e}"
            )
            return

        # -------------------------------------------------
        # PEGA O TÓPICO EXISTENTE
        # -------------------------------------------------

        thread = getattr(
            mensagem,
            "thread",
            None
        )

        # Caso a própria interação tenha acontecido dentro
        # de um tópico, utiliza esse tópico.
        if thread is None and isinstance(
            interaction.channel,
            discord.Thread
        ):
            thread = interaction.channel

        if thread is None:
            print(
                "❌ O tópico da mensagem não foi encontrado."
            )
            return

        # -------------------------------------------------
        # MANDA A MENÇÃO SEPARADAMENTE
        # -------------------------------------------------

        try:
            mensagem_mencao = await thread.send(
                interaction.user.mention
            )

            # -------------------------------------------------
            # MANDA A MENSAGEM EM INGLÊS
            # -------------------------------------------------

            mensagem_ingles = await thread.send(
                TOPICO_INGLES
            )

            # -------------------------------------------------
            # APAGA A MENÇÃO
            # -------------------------------------------------

            try:
                await mensagem_mencao.delete()
            except discord.NotFound:
                pass

            # -------------------------------------------------
            # ADICIONA O SOLICITADO POR NO FINAL
            # -------------------------------------------------

            await mensagem_ingles.edit(
                content=(
                    f"{TOPICO_INGLES}\n"
                    f"-# Requested by: {interaction.user.name}"
                )
            )

        except discord.Forbidden:
            print(
                "❌ Sem permissão para enviar ou apagar "
                "mensagens no tópico."
            )

        except Exception as e:
            print(
                f"❌ Erro ao enviar instruções no tópico: {e}"
            )

    # =====================================================
    # BOTÃO: VALIDAR VERIFICAÇÃO
    # =====================================================

    async def verify(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        guild = interaction.guild
        member = interaction.user

        if not guild or guild.id != GUILD_ID:
            await interaction.followup.send(
                "❌ | Este sistema de verificação não funciona neste servidor.",
                ephemeral=True
            )
            return

        role = guild.get_role(
            ROLE_ID
        )

        if not role:
            await interaction.followup.send(
                "❌ | O cargo de verificação não foi encontrado. Contate um administrador.",
                ephemeral=True
            )
            return

        if role in member.roles:
            await interaction.followup.send(
                f"{EMOJI_VERIFY} | Você já está verificado e possui o cargo!",
                ephemeral=True
            )
            return

        cog = self.bot.get_cog(
            "Verification"
        )

        if not cog:
            await interaction.followup.send(
                "❌ | Sistema temporariamente indisponível.",
                ephemeral=True
            )
            return

        invites_count = await cog.get_user_invites(
            member.id
        )

        if invites_count >= 2:

            try:

                await member.add_roles(
                    role
                )

                await interaction.followup.send(
                    f"{EMOJI_VERIFY} | **Verificação concluída!** "
                    f"Você convidou {invites_count} pessoas e recebeu o cargo **{role.name}**.",
                    ephemeral=True
                )

            except discord.Forbidden:

                await interaction.followup.send(
                    "❌ | Eu não tenho permissão para gerenciar cargos. "
                    "Verifique se meu cargo está acima do cargo de verificação na lista de cargos.",
                    ephemeral=True
                )

        else:

            await interaction.followup.send(
                f"❌ | Você precisa de 2 convites. "
                f"No momento, você tem apenas **{invites_count}/2** convites validados.",
                ephemeral=True
            )

    # =====================================================
    # BOTÃO: MEUS CONVITES
    # =====================================================

    async def my_invites(
        self,
        interaction: discord.Interaction
    ):

        if (
            not interaction.guild
            or interaction.guild.id != GUILD_ID
        ):
            await interaction.response.send_message(
                "❌ | Este sistema de verificação não funciona neste servidor.",
                ephemeral=True
            )
            return

        cog = self.bot.get_cog(
            "Verification"
        )

        if not cog:
            await interaction.response.send_message(
                "❌ | Sistema temporariamente indisponível.",
                ephemeral=True
            )
            return

        invites_count = await cog.get_user_invites(
            interaction.user.id
        )

        await interaction.response.send_message(
            f"{EMOJI_CONVITE} | Você possui atualmente **{invites_count}** convites validados.",
            ephemeral=True
        )

    # =====================================================
    # BOTÃO: CRIAR CONVITE
    # =====================================================

    async def create_invite(
        self,
        interaction: discord.Interaction
    ):

        if (
            not interaction.guild
            or interaction.guild.id != GUILD_ID
        ):
            await interaction.response.send_message(
                "❌ | Este sistema de verificação não funciona neste servidor.",
                ephemeral=True
            )
            return

        cog = self.bot.get_cog(
            "Verification"
        )

        if not cog:
            await interaction.response.send_message(
                f"{EMOJI_CONVITE} | ❌ Sistema temporariamente indisponível.",
                ephemeral=True
            )
            return

        user_id = interaction.user.id

        convite_existente = None

        # -------------------------------------------------
        # PROCURA NO CACHE
        # -------------------------------------------------

        for code, data in cog.invite_cache.items():

            if data["inviter"] == user_id:

                convite_existente = code
                break

        # -------------------------------------------------
        # PROCURA NO SERVIDOR
        # -------------------------------------------------

        if not convite_existente:

            try:

                invites = await interaction.guild.invites()

                for invite in invites:

                    if (
                        invite.inviter
                        and invite.inviter.id == user_id
                    ):

                        convite_existente = invite.code

                        cog.invite_cache[
                            invite.code
                        ] = {
                            "uses": invite.uses,
                            "inviter": user_id
                        }

                        break

            except discord.Forbidden:

                await interaction.response.send_message(
                    "❌ | Não consigo verificar seus convites existentes. "
                    "Preciso da permissão **Gerenciar Servidor**.",
                    ephemeral=True
                )
                return

            except Exception as e:

                print(
                    f"❌ Erro ao verificar convites existentes: {e}"
                )

        # -------------------------------------------------
        # JÁ POSSUI CONVITE
        # -------------------------------------------------

        if convite_existente:

            await interaction.response.send_message(
                content=(
                    f"⚠️ | Você já possui um convite criado! "
                    f"Use o seu link:\n"
                    f"`https://discord.gg/{convite_existente}`\n"
                    f"(BASTA CLICAR NO NOME PRETO PARA COPIAR)"
                ),
                ephemeral=True
            )
            return

        # -------------------------------------------------
        # CRIA CONVITE
        # -------------------------------------------------

        try:

            invite = await interaction.channel.create_invite(
                max_age=0,
                max_uses=0,
                unique=True,
                reason=f"Criado por {interaction.user}"
            )

            cog.invite_cache[
                invite.code
            ] = {
                "uses": invite.uses,
                "inviter": user_id
            }

            await interaction.response.send_message(
                f"🔗 | Aqui está o seu convite exclusivo:\n"
                f"`{invite.url}`\n"
                f"(BASTA CLICAR NO NOME PRETO PARA COPIAR)",
                ephemeral=True
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                "❌ | Não consegui criar um convite neste canal. "
                "Certifique-se de que eu tenho permissão para **Criar Convites**.",
                ephemeral=True
            )

        except Exception as e:

            print(
                f"❌ Erro ao criar convite: {e}"
            )

            await interaction.response.send_message(
                "❌ | Não consegui criar o convite.",
                ephemeral=True
            )


# =========================================================
# COG
# =========================================================

class Verification(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.invite_cache = {}

    # =====================================================
    # MONGODB
    # =====================================================

    async def get_user_invites(
        self,
        user_id
    ):

        try:

            data = self.bot.db[
                "verification_invites"
            ].find_one(
                {
                    "user_id": str(user_id)
                }
            )

            if data:

                return data.get(
                    "invites_count",
                    0
                )

        except Exception as e:

            print(
                f"❌ Erro ao buscar convites no MongoDB: {e}"
            )

        return 0

    async def update_user_invites(
        self,
        user_id,
        increment_value
    ):

        try:

            self.bot.db[
                "verification_invites"
            ].update_one(
                {
                    "user_id": str(user_id)
                },
                {
                    "$inc": {
                        "invites_count": increment_value
                    }
                },
                upsert=True
            )

            print(
                f"💾 Banco Atualizado: {user_id} "
                f"modificado em {increment_value} pontos."
            )

        except Exception as e:

            print(
                f"❌ Erro ao atualizar convites no MongoDB: {e}"
            )

    async def get_referred_by(
        self,
        member_id
    ):

        try:

            data = self.bot.db[
                "verification_referrals"
            ].find_one(
                {
                    "member_id": str(member_id)
                }
            )

            if data:

                return data.get(
                    "inviter_id"
                )

        except Exception as e:

            print(
                f"❌ Erro ao buscar indicação no MongoDB: {e}"
            )

        return

    # =========================================================
    # MEMBRO SAIU
    # =========================================================

    @commands.Cog.listener()
    async def on_member_remove(
        self,
        member
    ):

        if member.guild.id != GUILD_ID:
            return

        inviter_id = await self.remove_referred_by(
            member.id
        )

        if inviter_id:

            await self.update_user_invites(
                inviter_id,
                -1
            )

            print(
                f"📉 Membro {member.name} saiu do servidor. "
                f"1 convite removido de {inviter_id}."
            )

    # =========================================================
    # COMANDO SLASH
    # =========================================================

    @app_commands.command(
        name="setup_verificacao",
        description="Envia o painel de verificação no canal configurado."
    )
    @app_commands.default_permissions(
        administrator=True
    )
    async def setup_verificacao(
        self,
        interaction: discord.Interaction
    ):

        if interaction.guild_id != GUILD_ID:

            await interaction.response.send_message(
                "❌ | Este comando não pode ser executado neste servidor.",
                ephemeral=True
            )
            return

        channel = interaction.guild.get_channel(
            CHANNEL_ID
        )

        if not channel:

            await interaction.response.send_message(
                f"❌ | Canal com ID `{CHANNEL_ID}` não foi encontrado.",
                ephemeral=True
            )
            return

        view = VerificationView(
            self.bot
        )

        await channel.send(
            view=view
        )

        await interaction.response.send_message(
            f"✅ | Painel de verificação enviado com sucesso em {channel.mention}!",
            ephemeral=True
        )


# =========================================================
# SETUP
# =========================================================

async def setup(bot):

    await bot.add_cog(
        Verification(bot)
            )
