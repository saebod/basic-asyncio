import asyncio
from aiohttp import ClientSession, ClientTimeout
import time
import json
import pandas as pd # 
from tqdm import tqdm

# Loads df
df = pd.read_csv("df.csv")
#Split columns
df[['Type', 'Y', 'X']] =df['CelleID_m100'].str.split('_', expand=True)
df['X'] = df['X'].apply(lambda x: float(x)*100+50)
df['Y'] = df['Y'].apply(lambda x: float(x)*100+50)
url = 'https://api.dataforsyningen.dk/kommuner/reverse?x={}&y={}&srid=25832'

## Asynico settings
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
timeout = ClientTimeout(total=6000)

#Creates a lists of the results
ListOfResults = []

#Function to collect each task
def CreateListOfRequests(session):
    '''Creates a list of tasks from each postnumer'''
    tasks = []
    for idx, row in tqdm(df.iterrows()):
        tasks.append(asyncio.create_task(session.get(url.format(df.loc[idx,'X'],df.loc[idx,'Y']), ssl=False)))
    return tasks

#Function to handle the response
def GetMunicipality(response):
    '''
    Takes the respons and return the Municipality
    '''
    data=json.dumps(response)
    data=json.loads(data)
    Name=None
    if 'navn' in data:
        Name=data['navn']
    else:
        Name='None'
    return Name

start = time.time()
#Collect the response
async def GetResponse():
    async with ClientSession(trust_env=True,timeout=timeout) as session:
        tasks = CreateListOfRequests(session)
        responses = await asyncio.gather(*tasks)
        for idx, response in enumerate(responses):
            df.loc[idx,'Kommune']=GetMunicipality(await response.json())
asyncio.run(GetResponse())
end = time.time()
total_time = end - start
print("It took {} seconds to make {} API calls".format(total_time, len(df)))
