from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):

    # definimos as origens permitidas
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "*",
        #definimos o wildcard para permitir todas as origens, 
        # mas em produção é recomendado especificar os domínios permitidos


        # Adiciona aqui o domínio do frontend em produção
        #"https://seu-dominio.com"

    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    