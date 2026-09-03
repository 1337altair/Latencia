# Latencia

O Latencia é um app que eu fiz pra testar a internet sem precisar ficar abrindo site de speedtest toda hora. A ideia é ir além de só mostrar download e upload e virar uma ferramenta pra entender quando a conexão tá ruim e onde pode estar o problema.

Hoje ele já testa download, upload, ping, jitter e perda de pacotes. Tem monitor de latência em tempo real, diagnóstico básico, histórico dos testes, nota da conexão e algumas informações da rede.

A interface tem português e inglês. Dá pra trocar em Configurações e ele lembra o idioma que você escolheu.

Feito por 0xaltair.

Pra usar o programa não precisa instalar Python, VS Code ou dependência nenhuma. É só baixar o `Latencia-Setup.exe`, abrir e instalar normalmente. Também tem o `Latencia.exe` portátil pra quem só quer abrir direto sem instalar.

Se eu estiver mexendo no código e quiser testar localmente, aí sim preciso do Python. O `build_release.bat` serve pra gerar uma versão no Windows, mas normalmente nem preciso usar ele porque o GitHub já faz a build sozinho.

Quando eu mando o projeto pro GitHub, a action `Windows build` compila o programa em uma máquina Windows e gera `Latencia.exe` e `Latencia-Setup.exe`. Os dois ficam disponíveis nos artefatos da execução.

Se eu criar uma tag tipo `v0.1.0`, o GitHub também cria uma Release automaticamente e coloca os dois arquivos nela. Aí dá pra mandar o link da Release pra qualquer pessoa baixar e instalar.

O histórico do programa fica salvo no próprio perfil do Windows em `%LOCALAPPDATA%\Latencia`, então atualizar ou reinstalar o app não apaga os testes antigos automaticamente.

Ainda tem bastante coisa que eu quero melhorar, principalmente diagnóstico de Wi-Fi, gráficos, escolha de servidor, testes mais consistentes de velocidade e identificação melhor de problema entre PC, roteador e operadora.
