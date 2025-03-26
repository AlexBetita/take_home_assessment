from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (auth_router,
                    bot_router,
                    order_router,
                    test_router)

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json", debug=True)

# routes
app.include_router(auth_router, prefix='/api')
app.include_router(bot_router, prefix='/api')
app.include_router(order_router, prefix='/api')
app.include_router(test_router, prefix='/api')

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
