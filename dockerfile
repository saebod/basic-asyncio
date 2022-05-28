FROM python:3.8
COPY . .
RUN python -m pip install \
    aiohttp \
    asyncio 

CMD ["python","main.py"]