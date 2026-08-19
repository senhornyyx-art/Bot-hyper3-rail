import discord
from discord.ext import commands
from discord import app_commands

# IDs fornecidos
ROLE_ID = 1538708137748594799   # ID do cargo que o usuário ganhará
CHANNEL_ID = 1539108037120229486  # ID do canal onde o painel será enviado
GUILD_ID = 1538601853632118877  # ID DO SERVIDOR ONDE O SISTEMA VAI FUNCIONAR

# URL da imagem que ficará no topo do Container
IMAGE_URL = "https://cdn.discordapp.com/attachments/1538607175004455012/1539405747538890812/UQjECAI.png?ex=6a8632d2&is=6a84e152&hm=aacfad9292ca73220b574db55e6b67707c913196c4b6a8fcc488b80c826b6460&"

# Emojis personalizados
EMOJI_CONVITE = "<:convite:1526352250837143552>"
EMOJI_VERIFY = "<:verify:1526360202197209128>"


class VerificationView(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

        # IMPORTANTE:
        # O accent_color precisa ficar DEPOIS dos argumentos posicionais.
        container = discord.ui.Container(
            discord.ui.MediaGallery(
                discord.MediaGalleryItem(IMAGE_URL)
            ),

            discord.ui.Separator(),

            discord.ui.TextDisplay(
                """## <:topic1:1526287141775343656> <:convite:1526352250837143552> Convide 2 pessoas\n
                > - Convide 2 pessoas usando seu convite. (podem ser editores ou não.) Ao atingir a meta, clique no botão \"Validar verificação\".\n\n"
            ## <:topicopen:1526287216954052719> <:verify:1526360202197209128> Após verificar:\n
            > - 📦 Acesso aos Presets & Project Files (AE & AMZ)\n
            > - 🎬 Recursos de edição: CC's, Packs, Fontes, Overlays, Clipes, Músicas e muito mais recursos premium.\n
            > - 🛠️ Suporte completo para editores.\n
            ## <:topicopen:1526287216954052719> <:__:1526354605028413440> Como ver seus convites:\n
            > - Clique em \"Meus convites\" para ver seu progresso.\n
            > - Clique em \"Criar convite\" para gerar seu próprio link.\n
            -# <:prints:1526358671691612200> Tire suas dúvidas no tópico abaixo. O suporte é voluntário; aguarde sem mencionar a Staff."""
            ),

            discord.ui.Separator(),

            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Validar verificação",
                    style=discord.ButtonStyle.green,
                    custom_id="verify_btn",
                    emoji=discord.PartialEmoji.from_str(EMOJI_VERIFY)
                ),

                discord.ui.Button(
                    label="Meus convites",
                    style=discord.ButtonStyle.blurple,
                    custom_id="my_invites_btn",
                    emoji=discord.PartialEmoji.from_str(EMOJI_CONVITE)
                ),

                discord.ui.Button(
                    label="Criar convite",
                    style=discord.ButtonStyle.gray,
                    custom_id="create_invite_btn",
                    emoji="🔗"
                )
            ),

            # BORDA LATERAL DO CONTAINER
            accent_color=discord.Color.from_str("#3F4147")
        )

        self.add_item(container)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        custom_id = interaction.data.get("custom_id") if interaction.data else None

        if custom_id == "verify_btn":
            await self.verify(interaction)

        elif custom_id == "my_invites_btn":
            await self.my_invites(interaction)

        elif custom_id == "create_invite_btn":
            await self.create_invite(interaction)

        return False

    # =========================================================
    # BOTÃO: VALIDAR VERIFICAÇÃO
    # =========================================================

    async def verify(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        member = interaction.user

        if not guild or guild.id != GUILD_ID:
            await interaction.followup.send(
                "❌ | Este sistema de verificação não funciona neste servidor.",
                ephemeral=True
            )
            return

        role = guild.get_role(ROLE_ID)

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

        cog = self.bot.get_cog("Verification")

        if not cog:
            await interaction.followup.send(
                "❌ | Sistema temporariamente indisponível.",
                ephemeral=True
            )
            return

        invites_count = await cog.get_user_invites(member.id)

        # META: 2 CONVITES
        if invites_count >= 2:
            try:
                await member.add_roles(role)

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

    # =========================================================
    # BOTÃO: MEUS CONVITES
    # =========================================================

    async def my_invites(self, interaction: discord.Interaction):
        if not interaction.guild or interaction.guild.id != GUILD_ID:
            await interaction.response.send_message(
                "❌ | Este sistema de verificação não funciona neste servidor.",
                ephemeral=True
            )
            return

        cog = self.bot.get_cog("Verification")

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

    # =========================================================
    # BOTÃO: CRIAR CONVITE
    # =========================================================

    async def create_invite(self, interaction: discord.Interaction):
        if not interaction.guild or interaction.guild.id != GUILD_ID:
            await interaction.response.send_message(
                "❌ | Este sistema de verificação não funciona neste servidor.",
                ephemeral=True
            )
            return

        cog = self.bot.get_cog("Verification")

        if not cog:
            await interaction.response.send_message(
                f"{EMOJI_CONVITE} | ❌ Sistema temporariamente indisponível.",
                ephemeral=True
            )
            return

        user_id = interaction.user.id

        # =====================================================
        # PRIMEIRO: PROCURA NO CACHE
        # =====================================================

        convite_existente = None

        for code, data in cog.invite_cache.items():
            if data["inviter"] == user_id:
                convite_existente = code
                break

        # =====================================================
        # SEGUNDO: PROCURA DIRETAMENTE NO SERVIDOR
        # =====================================================

        if not convite_existente:
            try:
                invites = await interaction.guild.invites()

                for invite in invites:
                    if invite.inviter and invite.inviter.id == user_id:
                        convite_existente = invite.code

                        cog.invite_cache[invite.code] = {
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

        # =====================================================
        # SE JÁ POSSUI CONVITE, NÃO CRIA OUTRO
        # =====================================================

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

        # =====================================================
        # CRIA NOVO CONVITE
        # =====================================================

        try:
            invite = await interaction.channel.create_invite(
                max_age=0,
                max_uses=0,
                unique=True,
                reason=f"Criado por {interaction.user}"
            )

            cog.invite_cache[invite.code] = {
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


class Verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.invite_cache = {}

    # =========================================================
    # MONGODB
    # =========================================================

    async def get_user_invites(self, user_id):
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

    async def get_referred_by(self, member_id):
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

        return None

    async def set_referred_by(
        self,
        member_id,
        inviter_id
    ):
        try:
            self.bot.db[
                "verification_referrals"
            ].update_one(
                {
                    "member_id": str(member_id)
                },
                {
                    "$set": {
                        "inviter_id": str(inviter_id)
                    }
                },
                upsert=True
            )

            print(
                f"💾 Indicação Registrada: "
                f"Membro {member_id} "
                f"convidado por {inviter_id}"
            )

        except Exception as e:
            print(
                f"❌ Erro ao definir indicação no MongoDB: {e}"
            )

    async def remove_referred_by(self, member_id):
        try:
            data = self.bot.db[
                "verification_referrals"
            ].find_one_and_delete(
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
                f"❌ Erro ao remover indicação no MongoDB: {e}"
            )

        return None

    # =========================================================
    # INICIALIZAÇÃO
    # =========================================================

    async def cog_load(self):
        self.bot.add_view(
            VerificationView(self.bot)
        )

        self.bot.loop.create_task(
            self.load_all_invites()
        )

    async def load_all_invites(self):
        await self.bot.wait_until_ready()

        # SOMENTE O SERVIDOR CONFIGURADO
        guild = self.bot.get_guild(
            GUILD_ID
        )

        if not guild:
            print(
                f"❌ Servidor com ID {GUILD_ID} não encontrado."
            )
            return

        print(
            f"🔄 Carregando convites apenas do servidor: "
            f"{guild.name} ({guild.id})..."
        )

        try:
            invites = await guild.invites()

            for invite in invites:
                if invite.inviter:
                    self.invite_cache[
                        invite.code
                    ] = {
                        "uses": invite.uses,
                        "inviter": invite.inviter.id
                    }

            print(
                f"✅ Cache populado: "
                f"{len(invites)} convites."
            )

        except discord.Forbidden:
            print(
                f"❌ Sem permissão para ler os convites "
                f"do servidor {guild.name}."
            )

        except Exception as e:
            print(
                f"❌ Erro ao carregar convites: {e}"
            )

    # =========================================================
    # READY
    # =========================================================

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.tree.sync()

            print(
                "🚀 [Verification] Comando "
                "/setup_verificacao sincronizado com sucesso!"
            )

        except Exception as e:
            print(
                f"❌ Erro ao sincronizar comandos automaticamente: {e}"
            )

    # =========================================================
    # CONVITE CRIADO
    # =========================================================

    @commands.Cog.listener()
    async def on_invite_create(self, invite):

        # Ignora qualquer outro servidor
        if invite.guild and invite.guild.id != GUILD_ID:
            return

        if invite.inviter:
            self.invite_cache[
                invite.code
            ] = {
                "uses": invite.uses,
                "inviter": invite.inviter.id
            }

    # =========================================================
    # CONVITE DELETADO
    # =========================================================

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):

        if invite.guild and invite.guild.id != GUILD_ID:
            return

        self.invite_cache.pop(
            invite.code,
            None
        )

    # =========================================================
    # MEMBRO ENTROU
    # =========================================================

    @commands.Cog.listener()
    async def on_member_join(self, member):

        # FUNCIONA SOMENTE NO GUILD_ID
        if member.guild.id != GUILD_ID:
            return

        print(
            f"👤 Membro entrou: "
            f"{member.name} ({member.id})"
        )

        try:
            current_invites = await member.guild.invites()

            for invite in current_invites:

                cached = self.invite_cache.get(
                    invite.code
                )

                if cached and invite.uses > cached["uses"]:

                    inviter_id = str(
                        cached["inviter"]
                    )

                    member_id = str(
                        member.id
                    )

                    # Impede auto-convite
                    if inviter_id == member_id:
                        print(
                            f"⚠️ {member.name} tentou entrar "
                            f"usando o próprio convite. Ignorando."
                        )

                        self.invite_cache[
                            invite.code
                        ]["uses"] = invite.uses

                        break

                    # =================================================
                    # IMPOSSIBILITA CONTABILIZAR O MESMO MEMBRO 2X
                    # =================================================

                    ja_indicado = await self.get_referred_by(
                        member_id
                    )

                    if ja_indicado:
                        print(
                            f"⚠️ {member.name} já possui uma "
                            f"indicação registrada. Ignorando duplicação."
                        )

                        self.invite_cache[
                            invite.code
                        ]["uses"] = invite.uses

                        break

                    print(
                        f"🎉 Convite correspondido! "
                        f"{member.name} entrou usando "
                        f"o convite de {inviter_id}."
                    )

                    # Salva quem convidou
                    await self.set_referred_by(
                        member_id,
                        inviter_id
                    )

                    # Adiciona 1 convite ao convidador
                    await self.update_user_invites(
                        inviter_id,
                        1
                    )

                    self.invite_cache[
                        invite.code
                    ]["uses"] = invite.uses

                    break

        except discord.Forbidden:
            print(
                f"❌ Sem permissão para ler convites no evento de entrada de {member.name}."
            )
        except Exception as e:
            print(
                f"❌ Erro no processamento do evento on_member_join: {e}"
            )

    # =========================================================
    # MEMBRO SAIU
    # =========================================================

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if member.guild.id != GUILD_ID:
            return

        inviter_id = await self.remove_referred_by(member.id)

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
    # COMANDO SLASH: /setup_verificacao
    # =========================================================

    @app_commands.command(
        name="setup_verificacao",
        description="Envia o painel de verificação no canal configurado."
    )
    @app_commands.default_permissions(administrator=True)
    async def setup_verificacao(self, interaction: discord.Interaction):
        if interaction.guild_id != GUILD_ID:
            await interaction.response.send_message(
                "❌ | Este comando não pode ser executado neste servidor.",
                ephemeral=True
            )
            return

        channel = interaction.guild.get_channel(CHANNEL_ID)

        if not channel:
            await interaction.response.send_message(
                f"❌ | Canal com ID `{CHANNEL_ID}` não foi encontrado.",
                ephemeral=True
            )
            return

        view = VerificationView(self.bot)
        await channel.send(view=view)

        await interaction.response.send_message(
            f"✅ | Painel de verificação enviado com sucesso em {channel.mention}!",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Verification(bot))
