import uvicorn
from fastapi import FastAPI
from controllers.ocr_controller import ocr_router
from fastapi.responses import RedirectResponse

app = FastAPI()
app.include_router(ocr_router)


@app.exception_handler(404)
def otherwise(request, exeption):
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8080)
