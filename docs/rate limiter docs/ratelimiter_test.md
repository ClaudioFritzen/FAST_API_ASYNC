✅ Resumo validado: como “burlar” o rate limiter nos testes
A sua estratégia está correta e completa.
Aqui está a versão final, organizada e com os motivos por trás de cada passo.

1️⃣ Ativar TESTING=1 antes de qualquer import
Você fez certo:

pytest.ini
ini
[pytest]
env =
    TESTING=1
E instalou:

Código
poetry add --dev pytest-env
Isso garante:

TESTING=1 existe antes de qualquer import

app.py é importado já sabendo que está em modo de teste

Redis não é importado

limiter não é criado

middleware ignora o rate limit

Perfeito.

fast_zero_async/config.py
python
import os

TESTING = os.getenv("TESTING", "0") == "1"
Ele é responsável por:

ler a variável de ambiente definida pelo pytest

converter para booleano

centralizar a lógica de ambiente

permitir que o app se comporte diferente em produção e testes

2️⃣ Mover o import do app para dentro da fixture client
Você fez isso:

python
app_module = importlib.import_module('fast_zero_async.app')
app = app_module.app
Isso resolve o problema do event loop:

pytest cria o loop

só depois o app é carregado

FastAPI inicializa dentro do loop correto

testcontainers não quebra

Redis não é importado cedo demais

Perfeito.

3️⃣ Alterações no app.py
Você implementou:

python
from fast_zero_async.config import TESTING

if not TESTING:
    from fast_zero_async.services.redis.client import redis_client
    from fast_zero_async.services.redis.rate_limiter import AsyncRateLimiter
    limiter = AsyncRateLimiter(redis_client, 10, 60)
else:
    limiter = None
Isso garante:

Em produção → Redis + limiter funcionam

Em testes → nada disso é importado

Perfeito.

4️⃣ Remover qualquer import de Redis ou limiter do conftest.py
Você fez isso, e isso foi crucial.

Antes, o conftest importava:

python
from fast_zero_async.services.redis import client as redis_module
from fast_zero_async.app import limiter
Isso quebrava tudo, porque:

importava o app cedo demais

importava Redis cedo demais

criava pools no loop errado

causava “Event loop is closed”

Ao remover essas fixtures, tudo estabilizou.

Perfeito.

5️⃣ Resultado final
Agora você tem:

✔ Testes funcionando
✔ Redis ignorado nos testes
✔ Rate limiter desativado
✔ Event loop estável
✔ Lint satisfeito
✔ Estrutura limpa e profissional