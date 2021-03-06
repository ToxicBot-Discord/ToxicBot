from functools import partial
from typing import Optional
from discord import Embed


"""
Utils to produce Discord Embed constructs.

You can use the partials `error`, `success` and `info` to apply a style more relevant
to the nature of the message you want to embed, e.g.

error => red border
success => green border
info => blue/your default custom color

Feel free to create others depending on your needs.

You can try them out here:
# https://leovoel.github.io/embed-visualizer/
"""


def as_embed(
    text: str,
    *,
    footer: Optional[str] = None,
    title: Optional[str] = None,
    **kw
) -> Embed:
    """Wrap a string in a stylized discord Embed object."""
    em = Embed(
        type='rich',
        title=title or 'Toxic Bot',
        description=text,
        **kw
    )
    if footer is not None:
        em.set_footer(text=footer)
    return em


error = partial(as_embed, color=0xff041b, title='Error')
info = partial(as_embed, color=0xCA45FF, title='Info')
help = partial(as_embed, color=0xCA45FF, title='Help')
success = partial(as_embed, color=0x6fc12e, title='Success')
