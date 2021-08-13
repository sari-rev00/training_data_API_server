# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import json

from db.tables import SessionManager

sm = SessionManager()


class Data(BaseModel):
    code: str
    score: Dict


class SimpleResponse(BaseModel):
    Dict


class App(FastAPI):
    def __init__(self):
        super().__init__()
        self.prepare_resources()
        return None
    
    def prepare_resources(self):
        @self.get('/')
        def index():
            return JSONResponse(content={'msg': 'ok'}, status_code=status.HTTP_200_OK)
        
        @self.post('/upload', response_model=SimpleResponse)
        def upload(request: Data):
            print(request.score)
            sm.calc_insert(data=request.score)
            return JSONResponse(
                content={'msg': 'ok'}, 
                status_code=status.HTTP_200_OK
            )

        @self.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc):
#            print(dir(request))
#            print(request.app)
#            print(request.client)
#            print(request.headers)
#            print(request.method)
#            print(request.url)
            return JSONResponse(
                content={'msg': 'Invalid request.'},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        @self.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc):
            print(request)
            return JSONResponse(
                content={'msg': 'Internal server error.'},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return None


TEST = False
if __name__ == '__main__':
    import uvicorn
    if TEST:
        host = "0.0.0.0"
    else:
        host = "192.168.0.51"
    try:
        app = None
        app=App()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
#            allow_credentials=True,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )

        uvicorn.run(
            app=app, 
            host=host, 
            port=8000, 
        )
    except Exception as e:
        print(e)
    finally:
        print("close app")
        if app:
            del app