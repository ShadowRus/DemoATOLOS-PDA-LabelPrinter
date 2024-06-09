import asyncio
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from api import deps
import datetime
import requests
import json
from decouple import config
from requests.exceptions import ConnectionError

router = APIRouter()
now = datetime.datetime.now()