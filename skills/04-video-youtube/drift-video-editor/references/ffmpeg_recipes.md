# FFmpeg Recipes for Tech & Devlog Video Editing

Guia prático de filtros complexos para cortes acústicos, transições, zoom contextual e composição de overlays.

---

## 1. Detecção e Remoção de Silêncio com Padding Acústico

### Detecção de Silêncios
```bash
ffmpeg -hide_banner -vn -i input.mp4 -af "silencedetect=noise=-30dB:d=0.5" -f null -
```
- `-30dB`: Limiar típico de ruído de sala vs fala humana.
- `d=0.5`: Ignora pausas respiratórias inferiores a 500ms.

### Regra de Padding Acústico
- **In-Padding**: Adicionar `150ms` antes do início detectado da voz para não engolir o primeiro fonema.
- **Out-Padding**: Manter `250ms` após o fim da fala para preservar a cauda natural da reverberação e respiração.

### Micro-Fades em Áudio (Anti-Click)
Em cada junção de corte de voz, adicione micro-fades de entrada e saída:
```text
afade=t=in:st=0:d=0.08,afade=t=out:st=<DUR-0.08>:d=0.08
```

---

## 2. Dynamic Punch-In Zooms (Enquadramento Contextual)

Para dar ênfase visual a menus, código ou momentos de física/gameplay sem perda de proporção:

### Enquadramento Central (1.25x / 1440x810)
```text
crop=1440:810:(in_w-out_w)/2:(in_h-out_h)/2,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1
```

### Enquadramento Superior Esquerdo (Menu / UI)
```text
crop=1440:810:80:60,scale=1920:1080,setsar=1
```

### Enquadramento Inferior Direito (Minimapa / Chat)
```text
crop=1440:810:in_w-out_w-80:in_h-out_h-60,scale=1920:1080,setsar=1
```

> **Aviso Crítico**: O nó `setsar=1` é obrigatório em todos os fluxos recortados para evitar distorção ou falha de concatenação no filtro `concat`.

---

## 3. Transições Suaves (`xfade`)

Entre blocos conceituais distintos, calcular o offset exato:
$$\text{offset} = \text{duração}(A) - \text{duração da transição}$$

### Exemplo de Dissolve (0.4s)
```text
[v0][v1]xfade=transition=fade:duration=0.4:offset=12.200[v_xfaded]
```

### Transição de Áudio Equivalente (`acrossfade`)
```text
[a0][a1]acrossfade=d=0.4:c1=tri:c2=tri[a_xfaded]
```

---

## 4. Composição de Lower-Third com Alpha Fade

Para sobrepor gráficos transparentes gerados pelo `scripts/generate_lower_third.py`:

```bash
ffmpeg -i input.mp4 -i lower_third.png -filter_complex \
"[1:v]format=rgba,fade=t=in:st=1.0:d=0.4:alpha=1,fade=t=out:st=9.6:d=0.4:alpha=1[lt_faded]; \
 [0:v][lt_faded]overlay=0:0:enable='between(t,1.0,10.0)'[vout]" \
-map "[vout]" -map 0:a -c:v libx264 -crf 18 -preset fast -c:a copy output.mp4
```

---

## 5. Perfil de Exportação Recomendado (1080p60 Web & YouTube)

```bash
ffmpeg -y -i input.mp4 \
  -c:v libx264 -preset fast -crf 18 -r 60 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  output_1080p60.mp4
```
- `-crf 18`: Qualidade visual transparente (sem artefatos de compressão perceptíveis).
- `-movflags +faststart`: Move a tabela de átomos `moov` para o início do arquivo, permitindo reprodução instantânea na web.
