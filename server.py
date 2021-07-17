# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import json

from db.tables import SessionManager

sm = SessionManager()

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
        def upload(request: Dict):
            print(request)
            sm.calc_insert(data=request)
            return JSONResponse(content={'msg': 'ok'}, status_code=status.HTTP_200_OK)

        @self.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc):
            logger.error(exc.errors())
            return JSONResponse(
                content={'msg': 'Invalid request.'},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        @self.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc):
            logger.error(exc.detail)
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