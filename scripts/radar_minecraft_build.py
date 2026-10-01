import asyncio, subprocess
from pathlib import Path
import edge_tts

W=Path('work'); O=Path('out'); O.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
VOICE='pt-BR-ThalitaMultilingualNeural'; RATE='-3%'; PITCH='-2Hz'

sections=[
('A PRIMEIRA NOVA DIMENSÃO EM 14 ANOS','Minecraft acaba de ganhar uma das maiores novidades da sua história recente. A Mojang confirmou The Sift, uma nova dimensão que já pode ser explorada em Minecraft Dungeons 2 e que também vai chegar ao Minecraft principal. E não estamos falando de um simples bioma ou de uma atualização pequena. The Sift será a quarta dimensão oficial do universo Minecraft.'),
('O QUE É THE SIFT?','The Sift é uma dimensão vibrante, cheia de almas e conectada ao mundo por fendas misteriosas. Em Dungeons 2, essas fendas podem aparecer durante a exploração e transportar o jogador para áreas totalmente novas. A Mojang já mostrou regiões como Meadow e Carapace, com cenários bem diferentes do Overworld, do Nether e do End.'),
('POR QUE ISSO É TÃO GRANDE?','A última vez que Minecraft recebeu uma nova dimensão foi há mais de quatorze anos, quando o End passou a fazer parte do jogo. Desde então, o universo principal ficou dividido entre Overworld, Nether e End. Agora, The Sift entra oficialmente nessa lista e abre espaço para novas criaturas, estruturas, mecânicas e histórias.'),
('DUNGEONS 2 JÁ ESTÁ DISPONÍVEL','Minecraft Dungeons 2 foi lançado em vinte e nove de setembro de dois mil e vinte e seis para Steam, Xbox Series X e S, PlayStation 5, Nintendo Switch e Switch 2. Além da nova dimensão, o jogo traz um mundo interligado, novas missões, mais equipamentos e o retorno dos illagers, agora liderados pelo Illager High Council.'),
('E NO MINECRAFT NORMAL?','A parte mais importante para quem joga Minecraft Java ou Bedrock é esta: a Mojang confirmou que The Sift também vai chegar ao jogo principal no próximo ano. Durante o Minecraft Live, a empresa mostrou um primeiro vislumbre da dimensão e até uma das criaturas que vivem por lá. Então não é rumor, mod ou conceito de fã. É conteúdo oficial.'),
('O QUE PODE MUDAR NO JOGO?','Uma quarta dimensão pode mudar bastante a exploração de Minecraft. Novos portais podem significar novos materiais, inimigos, estruturas e sistemas exclusivos. A Mojang ainda não revelou todos os detalhes da versão para Java e Bedrock, então vale separar o que já foi confirmado do que ainda é especulação. Mas uma coisa é certa: The Sift é uma das maiores expansões do universo Minecraft em muitos anos.'),
('CURTIU A NOVIDADE?','E aí, você acha que The Sift tem potencial para ficar no mesmo nível do Nether e do End? Conta pra gente nos comentários. Se gostou do vídeo, deixe seu like e não esqueça de se inscrever no Radar dos Games para acompanhar mais notícias, lançamentos e novidades do mundo dos games.')]
shorts=[
('MINECRAFT GANHOU UMA NOVA DIMENSÃO!','Depois de mais de quatorze anos, Minecraft finalmente tem uma nova dimensão oficial. Ela se chama The Sift, já apareceu em Minecraft Dungeons 2 e foi confirmada para chegar ao Minecraft Java e Bedrock no próximo ano. É a quarta dimensão, ao lado do Overworld, Nether e End. Assista ao vídeo completo no Radar dos Games.'),
('O QUE É THE SIFT?','The Sift é a nova dimensão de Minecraft. Ela é vibrante, cheia de almas e acessada por fendas misteriosas em Minecraft Dungeons 2. A Mojang já mostrou regiões como Meadow e Carapace, além de novas criaturas. E o mais importante: ela também vai chegar ao Minecraft principal.'),
('NÃO É RUMOR: VAI CHEGAR AO MINECRAFT NORMAL','Se você achou que The Sift era exclusiva de Minecraft Dungeons 2, atenção. A Mojang confirmou no Minecraft Live que a nova dimensão chega ao Minecraft Java e Bedrock no próximo ano. Pela primeira vez em mais de quatorze anos, o jogo principal vai ganhar uma quarta dimensão oficial. Siga o Radar dos Games para mais novidades.')]

