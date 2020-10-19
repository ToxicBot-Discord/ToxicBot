from discord import Embed


def as_embed(text: str) -> Embed:
    return Embed(
        title='ToxixBot says',
        description=text
    )
