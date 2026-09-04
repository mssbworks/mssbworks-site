# -*- coding: utf-8 -*-
"""引っ越しの検収。GitHub Pages版とWorkers版を全ファイル突き合わせる。

目視で「だいたい同じ」にしない。**ファイルの指紋（SHA-256）の全数一致で言い切る。**
1本でも中身が違えば、どのファイルがどう違うかを出して異常終了する。

使い方:
    python3 .cloudflare/検収.py https://mssbworks-site.<アカウント>.workers.dev

引っ越し前は、比較先を GitHub Pages（https://mssbworks.com）にしておく。
"""
import hashlib
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _assetsignore():
    """配らないものの一覧は .assetsignore を正本にする。

    ここに同じ一覧をもう1つ書くと、片方だけ直したときに検収が嘘をつく
    （実際、.assetsignore を足したとき検収側の除外を忘れて不一致が出た）。
    """
    path = os.path.join(ROOT, '.assetsignore')
    names = set()
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    names.add(line.rstrip('/').replace('/**', ''))
    return names


SKIP = {'.git', '.cloudflare', 'node_modules'} | _assetsignore()
SKIP_FILES = _assetsignore()


def local_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
            out.append(rel)
    return sorted(out)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fetch(base, rel):
    url = base.rstrip('/') + '/' + rel
    req = urllib.request.Request(url, headers={'User-Agent': 'mssb-kenshu/1'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


def main():
    if len(sys.argv) < 2:
        print('比較先のURLを渡してください（例: https://mssbworks.com）')
        return 2
    base = sys.argv[1]
    files = local_files()
    print(f'手元のファイル: {len(files)}本')
    bad = []
    for rel in files:
        with open(os.path.join(ROOT, rel), 'rb') as f:
            want = sha(f.read())
        try:
            status, body = fetch(base, rel)
        except Exception as e:
            bad.append((rel, f'取れない: {e}'))
            continue
        if status != 200:
            bad.append((rel, f'HTTP {status}'))
            continue
        got = sha(body)
        if got != want:
            bad.append((rel, f'中身が違う（手元 {want[:12]} / 先 {got[:12]}）'))

    if bad:
        print(f'\n不一致 {len(bad)}件')
        for rel, why in bad:
            print(f'  {rel}: {why}')
        print('\n→ 切り替えない。原因を潰してから再実行する')
        return 1
    print(f'\n全{len(files)}本が指紋まで一致。切り替えてよい')
    return 0


if __name__ == '__main__':
    sys.exit(main())
