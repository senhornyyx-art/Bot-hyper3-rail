import discord
from discord.ext import commands
from discord import app_commands
import time

# =========================================================
# CONFIGURAÇÕES
# =========================================================

ROLE_ID = 1538708137748594799
CHANNEL_ID = 1539108037120229486
GUILD_ID = 1538601853632118877

# ID DO TÓPICO
THREAD_ID = 1539497894816514120

IMAGE_URL = "https://cdn.discordapp.com/attachments/1538601853632118877/1539405747538890812/UQjECAI.png?ex=6a8632d2&is=6a84e152&hm=aacfad9292ca73220b574db55e6b67707c913196c4b6a8fcc488b80c826b6460&"

EMOJI_CONVITE = "<:convite:1526352250837143552>"
EMOJI_VERIFY = "<:verify:1526360202197209128>"

ENGLISH_BUTTON_ID = "english_verification_btn"

# =========================================================
# COOLDOWN DO BOTÃO ENGLISH
# 2 HORAS
# =========================================================

ENGLISH_COOLDOWN = 2 * 60 * 60

english_cooldowns = {}


# =========================================================
# TEXTO PORTUGUÊS
# =========================================================

PORTUGUESE_TEXT = """# <:topic1:1526287141775343656> <:convite:1526352250837143552> Convide 2 pessoas
> - Convide 2 pessoas usando seu convite e quando atingir a meta, clique em "Validar verificação".
# <:topicopen:1526287216954052719> <:verify:1526360202197209128> Benefícios:
> - 🎁 Presets, Project Files & softwares (After Effects, Alight Motion, After Motion Z)
> - 💻 CC's, Packs, Fontes, Overlays, Clipes, Músicas e muito mais recursos de edição em todos os estilos.
> - ⭐ Suporte e canal de dúvidas para editores.
# <:topicopen:1526287216954052719> <:__:1526354605028413440> Como ver seus convites:
> - Clique em "Meus convites" para acompanhar seu progresso. Observação: para validar a pessoa precisa entrar no servidor.
> - Clique em "Criar convite" para gerar seu link de convite e enviar para duas pessoas.
-# <:prints:1526358671691612200> Dúvidas ou problemas com a verificação? Anexe prints como provas, ou tire sua dúvida no tópico abaixo. O suporte é voluntáriado, então aguarde com paciência."""


# =========================================================
# TEXTO INGLÊS DO PAINEL
# =========================================================

ENGLISH_TEXT = """# <:topic1:1526287141775343656> <:convite:1526352250837143552> Invite 2 people
> - Invite 2 people using your invite and once you reach the goal, click "Verify".
# <:topicopen:1526287216954052719> <:verify:1526360202197209128> Benefits:
> - 🎁 Presets, Project Files & software (After Effects, Alight Motion, After Motion Z)
> - 💻 CC's, Packs, Fonts, Overlays, Clips, Music and many more editing resources in all styles.
> - ⭐ Support and a help channel for editors.
# <:topicopen:1526287216954052719> <:__:1526354605028413440> How to check your invites:
> - Click "My Invites" to check your progress. Note: the person must join the server for the invite to be validated.
> - Click "Create Invite" to generate your invite link and send it to two people.
-# <:prints:1526358671691612200> Questions or problems with verification? Attach screenshots as proof or ask your question in the thread below. Support is voluntary, so please be patient and wait."""


# =========================================================
# TEXTO ENVIADO NO TÓPICO
# =========================================================

ENGLISH_THREAD_TEXT = """## <:book:1539496360061968484> **・ Use this thread correctly:**
* **Use this thread** to **ask questions, comment or discuss** the invite system.
* **The invited person must join** the server for the invite to be validated during verification.
* **Avoid messages unrelated to the topic** to keep the thread organized."""


# =========================================================
# VIEW DO PAINEL
# =========================================================

