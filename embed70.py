"""Re-embed feature modules (base64) into build.py: v66_picker.py, v67_history.py, v68_alternatives.py, v69_checker.py, v70_yearly.py."""
import base64, re
b = open('build.py').read()
for mod, var in (("v66_picker.py", "_v66b64"), ("v67_history.py", "_v67b64"), ("v68_alternatives.py", "_v68b64"), ("v69_checker.py", "_v69b64"), ("v70_yearly.py", "_v70b64")):
    enc = base64.b64encode(open(mod, 'rb').read()).decode()
    pat = r'(/ "' + re.escape(mod) + r'"\)\.write_bytes\(' + var + r'\.b64decode\(")[^"]*(")'
    b2, k = re.subn(pat, lambda m: m.group(1) + enc + m.group(2), b, count=1)
    assert k == 1, mod
    b = b2; print("embedded", mod, len(enc))
open('build.py', 'w').write(b)
