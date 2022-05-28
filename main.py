import asyncio
import aiohttp
import time
import json



url = 'https://api.dataforsyningen.dk/postnumre/{}'
Postnumre = ['22222000', '1455', '2200', '2300', '2400','1000','7130','7140','2000', '1455', '2200', '2300', '2400','1000', '1455', '2200']

#Creates a lists of the results
ListOfResults = []

#Function to collect each task
def CreateListOfRequests(session):
    '''Creates a list of tasks from each postnumer'''
    tasks = []
    for postnummer in Postnumre :
        tasks.append(asyncio.create_task(session.get(url.format(postnummer), ssl=False)))
    return tasks

#Function to handle the response
def GetCityName(response):
    '''
    Takes the respons and return the city name
    '''
    data=json.dumps(response)
    data=json.loads(data)
    Name=None
    if 'navn' in data:
        Name=data['navn']
    return Name


start = time.time()

#Collect the response
async def GetResponse():
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = CreateListOfRequests(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(GetCityName(await response.json()))
asyncio.run(GetResponse())

end = time.time()
total_time = end - start
print("It took {} seconds to make {} API calls".format(total_time, len(Postnumre)))