class VerificationView(discord.ui.LayoutView):

    def __init__(
        self,
        bot: commands.Bot
    ):
        super().__init__(
            timeout=None
        )

        self.bot = bot

        container = discord.ui.Container(

            discord.ui.MediaGallery(
                discord.MediaGalleryItem(
                    IMAGE_URL
                )
            ),

            discord.ui.Separator(),

            discord.ui.TextDisplay(
                PORTUGUESE_TEXT
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

        self.add_item(
            container
        )

    # =====================================================
    # INTERACTION CHECK
    # =====================================================

    async def interaction_check(
        self,
        interaction: discord.Interaction
    ) -> bool:

        custom_id = (
            interaction.data.get(
                "custom_id"
            )
            if interaction.data
            else None
        )

        if custom_id == "verify_btn":

            await self.verify(
                interaction
            )

        elif custom_id == "my_invites_btn":

            await self.my_invites(
                interaction
            )

        elif custom_id == "create_invite_btn":

            await self.create_invite(
                interaction
            )

        elif custom_id == ENGLISH_BUTTON_ID:

            await self.english_instructions(
                interaction
            )

        return False

    # =====================================================
    # ENGLISH INSTRUCTIONS
    # =====================================================

    async def english_instructions(
        self,
        interaction: discord.Interaction
    ):

        user = interaction.user
        user_id = user.id

        agora = time.monotonic()

        ultimo_clique = english_cooldowns.get(
            user_id,
            0
        )

        # =================================================
        # COOLDOWN DE 2 HORAS
        # =================================================

        if agora - ultimo_clique < ENGLISH_COOLDOWN:

            restante = (
                ENGLISH_COOLDOWN
                - (
                    agora
                    - ultimo_clique
                )
            )

            horas = int(
                restante // 3600
            )

            minutos = int(
                (
                    restante % 3600
                ) // 60
            )

            segundos = int(
                restante % 60
            )

            if horas > 0:

                tempo = f"{horas}h"

                if minutos:
                    tempo += (
                        f" {minutos}min"
                    )

            elif minutos > 0:

                tempo = (
                    f"{minutos}min"
                )

                if segundos:
                    tempo += (
                        f" {segundos}s"
                    )

            else:

                tempo = (
                    f"{segundos}s"
                )

            await interaction.response.send_message(
                (
                    "⏳ | You need to wait "
                    f"**{tempo}** before requesting "
                    "the instructions again."
                ),
                ephemeral=True
            )

            return

        # =================================================
        # REGISTRA O CLIQUE
        # =================================================

        english_cooldowns[user_id] = agora

        await interaction.response.defer(
            ephemeral=True
        )

        try:

            # =================================================
            # BUSCA O TÓPICO
            # =================================================

            thread = self.bot.get_channel(
                THREAD_ID
            )

            if not thread:

                try:

                    thread = await self.bot.fetch_channel(
                        THREAD_ID
                    )

                except Exception as e:

                    print(
                        "❌ Não foi possível encontrar "
                        f"o tópico: {e}"
                    )

                    english_cooldowns.pop(
                        user_id,
                        None
                    )

                    await interaction.followup.send(
                        (
                            "❌ | I couldn't find "
                            "the instructions thread."
                        ),
                        ephemeral=True
                    )

                    return

            # =================================================
            # CONFIRMA SE É UM TÓPICO
            # =================================================

            if not isinstance(
                thread,
                discord.Thread
            ):

                print(
                    "❌ O THREAD_ID configurado "
                    "não corresponde a um tópico."
                )

                english_cooldowns.pop(
                    user_id,
                    None
                )

                await interaction.followup.send(
                    (
                        "❌ | The configured "
                        "instructions channel is "
                        "not a thread."
                    ),
                    ephemeral=True
                )

                return

            # =================================================
            # 1 — MANDA A MENÇÃO SEPARADAMENTE
            # =================================================

            await thread.send(
                user.mention
            )

            # =================================================
            # 2 — MONTA A MENSAGEM DO TÓPICO
            #
            # O REQUESTED BY JÁ NASCE NA MENSAGEM.
            # NÃO É EDITADO DEPOIS.
            # =================================================

            mensagem_ingles = (
                ENGLISH_THREAD_TEXT
                + "\n"
                + f"-# Requested by: {user.name}"
            )

            # =================================================
            # 3 — ENVIA AS INSTRUÇÕES NO TÓPICO
            # =================================================

            await thread.send(
                mensagem_ingles
            )

            # =================================================
            # 4 — INSTRUÇÕES EM EPHEMERAL
            # =================================================

            english_container = discord.ui.Container(

                discord.ui.TextDisplay(
                    ENGLISH_TEXT
                ),

                accent_color=discord.Color.from_str(
                    "#3F4147"
                )
            )

            english_view = discord.ui.LayoutView(
                timeout=None
            )

            english_view.add_item(
                english_container
            )

            await interaction.followup.send(
                view=english_view,
                ephemeral=True
            )

        except discord.Forbidden:

            english_cooldowns.pop(
                user_id,
                None
            )

            await interaction.followup.send(
                (
                    "❌ | I don't have permission "
                    "to send messages in this thread."
                ),
                ephemeral=True
            )

        except Exception as e:

            english_cooldowns.pop(
                user_id,
                None
            )

            print(
                "❌ Erro no botão "
                f"English Instructions: {e}"
            )

            await interaction.followup.send(
                (
                    "❌ | I couldn't send "
                    "the instructions."
                ),
                ephemeral=True
            )

    # =====================================================
    # VALIDAR VERIFICAÇÃO
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

        if (
            not guild
            or guild.id != GUILD_ID
        ):

            await interaction.followup.send(
                (
                    "❌ | Este sistema de "
                    "verificação não funciona "
                    "neste servidor."
                ),
                ephemeral=True
            )

            return

        role = guild.get_role(
            ROLE_ID
        )

        if not role:

            await interaction.followup.send(
                (
                    "❌ | O cargo de verificação "
                    "não foi encontrado. "
                    "Contate um administrador."
                ),
                ephemeral=True
            )

            return

        if role in member.roles:

            await interaction.followup.send(
                (
                    f"{EMOJI_VERIFY} | Você já está "
                    "verificado e possui o cargo!"
                ),
                ephemeral=True
            )

            return

        cog = self.bot.get_cog(
            "Verification"
        )

        if not cog:

            await interaction.followup.send(
                (
                    "❌ | Sistema temporariamente "
                    "indisponível."
                ),
                ephemeral=True
            )

            return

        invites_count = (
            await cog.get_user_invites(
                member.id
            )
        )

        if invites_count >= 2:

            try:

                await member.add_roles(
                    role
                )

                await interaction.followup.send(
                    (
                        f"{EMOJI_VERIFY} | "
                        "**Verificação concluída!** "
                        f"Você convidou "
                        f"{invites_count} pessoas "
                        f"e recebeu o cargo "
                        f"**{role.name}**."
                    ),
                    ephemeral=True
                )

            except discord.Forbidden:

                await interaction.followup.send(
                    (
                        "❌ | Eu não tenho "
                        "permissão para gerenciar "
                        "cargos. Verifique se meu "
                        "cargo está acima do cargo "
                        "de verificação na lista "
                        "de cargos."
                    ),
                    ephemeral=True
                )

        else:

            await interaction.followup.send(
                (
                    "❌ | Você precisa de "
                    "2 convites. No momento, "
                    f"você tem apenas "
                    f"**{invites_count}/2** "
                    "convites validados."
                ),
                ephemeral=True
            )

    # =====================================================
    # MEUS CONVITES
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
                (
                    "❌ | Este sistema de "
                    "verificação não funciona "
                    "neste servidor."
                ),
                ephemeral=True
            )

            return

        cog = self.bot.get_cog(
            "Verification"
        )

        if not cog:

            await interaction.response.send_message(
                (
                    "❌ | Sistema temporariamente "
                    "indisponível."
                ),
                ephemeral=True
            )

            return

        invites_count = (
            await cog.get_user_invites(
                interaction.user.id
            )
        )

        await interaction.response.send_message(
            (
                f"{EMOJI_CONVITE} | Você possui "
                f"atualmente **{invites_count}** "
                "convites validados."
            ),
            ephemeral=True
        )

    # =====================================================
    # CRIAR CONVITE
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
                (
                    "❌ | Este sistema de "
                    "verificação não funciona "
                    "neste servidor."
                ),
                ephemeral=True
            )

            return

        cog = self.bot.get_cog(
            "Verification"
        )

        if not cog:

            await interaction.response.send_message(
                (
                    f"{EMOJI_CONVITE} | ❌ "
                    "Sistema temporariamente "
                    "indisponível."
                ),
                ephemeral=True
            )

            return

        user_id = interaction.user.id

        convite_existente = None

        # =================================================
        # PROCURA NO CACHE
        # =================================================

        for code, data in (
            cog.invite_cache.items()
        ):

            if data["inviter"] == user_id:

                convite_existente = code

                break

        # =================================================
        # PROCURA NO SERVIDOR
        # =================================================

        if not convite_existente:

            try:

                invites = (
                    await interaction.guild.invites()
                )

                for invite in invites:

                    if (
                        invite.inviter
                        and invite.inviter.id
                        == user_id
                    ):

                        convite_existente = (
                            invite.code
                        )

                        cog.invite_cache[
                            invite.code
                        ] = {
                            "uses": invite.uses,
                            "inviter": user_id
          }

                        break

            except discord.Forbidden:

                await interaction.response.send_message(
                    (
                        "❌ | Não consigo verificar "
                        "seus convites existentes. "
                        "Preciso da permissão "
                        "**Gerenciar Servidor**."
                    ),
                    ephemeral=True
                )

                return

            except Exception as e:

                print(
                    "❌ Erro ao verificar "
                    f"convites existentes: {e}"
                )

        # =================================================
        # JÁ POSSUI CONVITE
        # =================================================

        if convite_existente:

            await interaction.response.send_message(
                content=(
                    "⚠️ | Você já possui "
                    "um convite criado! "
                    "Use o seu link:\n"
                    f"`https://discord.gg/"
                    f"{convite_existente}`\n"
                    "(BASTA CLICAR NO NOME "
                    "PRETO PARA COPIAR)"
                ),
                ephemeral=True
            )

            return

        # =================================================
        # CRIA NOVO CONVITE
        # =================================================

        try:

            invite = (
                await interaction.channel.create_invite(
                    max_age=0,
                    max_uses=0,
                    unique=True,
                    reason=(
                        f"Criado por "
                        f"{interaction.user}"
                    )
                )
            )

            cog.invite_cache[
                invite.code
            ] = {
                "uses": invite.uses,
                "inviter": user_id
            }

            await interaction.response.send_message(
                (
                    "🔗 | Aqui está o seu "
                    "convite exclusivo:\n"
                    f"`{invite.url}`\n"
                    "(BASTA CLICAR NO NOME "
                    "PRETO PARA COPIAR)"
                ),
                ephemeral=True
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                (
                    "❌ | Não consegui criar "
                    "um convite neste canal. "
                    "Certifique-se de que eu "
                    "tenho permissão para "
                    "**Criar Convites**."
                ),
                ephemeral=True
            )

        except Exception as e:

            print(
                f"❌ Erro ao criar convite: {e}"
            )

            await interaction.response.send_message(
                (
                    "❌ | Não consegui "
                    "criar o convite."
                ),
                ephemeral=True
)

