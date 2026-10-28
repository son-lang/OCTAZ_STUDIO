#!/usr/bin/env python3
"""배포 전 실행: python3 tools/stamp.py  (저장소 루트에서. 자동 실행은 .github/workflows/stamp.yml 참고)
- images/ 안 이미지 URL 뒤에 ?v=<파일 내용 해시> 를 붙입니다(내용이 바뀐 파일만 주소가 바뀜 -> 캐시 무효화).
- <meta name="build-id">를 갱신합니다(페이지 내부 최신 버전 확인용).
여러 번 실행해도 결과가 같습니다(멱등)."""
import re, sys, hashlib, os
root = sys.argv[1] if len(sys.argv) > 1 else ('site' if os.path.isdir('site') else '.')
def h(b): return hashlib.sha1(b).hexdigest()[:8]
for name in ('index.html', 'work.html'):
    p = os.path.join(root, name)
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'\s*<meta name="build-id" content="[^"]*">', '', t)
    def img(m):
        f = os.path.join(root, m.group(1))
        return f'src="{m.group(1)}?v={h(open(f,"rb").read())}"' if os.path.exists(f) else m.group(0)
    t = re.sub(r'src="(images/[^"?]+)(?:\?v=[0-9a-f]+)?"', img, t)
    # 별도 CSS/JS 파일을 추가하게 될 경우도 자동 처리 (상대경로 로컬 파일만)
    def res(m):
        f = os.path.join(root, m.group(2))
        return f'{m.group(1)}="{m.group(2)}?v={h(open(f,"rb").read())}"' if os.path.exists(f) else m.group(0)
    t = re.sub(r'(href|src)="((?!https?:|//|#|mailto:)[^"?#]+\.(?:css|js))(?:\?v=[0-9a-f]+)?"', res, t)
    bid = h(t.encode())
    t = t.replace('<meta charset="UTF-8">', f'<meta charset="UTF-8">\n<meta name="build-id" content="{bid}">', 1)
    open(p, 'w', encoding='utf-8').write(t)
    print(name, 'build-id', bid)
