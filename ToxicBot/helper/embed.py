from functools import partial
from discord import Embed


def as_embed(text: str, **kw) -> Embed:
    return Embed(
        type='rich',
        title='ToxicBot says',
        description=text,
        **kw
    )


error   = partial(as_embed, color=0xff0000)
warning = partial(as_embed, color=0xffff00)
info    = partial(as_embed, color=0x0000ff)
