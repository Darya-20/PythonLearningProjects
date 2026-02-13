from re import sub
from django import template


register = template.Library()


@register.filter()
def censor(text):
    def replacement(match_obj):
        word = match_obj.group(0)
        l = len(word) - 1
        return word[0] + '*' * l
    
    pattern = r'[ЕЁеё]‑мо[её]|[ЕЁеё]лки‑палки|[Бб]лин|[Чч]ертовщин[аыуео]й?'
    text = sub(pattern, replacement, text)
    return f'{text} '

