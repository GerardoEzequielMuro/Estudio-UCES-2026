# -*- coding: utf-8 -*-
import io, re
s = io.open(r'C:\Users\gerar\Downloads\Sistema-Estudio-UCES\analisis-conceptual.html', encoding='utf8').read()
print('size KB:', round(len(s.encode('utf8')) / 1024))
print('emdash:', s.count('—'), 'endash:', s.count('–'))
print('tabs:', len(re.findall(r'data-tab=', s)))
print('quiz preguntas:', len(re.findall(r'\{q:"', s)))
print('flashcards:', len(re.findall(r'\{f:"', s)))
print('script balanceado:', s.count('<script>') == s.count('</script>'))
print('div balance:', s.count('<div') - s.count('</div>'))
