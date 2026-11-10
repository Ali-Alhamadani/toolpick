import base64,re
b=open('build.py').read()
enc=base64.b64encode(open('v67_history.py','rb').read()).decode()
b2=re.sub(r'(/ "v67_history.py"\)\.write_bytes\(_v67b64\.b64decode\(")[^"]*(")', lambda m: m.group(1)+enc+m.group(2), b, count=1)
assert b2!=b or enc in b
open('build.py','w').write(b2); print("embedded", len(enc))
