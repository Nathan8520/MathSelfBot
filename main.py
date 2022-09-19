import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests

bot = commands.Bot(">", self_bot=True)


@bot.event
async def on_ready():
    print("Bot ready")


@bot.command()
async def exe(ctx, *args):
    try:
        output = []
        exec(
            f'async def __ex(ctx, OUT): ' +
            ''.join(f'\n {l.replace("print", "OUT.append")}' for l in args[0][:-3].split('\n')[1:])
        )
        await locals()['__ex'](ctx, output)

        if len(output) > 0:
            await ctx.channel.send("```\n{}\n```".format("\n".join([str(x) for x in output])))

    except Exception as e:
        await ctx.channel.send("```\n{}\n```".format(e))


@bot.command()
async def tex(ctx: Context, *args):
    data = "".join(args)
    image = requests.request(method="GET", url="https://latex.codecogs.com/png.latex?{\color{white} " + data + "}")

    file = open("image.png", "wb")
    file.write(image.content)
    file.close()

    if ctx.reference == None:
        await ctx.channel.send(file=discord.File("image.png"))
    else:
        await ctx.channel.send(file=discord.File("image.png"), reference=ctx.reference)

    await ctx.delete()


@bot.event
async def on_message(message):
    if message.author.id != 592409615568863232:
        return

    if message.content.startswith(">tex"):
        await tex(message, message.content[4:])
        return
    if message.content.startswith(">exe"):
        await exe(message, message.content[4:])
        return

    if not message.content.startswith("|"):
        content = message.content
        # ℝ ℚ ℕ ℤ
        replace = {"in": "∈",
                   "notin": "∉",
                   "R": "ℝ",
                   "Q": "ℚ",
                   "N": "ℕ",
                   "Z": "ℤ",
                   "C": "ℂ",
                   "empty": "Ø",
                   "forall": "∀",
                   "exists": "∃",
                   "notexists": "∄",
                   "alpha": "α",
                   "beta": "β",
                   "Gamma": "Γ",
                   "delta": "δ",
                   "Delta": "Δ",
                   "epsilon": "ε",
                   "zeta": "ζ",
                   "theta": "θ",
                   "lambda": "λ",
                   "mu": "μ",
                   "pi": "π",
                   "Pi": "∏",
                   "Sigma": "Σ",
                   "sigma": "σ",
                   "phi": "φ",
                   "Phi": "Φ",
                   "psi": "ψ",
                   "Psi": "Ψ",
                   "omega": "ω",
                   "Omega": "Ω",
                   "nabla": "∇",
                   "partial": "∂",
                   "implies": "⇒",
                   "iff": "⇔",
                   "not": "¬",
                   "intersect": "⋂",
                   "union": "⋃",
                   "subset": "⊆",
                   "propersubset": "⊂",
                   "notsubset": "⊄",
                   "neq": "≠",
                   "approx": "≈",
                   "ge": "≥",
                   "le": "≤",
                   "pm": "±",
                   "mp": "±",
                   "cdot": "⋅",
                   "div": "÷",
                   "degree": "°",
                   "perp": "⊥",
                   "parallel": "∥",
                   "eq": "≡",
                   "infty": "∞",
                   "and": "∧",
                   "or": "∨",
                   "xor": "⊕",
                   "therefore": "∴",
                   "because": "∵",
                   "int": "∫",
                   "dint": "∫∫",
                   "tint": "∫∫∫",
                   "lineint": "∮",
                   "surfaceint": "∯",
                   "volumeint": "∰",
                   "function": "↦",
                   "^0": "⁰",
                   "^1": "¹",
                   "^2": "²",
                   "^3": "³",
                   "^4": "⁴",
                   "^5": "⁵",
                   "^6": "⁶",
                   "^7": "⁷",
                   "^8": "⁸",
                   "^9": "⁹",
                   "^+": "⁺",
                   "^-": "⁻",
                   "^=": "⁼",
                   "^(": "⁽",
                   "^)": "⁾",
                   "_0": "₀",
                   "_1": "₁",
                   "_2": "₂",
                   "_3": "₃",
                   "_4": "₄",
                   "_5": "₅",
                   "_6": "₆",
                   "_7": "₇",
                   "_8": "₈",
                   "_9": "₉",
                   "_+": "₊",
                   "_-": "₋",
                   "_=": "₌",
                   "_(": "₍",
                   "_)": "₎",
                   "^alpha": "ᵅ",
                   "^beta": "ᵝ",
                   "_beta": "ᵦ",
                   "_x": "ₓ",
                   "_i": "ᵢ",
                   "_j": "ⱼ",
                   "_k": "ₖ",
                   "^y": "ʸ",
                   "cross": "⨯"
                   }

        for key, val in reversed(sorted(replace.items())):
            if key[0] in ["^", "_"]:
                content = content.replace(key, val)
            else:
                content = content.replace("\\" + key, val)
                content = content.replace("/" + key, val)

        if content != message.content:
            await message.edit(content=content)


bot.run("INSERT TOKEN HERE", bot=False)