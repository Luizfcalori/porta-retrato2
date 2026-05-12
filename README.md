# 🖼 Retrato Digital — PWA

Slideshow elegante para exibir fotos da galeria no Android (ou qualquer dispositivo).

## Como instalar no Android

### Opção 1 — Via Google Chrome (recomendado)
1. Abra o Chrome no Android
2. Acesse o arquivo `index.html` (suba para um servidor ou use um app como "Simple HTTP Server")
3. O Chrome mostrará um banner "Adicionar à tela inicial" — toque nele
4. Ou: toque no menu ⋮ → "Adicionar à tela inicial"
5. O app aparecerá na sua tela inicial como qualquer outro aplicativo ✅

### Opção 2 — Hospedar localmente com um servidor HTTP
Se tiver um PC na mesma rede Wi-Fi:
```bash
# Python 3
cd pasta-retrato-digital
python3 -m http.server 8080
```
Depois acesse no Android: `http://IP-DO-PC:8080`

### Opção 3 — Usar o GitHub Pages (grátis)
1. Crie um repositório no GitHub
2. Faça upload dos arquivos
3. Ative GitHub Pages nas configurações
4. Acesse a URL gerada no Android e instale

## Funcionalidades

- 🖼 **Slideshow automático** com efeito Ken Burns (zoom suave)
- 👆 **Swipe** para avançar/voltar entre fotos
- ⏯ **Pausa/Retomada** do slideshow
- ⏱ **Velocidade ajustável**: 3s, 5s, 8s ou 12s por foto
- ➕ **Adicionar mais fotos** sem reiniciar
- 🕐 **Relógio ambiente** discreto no canto
- 📱 **Tela cheia** automática (modo retrato digital)
- ✈️ **Funciona offline** após o primeiro acesso

## Controles

| Ação | Gesto |
|------|-------|
| Próxima foto | Swipe ← ou toque ▸ |
| Foto anterior | Swipe → ou toque ◂ |
| Mostrar/ocultar controles | Toque no centro |
| Pausar/Retomar | Botão ⏸/▶ |
| Ajustar velocidade | Botão ⏱ |
| Adicionar fotos | Botão + |

## Arquivos

```
retrato-digital/
├── index.html      ← App principal
├── manifest.json   ← Configuração PWA
├── sw.js           ← Service Worker (offline)
├── icon-192.png    ← Ícone do app
├── icon-512.png    ← Ícone grande
└── README.md       ← Este arquivo
```
