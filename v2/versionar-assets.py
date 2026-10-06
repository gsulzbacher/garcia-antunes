#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carimba os links de CSS com um hash do conteúdo.

O GitHub Pages serve CSS com cache-control de 10 minutos. Sem isso, o
navegador de quem está revisando continua com a folha antiga depois de
um deploy, e o site aparece quebrado sem estar. Rodar antes de publicar.
"""
import hashlib, io, re, glob, os

versoes = {}
for css in glob.glob('assets/*.css'):
    h = hashlib.md5(open(css,'rb').read()).hexdigest()[:8]
    versoes[os.path.basename(css)] = h

alterados = 0
for pagina in glob.glob('*.html'):
    txt = io.open(pagina, encoding='utf-8').read()
    novo = txt
    for nome, h in versoes.items():
        novo = re.sub(r'href="assets/' + re.escape(nome) + r'(\?v=[0-9a-f]+)?"',
                      'href="assets/%s?v=%s"' % (nome, h), novo)
    if novo != txt:
        io.open(pagina, 'w', encoding='utf-8').write(novo)
        alterados += 1

print('versões:', ', '.join('%s=%s' % kv for kv in sorted(versoes.items())))
print('páginas carimbadas:', alterados)