# =========================================================
# COG
# =========================================================

class Verification(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot

        # =================================================
        # CACHE DOS CONVITES DO SERVIDOR
        # =================================================

        self.invite_cache = {}

    # =====================================================
    # MONGODB — BUSCAR CONVITES
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
                "❌ Erro ao buscar convites "
                f"no MongoDB: {e}"
            )

        return 0

    # =====================================================
    # MONGODB — ATUALIZAR CONVITES
    # =====================================================

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
                "❌ Erro ao atualizar convites "
                f"no MongoDB: {e}"
            )

    # =====================================================
    # BUSCAR INDICAÇÃO
    # =====================================================

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
                "❌ Erro ao buscar indicação "
                f"no MongoDB: {e}"
            )

        return None

    # =====================================================
    # SALVAR INDICAÇÃO
    # =====================================================

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
                "💾 Indicação Registrada: "
                f"Membro {member_id} "
                f"convidado por {inviter_id}"
            )

        except Exception as e:

            print(
                "❌ Erro ao definir indicação "
                f"no MongoDB: {e}"
            )

    # =====================================================
    # REMOVER INDICAÇÃO
    # =====================================================

    async def remove_referred_by(
        self,
        member_id
    ):

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
                "❌ Erro ao remover indicação "
                f"no MongoDB: {e}"
            )

        return None

    # =====================================================
    # INICIALIZAÇÃO DA COG
    # =====================================================

    async def cog_load(
        self
    ):

        # =================================================
        # REGISTRA A VIEW COMO PERSISTENTE
        # =================================================

        self.bot.add_view(
            VerificationView(
                self.bot
            )
        )

        # =================================================
        # CARREGA OS CONVITES DO SERVIDOR
        # =================================================

        self.bot.loop.create_task(
            self.load_all_invites()
        )

    # =====================================================
    # CARREGAR CONVITES DO SERVIDOR
    # =====================================================

    async def load_all_invites(
        self
    ):

        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(
            GUILD_ID
        )

        if not guild:

            print(
                f"❌ Servidor com ID "
                f"{GUILD_ID} não encontrado."
            )

            return

        print(
            "🔄 Carregando convites apenas "
            f"do servidor: {guild.name} "
            f"({guild.id})..."
        )

        try:

            invites = await guild.invites()

            self.invite_cache.clear()

            for invite in invites:

                if invite.inviter:

                    self.invite_cache[
                        invite.code
                    ] = {
                        "uses": invite.uses,
                        "inviter": invite.inviter.id
                    }

            print(
                "✅ Cache populado: "
                f"{len(invites)} convites."
            )

        except discord.Forbidden:

            print(
                "❌ Sem permissão para ler "
                f"os convites do servidor "
                f"{guild.name}."
            )

        except Exception as e:

            print(
                f"❌ Erro ao carregar convites: {e}"
            )

    # =====================================================
    # READY
    # =====================================================

    @commands.Cog.listener()
    async def on_ready(
        self
    ):

        try:

            await self.bot.tree.sync()

            print(
                "🚀 [Verification] Comando "
                "/setup_verificacao "
                "sincronizado com sucesso!"
            )

        except Exception as e:

            print(
                "❌ Erro ao sincronizar "
                f"comandos automaticamente: {e}"
            )

    # =====================================================
    # CONVITE CRIADO
    # =====================================================

    @commands.Cog.listener()
    async def on_invite_create(
        self,
        invite
    ):

        if (
            invite.guild
            and invite.guild.id != GUILD_ID
        ):

            return

        if invite.inviter:

            self.invite_cache[
                invite.code
            ] = {
                "uses": invite.uses,
                "inviter": invite.inviter.id
            }

            print(
                "🔗 Novo convite registrado: "
                f"{invite.code} "
                f"→ {invite.inviter}"
            )

    # =====================================================
    # CONVITE DELETADO
    # =====================================================

    @commands.Cog.listener()
    async def on_invite_delete(
        self,
        invite
    ):

        if (
            invite.guild
            and invite.guild.id != GUILD_ID
        ):

            return

        self.invite_cache.pop(
            invite.code,
            None
        )

        print(
            f"🗑️ Convite removido do cache: "
            f"{invite.code}"
        )

    # =====================================================
    # MEMBRO ENTROU
    # =====================================================

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member
    ):

        if member.guild.id != GUILD_ID:

            return

        print(
            "👤 Membro entrou: "
            f"{member.name} ({member.id})"
        )

        try:

            # =================================================
            # BUSCA OS CONVITES ATUAIS
            # =================================================

            current_invites = (
                await member.guild.invites()
            )

            # =================================================
            # PROCURA QUAL CONVITE AUMENTOU
            # =================================================

            for invite in current_invites:

                cached = (
                    self.invite_cache.get(
                        invite.code
                    )
                )

                if not cached:

                    # Convite que apareceu depois
                    # do último carregamento.
                    if invite.inviter:

                        self.invite_cache[
                            invite.code
                        ] = {
                            "uses": invite.uses,
                            "inviter": (
                                invite.inviter.id
                            )
                        }

                    continue

                # =================================================
                # DETECTA AUMENTO DE USOS
                # =================================================

                if invite.uses <= cached["uses"]:

                    continue

                inviter_id = str(
                    cached["inviter"]
                )

                member_id = str(
                    member.id
                )

                # =================================================
                # ATUALIZA PRIMEIRO O CACHE
                # =================================================

                self.invite_cache[
                    invite.code
                ]["uses"] = invite.uses

                # =================================================
                # IMPEDE AUTO-CONVITE
                # =================================================

                if inviter_id == member_id:

                    print(
                        f"⚠️ {member.name} tentou "
                        "entrar usando o próprio "
                        "convite. Ignorando."
                    )

                    break

                # =================================================
                # VERIFICA SE JÁ POSSUI INDICAÇÃO
                # =================================================

                ja_indicado = (
                    await self.get_referred_by(
                        member_id
                    )
                )

                if ja_indicado:

                    print(
                        f"⚠️ {member.name} já possui "
                        "uma indicação registrada. "
                        "Ignorando duplicação."
                    )

                    break

                # =================================================
                # CONVITE ENCONTRADO
                # =================================================

                print(
                    "🎉 Convite correspondido! "
                    f"{member.name} entrou usando "
                    f"o convite de {inviter_id}."
                )

                # =================================================
                # SALVA A INDICAÇÃO
                # =================================================

                await self.set_referred_by(
                    member_id,
                    inviter_id
                )

                # =================================================
                # ADICIONA 1 CONVITE AO USUÁRIO
                # =================================================

                await self.update_user_invites(
                    inviter_id,
                    1
                )

                break

        except discord.Forbidden:

            print(
                "❌ Sem permissão para ler "
                "convites no evento de entrada "
                f"de {member.name}."
            )

        except Exception as e:

            print(
                "❌ Erro no processamento do "
                f"evento on_member_join: {e}"
            )

    # =====================================================
    # MEMBRO SAIU
    # =====================================================

    @commands.Cog.listener()
    async def on_member_remove(
        self,
        member
    ):

        if member.guild.id != GUILD_ID:

            return

        inviter_id = (
            await self.remove_referred_by(
                member.id
            )
        )

        if inviter_id:

            await self.update_user_invites(
                inviter_id,
                -1
            )

            print(
                f"📉 Membro {member.name} "
                "saiu do servidor. "
                f"1 convite removido de "
                f"{inviter_id}."
            )

    # =====================================================
    # /SETUP_VERIFICACAO
    # =====================================================

    @app_commands.command(
        name="setup_verificacao",
        description=(
            "Envia o painel de verificação "
            "no canal configurado."
        )
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
                (
                    "❌ | Este comando não pode "
                    "ser executado neste servidor."
                ),
                ephemeral=True
            )

            return

        channel = (
            interaction.guild.get_channel(
                CHANNEL_ID
            )
        )

        if not channel:

            await interaction.response.send_message(
                (
                    f"❌ | Canal com ID "
                    f"`{CHANNEL_ID}` não foi "
                    "encontrado."
                ),
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
            (
                "✅ | Painel de verificação "
                "enviado com sucesso em "
                f"{channel.mention}!"
            ),
            ephemeral=True
    )

# =========================================================
# SETUP DA COG
# =========================================================

async def setup(
    bot
):

    await bot.add_cog(
        Verification(
            bot
        )
        )
