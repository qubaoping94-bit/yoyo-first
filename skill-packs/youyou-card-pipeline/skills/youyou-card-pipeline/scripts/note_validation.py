"""Structural note checks. Editorial truth and tone still require human/agent review."""
import re

HEADINGS = ('推荐标题', '正文内容', '推荐标签', '爆款来源', '合规口径')

def inspect_note(text):
    issues = []
    found = list(re.finditer(r'^### ([^\r\n]+)\s*$', text, re.M))
    names = [m.group(1).strip() for m in found]
    if names != list(HEADINGS):
        return {'ok': False, 'issues': ['Require exactly these five headings in order: '+', '.join(HEADINGS)]}
    blocks = {m.group(1).strip():text[m.end():found[i+1].start() if i+1<len(found) else len(text)].strip() for i,m in enumerate(found)}
    titles = re.findall(r'^([1-5])\.\s+(.+)$', blocks['推荐标题'], re.M)
    if [t[0] for t in titles] != ['1','2','3','4','5'] or len(set(t[1] for t in titles)) != 5:
        issues.append('Require five distinct numbered titles, 1 through 5')
    elif len(blocks['推荐标题'].splitlines()) != 5:
        issues.append('Title section must contain only five title lines')
    body = blocks['正文内容']
    paragraphs = [p for p in re.split(r'\n\s*\n',body) if p.strip()]
    length = len(re.sub(r'\s','',body))
    if not 6<=len(paragraphs)<=8: issues.append('Body requires 6 to 8 paragraphs')
    if not 1<=length<=1000: issues.append(f'Body contains {length} characters; limit is 1000')
    if re.search(r'^(?:#{1,6}\s|\d+[.、]\s*|[-*]\s)',body,re.M):
        issues.append('Body uses paragraphs, not subheadings or numbered/bulleted lists')
    tags = re.findall(r'#[^\s#]+',blocks['推荐标签'])
    if not 6<=len(tags)<=8 or len(set(tags))!=len(tags): issues.append('Require 6 to 8 distinct tags')
    if re.sub(r'#[^\s#]+|\s','',blocks['推荐标签']): issues.append('Tag section must contain only hashtags')
    for name in ('爆款来源','合规口径'):
        if not blocks[name]: issues.append(f'{name} must not be empty')
    return {'ok':not issues,'issues':issues,'body_chars':length,'paragraphs':len(paragraphs),'titles':len(titles),'tags':len(tags)}

def publication_text(text):
    """Called only after inspection succeeds; keep editorial notes out of posting copy."""
    def block(name,next_name):
        return text.split('### '+name,1)[1].split('### '+next_name,1)[0].strip()
    title=block('推荐标题','正文内容').splitlines()[0].split('. ',1)[1]
    return title+'\n\n'+block('正文内容','推荐标签')+'\n\n'+block('推荐标签','爆款来源')+'\n'
