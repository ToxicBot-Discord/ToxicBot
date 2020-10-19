from functools import partial
from typing import Optional
from discord import Embed


def as_embed(
    text: str,
    *,
    footer: Optional[str] = None,
    title: Optional[str] = None,
    **kw
) -> Embed:
    if title is None:
        title = 'Toxic Bot Message'
    em = Embed(
        type='rich',
        title=title,
        description=text,
        **kw
    )
    em.set_author(name='Toxic Bot')
    if footer is not None:
        em.set_footer(text=footer)
    return em


error = partial(as_embed, color=0xff0000, title='Oops!')
warning = partial(as_embed, color=0xffff00, title='Beware ...')
info = partial(as_embed, color=0x0000ff, title='Just so you know')
yes = partial(as_embed, color=0x00ff00, title='You did it!')