def run(cmd):
    print('+',' '.join(map(str,cmd)),flush=True)
    subprocess.run([str(x) for x in cmd],check=True)

def dur(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p)],text=True).strip())

async def synth(text,out):
    await edge_tts.Communicate(text,VOICE,rate=RATE,pitch=PITCH).save(str(out))

async def make_voice():
    for i,(_,txt) in enumerate(sections,1):
        mp3=W/f'sec{i}.mp3'; wav=W/f'sec{i}.wav'; await synth(txt,mp3)
        run(['ffmpeg','-y','-i',mp3,'-af','acompressor=threshold=-18dB:ratio=2.5:attack=15:release=180,loudnorm=I=-16:LRA=7:TP=-1.5','-ar','48000','-ac','2',wav])
    for i,(_,txt) in enumerate(shorts,1):
        mp3=W/f'short{i}.mp3'; wav=W/f'short{i}.wav'; await synth(txt,mp3)
        run(['ffmpeg','-y','-i',mp3,'-af','acompressor=threshold=-18dB:ratio=2.5:attack=15:release=180,loudnorm=I=-16:LRA=7:TP=-1.5','-ar','48000','-ac','2',wav])

asyncio.run(make_voice())

imgs=[W/'img02.jpg',W/'img06.jpg',W/'img08.jpg',W/'img03.jpg',W/'img02.jpg',W/'img07.jpg',W/'img05.jpg']
segs=[]
for i,((title,_),img) in enumerate(zip(sections,imgs),1):
    audio=W/f'sec{i}.wav'; d=dur(audio); out=W/f'seg{i}.mp4'; tf=W/f'title{i}.txt'; tf.write_text(title,encoding='utf-8')
    fade=max(0,d-0.45)
    motion="zoompan=z='min(zoom+0.00045,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30"
    vf=(f"scale=2100:1182:force_original_aspect_ratio=increase,crop=2100:1182,{motion},"
        f"drawbox=x=0:y=820:w=1920:h=260:color=black@0.45:t=fill,"
        f"drawtext=fontfile={FONT}:text='RADAR DOS GAMES':fontcolor=white:fontsize=28:x=48:y=40:box=1:boxcolor=black@0.60:boxborderw=12,"
        f"drawtext=fontfile={FONT}:textfile={tf.resolve()}:fontcolor=white:fontsize=46:x=72:y=865:box=1:boxcolor=black@0.50:boxborderw=12,"
        f"drawtext=fontfile={FONT_REG}:text='FONTE MINECRAFT - MOJANG - XBOX':fontcolor=white@0.72:fontsize=19:x=w-tw-45:y=h-th-32,"
        f"fade=t=in:st=0:d=0.35,fade=t=out:st={fade:.3f}:d=0.45")
    run(['ffmpeg','-y','-loop','1','-i',img,'-i',audio,'-t',f'{d:.3f}','-vf',vf,'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',out])
    segs.append(out)
with open(W/'bodylist.txt','w') as f:
    for p in segs: f.write(f"file '{p.resolve()}'\n")
run(['ffmpeg','-y','-f','concat','-safe','0','-i',W/'bodylist.txt','-c','copy',W/'body.mp4'])

run(['ffmpeg','-y','-i',W/'intro.mp4','-vf','scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',W/'intro_norm.mp4'])
with open(W/'finallist.txt','w') as f:
    f.write(f"file '{(W/'intro_norm.mp4').resolve()}'\nfile '{(W/'body.mp4').resolve()}'\n")
run(['ffmpeg','-y','-f','concat','-safe','0','-i',W/'finallist.txt','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',O/'Radar_dos_Games_Minecraft_The_Sift_FINAL.mp4'])

