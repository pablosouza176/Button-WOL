# Button WOL — Wake on LAN & Shutdown via Web

Uma interface web minimalista, elegante e responsiva para ligar e desligar seu computador remotamente via rede local usando Wake on LAN e SSH.

## ✨ Funcionalidades

- **Ligar o PC (Wake on LAN):** Envia um Magic Packet via broadcast UDP na sua rede local para acordar a máquina.
- **Desligar o PC (Shutdown via SSH):** Desliga o computador de forma segura acessando-o via SSH e executando o comando de desligamento.
- **Interface Web Moderna:** Feita com Flask e design focado em usabilidade (HTML/CSS), fácil de acessar via celular ou desktop.
- **Containerizado:** Totalmente empacotado em Docker, mantendo seu host limpo.
- **Compatível com CasaOS:** Inclui definições (`x-casaos`) no `docker-compose.yml` para integração nativa no CasaOS.

## 📂 Estrutura do Projeto

```text
Button-WOL/
├── app.py               # Backend em Python (Flask)
├── Dockerfile           # Instruções para construção da imagem Docker
├── docker-compose.yml   # Configuração dos serviços e CasaOS
├── requirements.txt     # Dependências do Python
├── wake_on_lan.sh       # Script bash que dispara o Magic Packet
├── shutdown.sh          # Script bash que acessa o PC via SSH para desligar
├── id_rsa               # Sua chave SSH privada (necessária para o shutdown)
└── templates/
    └── index.html       # Interface web
```

## 🚀 Passo a Passo de Instalação e Configuração

### 1. Preparar os Arquivos Locais
Antes de enviar para o servidor, configure os arquivos no seu computador.
1. Abra o arquivo `wake_on_lan.sh` e troque `<WOL_MAC>` pelo endereço MAC da placa de rede do computador que deseja ligar.
2. Abra o arquivo `shutdown.sh` e edite as variáveis:
   - `TARGET_HOST="<IP_DO_SEU_SERVIDOR>"`: Coloque o IP do computador que será desligado.
   - `TARGET_USER="<usuario_SSH>"`: Coloque o seu usuário do PC.
3. Edite o `docker-compose.yml` e altere a variável `WOL_MAC` (substitua `<SEU_MAC_ADDRESS>`) com o MAC address do PC.

### 2. Configurar a Chave SSH (Para a função de desligar)
Para o container conseguir desligar seu computador sem pedir senha, ele usa autenticação via chave SSH:
1. Gere um par de chaves SSH (se ainda não possuir uma dedicada). No seu terminal, rode:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "wol-container"
   ```
2. Renomeie a **chave privada** gerada para `id_rsa` e coloque na pasta raiz do projeto (`Button-WOL/id_rsa`).
3. Pegue o conteúdo da **chave pública** (`id_rsa.pub`) e adicione no arquivo de chaves autorizadas do computador alvo:
   - No **Linux/Mac**: Adicione em `~/.ssh/authorized_keys`.
   - No **Windows**: Adicione em `C:\Users\SeuUsuario\.ssh\authorized_keys` (lembre-se de ativar o servidor OpenSSH no Windows).

### 3. Transferir para o Servidor (CasaOS/Debian)
Copie a pasta inteira para o seu servidor (você pode usar um cliente SFTP ou SCP). Exemplo usando `scp`:
```bash
scp -r ./Button-WOL usuario@<IP_DO_SEU_SERVIDOR>:/DATA/AppData/wake-on-lan
```

### 4. Construir e Iniciar o Container
Acesse o seu servidor via SSH, vá até a pasta e suba o container:
```bash
cd /DATA/AppData/wake-on-lan
docker compose up -d --build
```
> **Nota de Rede (`network_mode: host`)**  
> O pacote mágico WOL precisa ser enviado via broadcast na rede local. Com o networking padrão e isolado do Docker, o pacote não alcança a rede física. Por isso, usamos a rede do host.

### 5. Acessar a Interface
Abra o navegador no seu celular ou PC e acesse a porta `8081` do seu servidor:
```text
http://<IP_DO_SEU_SERVIDOR>:8081
```

## 🛠 Comandos Úteis

```bash
# Ver logs em tempo real (muito útil para identificar erros de permissão ou SSH)
docker logs -f button-wol

# Parar o container
docker compose down

# Reiniciar o container
docker compose restart
```
