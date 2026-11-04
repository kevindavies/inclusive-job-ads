import sys,re,subprocess,os
src,dst,still=sys.argv[1:]
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'checker', 'wordlists.py'), src], check=True)
s=open(src).read()
here=os.path.dirname(os.path.abspath(__file__))

def region(s, drop):
    """Remove <!--NAME-->...<!--/NAME--> blocks for each name in drop, and the remaining markers."""
    for name in drop:
        s=re.sub(r'<!--%s-->.*?<!--/%s-->\n?' % (name, name), '', s, flags=re.S)
    return re.sub(r'<!--/?(MAIN|CHECKHEAD|CHECK|TEASER)-->\n?', '', s)

full=s
s=region(full, ['CHECKHEAD', 'CHECK'])
chk=region(full, ['MAIN', 'TEASER'])
chk=chk.replace('<title>inclusive-job-ads</title>', '<title>Check a job ad</title>', 1)
chk=chk.replace('<h1>inclusive-job-ads</h1>', '<h1><a href="../">inclusive-job-ads</a></h1>', 1)
s=s.replace(' data-nav="main"', ' aria-current="page"').replace(' data-nav="check"', '')
chk=chk.replace(' data-nav="check"', ' aria-current="page"').replace(' data-nav="main"', '')
s=s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
def page(s, head):
    i=s.index('<style>'); m=s.index('<main')
    out=head+s[:i]+s[i:m].replace('</style>','</style>\n</head>\n<body>',1)+s[m:].rstrip()+'\n</body>\n</html>\n'
    return out.replace('body {\n  background: var(--desk);','body {\n  margin: 0;\n  background: var(--desk);',1)

head='''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Guidelines for writing and reviewing job ads that welcome everyone who could do the job, with tools for Claude, ChatGPT, Gemini and Copilot. Free and open source.">
<meta property="og:title" content="inclusive-job-ads">
<meta property="og:description" content="Guidelines for writing and reviewing job ads that welcome everyone who could do the job.">
<meta property="og:image" content="https://inclusive-job-ads.beaks.co/og.png">
<meta property="og:url" content="https://inclusive-job-ads.beaks.co/">
<meta name="twitter:card" content="summary_large_image">
'''
out=page(s, head)
open(dst,'w').write(out)
chead=(head.replace('content="Guidelines for writing and reviewing job ads that welcome everyone who could do the job, with tools for Claude, ChatGPT, Gemini and Copilot. Free and open source."','content="Paste a job ad and check it against seven evidence-based guidelines. It runs in your browser, so your ad isn’t sent anywhere."')
  .replace('<meta property="og:title" content="inclusive-job-ads">','<meta property="og:title" content="Check a job ad">')
  .replace('content="Guidelines for writing and reviewing job ads that welcome everyone who could do the job."','content="Paste a job ad and check it against seven evidence-based guidelines."')
  .replace('https://inclusive-job-ads.beaks.co/">','https://inclusive-job-ads.beaks.co/check/">'))
assert chead.count('check/')==1 and 'Check a job ad' in chead
cdst=os.path.join(os.path.dirname(dst), 'check', 'index.html')
os.makedirs(os.path.dirname(cdst), exist_ok=True)
open(cdst,'w').write(page(chk, chead))
st=re.sub(r'<script>.*?</script>','',out,flags=re.S).replace('<html lang="en-GB">','<html lang="en-GB" data-theme="dark">')
st=st.replace('</style>','''.site-head, .lede-block, .sec, footer, .replay-row { display: none !important; }
html, body { height: 100%; }
.wrap { min-height: 100%; box-sizing: border-box; padding-block: 2rem; align-content: center; max-width: 56rem; }
.proof-row { grid-template-columns: minmax(0, 1fr) 8rem; }
.ad { font-size: 1.4rem; }
.note { top: 11rem; }
</style>''',1)
open(still,'w').write(st)
