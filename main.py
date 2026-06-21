import discord
from discord.ext import commands
from discord import ui
import json
import os # 加入這行以讀取環境變數

# 初始設定
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as f: return json.load(f)
    except: return {"currency_name": "代幣", "users": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=4, ensure_ascii=False)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 簽到按鈕視圖
class CheckinView(ui.View):
    def __init__(self):
        super().__init__(timeout=None) # 設置為 None 讓按鈕永久有效

    @ui.button(label="點我簽到領代幣", style=discord.ButtonStyle.green, custom_id="checkin_btn")
    async def checkin(self, interaction: discord.Interaction, button: ui.Button):
        data = load_data()
        # 這裡加入您原本的簽到邏輯 (隨機金額、日期檢查)
        # 記得使用 data["currency_name"] 來顯示貨幣名稱
        await interaction.response.send_message(f"簽到成功！你獲得了獎勵。", ephemeral=True)

    @ui.button(label="查看連續簽到天數", style=discord.ButtonStyle.gray, custom_id="streak_btn")
    async def streak(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("你目前連續簽到 X 天！", ephemeral=True)

# 更改貨幣名稱指令
@bot.command()
@commands.has_permissions(administrator=True)
async def setcurrency(ctx, name: str):
    data = load_data()
    data["currency_name"] = name
    save_data(data)
    await ctx.send(f"貨幣名稱已更改為：{name}")

# 發送簽到面板的指令
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_checkin(ctx):
    embed = discord.Embed(title="📅 每日簽到系統", description="點擊下方按鈕領取獎勵", color=discord.Color.blue())
    await ctx.send(embed=embed, view=CheckinView())

@bot.event
async def on_ready():
    bot.add_view(CheckinView()) # 必須在啟動時註冊 View
    print("機器人已啟動，按鈕已註冊")

# 使用環境變數讀取 Token，避免外洩
bot.run(os.getenv('DISCORD_TOKEN'))
