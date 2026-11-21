# Fazendo a implementação do Grafana com Doker na nossa maquina.

# 1. Primeiro criaremos o docker-compose
grafana:
    image: grafana/grafana
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: ${GF_SECURITY_ADMIN_USER}
      GF_SECURITY_ADMIN_PASSWORD: ${GF_SECURITY_ADMIN_PASSWORD}
    
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
    grafana-storage:

já definimos a senha e user no .env


#### Agora é so subir os containers
docker-compose up -d 

### Acessando o grafana
http://127.0.0.1:3000/login

# 2. Vamos nos conectar no nosso db postgres dentro do grafana

    - Vamos clicar em connections
    - Procuramos por postgres, instalar se já não estiver
    - Clicamos para adicionar em data sources
    - Passamos os dados que está definido no .env 


# PASSO 3 — Integrar Prometheus + FastAPI + Grafana
Depois deste passo, você terá:

Latência por endpoint

Requests por segundo

Erros por endpoint

Tempo médio de resposta

Status codes

Métricas internas da aplicação

Dashboard pronto no Grafana

E tudo isso em tempo real.

# 3.1 — Adicionar Prometheus ao docker-compose
Adicione este serviço:

yaml
prometheus:
  image: prom/prometheus
  container_name: prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  depends_on:
    - api

# 3.2 — Criar o arquivo prometheus.yml
Crie na raiz do projeto:

Código
prometheus.yml
Conteúdo:

yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "fastapi"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["api:8000"]
⚠️ IMPORTANTE:  
O nome do target deve ser o nome do serviço no docker-compose, que no seu caso é:

Código
api


# 3.3 — Instrumentar sua FastAPI com Prometheus
Instale:

Código
poetry add prometheus-fastapi-instrumentator@^7.0.0


No seu main.py:

python
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

Isso cria automaticamente o endpoint:

Código
/metrics


# Subindo o container 
docker-compose up -d                               
[+] up 9/111
 - Image prom/prometheus [⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿]   154MB / 154.4MB Pulling       


 ### se der algum erro 
 docker-compose down
>> docker-compose up -d --force-recreate      




Tivemos problemas com o alembic

mas isso não tem nada a ver com a configuração do grafana e promethues