thumb=(f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,drawbox=x=0:y=0:w=1280:h=720:color=black@0.23:t=fill,"
       f"drawtext=fontfile={FONT}:text='MINECRAFT TEM':fontcolor=white:fontsize=62:x=55:y=105:box=1:boxcolor=black@0.62:boxborderw=15,"
       f"drawtext=fontfile={FONT}:text='NOVA DIMENSÃO!':fontcolor=0x67F4FF:fontsize=70:x=55:y=215:box=1:boxcolor=black@0.65:boxborderw=15,"
       f"drawtext=fontfile={FONT}:text='1ª EM +14 ANOS':fontcolor=yellow:fontsize=44:x=60:y=345:box=1:boxcolor=black@0.70:boxborderw=12")
run(['ffmpeg','-y','-i',W/'img02.jpg','-frames:v','1','-vf',thumb,'-q:v','2',O/'Minecraft_The_Sift_Thumbnail.jpg'])

simgs=[W/'img02.jpg',W/'img06.jpg',W/'img08.jpg']
stitles=['MINECRAFT GANHOU\\nUMA NOVA DIMENSÃO!','O QUE É\\nTHE SIFT?','VAI CHEGAR AO\\nMINECRAFT NORMAL!']
ssubs=['THE SIFT - 4ª DIMENSÃO OFICIAL','FENDAS - ALMAS - NOVAS REGIÕES','JAVA + BEDROCK - CONFIRMADO']
for i,(img,title,sub) in enumerate(zip(simgs,stitles,ssubs),1):
    a=W/f'short{i}.wav'; d=dur(a); out=O/f'Radar_dos_Games_Minecraft_The_Sift_SHORT_{i}.mp4'
    fc=(f"[0:v]scale=1350:760:force_original_aspect_ratio=increase,crop=1350:760,zoompan=z='min(zoom+0.0007,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720:fps=30[move];"
        f"[move]split=2[b][f];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:14,eq=brightness=-0.22[bg];"
        f"[f]scale=1020:574[fg];[bg][fg]overlay=(W-w)/2:550[base];"
        f"[base]drawtext=fontfile={FONT}:text='RADAR DOS GAMES':fontcolor=white:fontsize=34:x=55:y=70:box=1:boxcolor=black@0.72:boxborderw=12,"
        f"drawtext=fontfile={FONT}:text='{title}':fontcolor=white:fontsize=62:x=(w-text_w)/2:y=185:line_spacing=8:box=1:boxcolor=black@0.72:boxborderw=18,"
        f"drawtext=fontfile={FONT}:text='{sub}':fontcolor=0x67F4FF:fontsize=36:x=(w-text_w)/2:y=1225:box=1:boxcolor=black@0.72:boxborderw=13,"
        f"drawtext=fontfile={FONT_REG}:text='VÍDEO COMPLETO NO CANAL':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=1510:box=1:boxcolor=black@0.65:boxborderw=11,"
        f"drawtext=fontfile={FONT}:text='RADAR DOS GAMES':fontcolor=yellow:fontsize=42:x=(w-text_w)/2:y=1575:box=1:boxcolor=black@0.68:boxborderw=12[v]")
    run(['ffmpeg','-y','-loop','1','-i',img,'-i',a,'-t',f'{d:.3f}','-filter_complex',fc,'-map','[v]','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart',out])

(O/'metadata.txt').write_text('''TÍTULO\nMINECRAFT GANHOU UMA NOVA DIMENSÃO! 😱 The Sift explicado\n\nDESCRIÇÃO\nDepois de mais de 14 anos, Minecraft ganhou uma nova dimensão oficial: The Sift. Ela já pode ser explorada em Minecraft Dungeons II e a Mojang confirmou que também chegará ao Minecraft Java e Bedrock no próximo ano.\n\nNeste vídeo do Radar dos Games: o que é The Sift, por que ela é a quarta dimensão oficial, o que muda em Dungeons II e o que já foi confirmado para Java e Bedrock.\n\nFontes oficiais: Minecraft / Mojang Studios / Xbox.\n#Minecraft #TheSift #MinecraftDungeons2 #Mojang #RadarDosGames\n\nTAGS\nMinecraft, The Sift, Minecraft nova dimensão, Minecraft Dungeons II, Mojang, Minecraft Live 2026, Minecraft Java, Minecraft Bedrock, Radar dos Games''',encoding='utf-8')
print('DONE')
for p in O.iterdir(): print(p,p.stat().st_size)
