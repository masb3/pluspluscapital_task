""""
    DESCRIPTION:
        Asynchronous API client for http://numbersapi.com/.
        API URL structure: http://numbersapi.com/number/type?querystring
        Retrieves random fact based on randomly chosen 'type', 'number' and 'QUERY PARAMETER OPTIONS'
        supported by API endpoint.
        Asynchronously requests 'conf.NUMBER_OF_FACTS_TO_GET' random facts from API server.

        Sequence flow:
            0. If 'number' should be generated on server side go to 5.
            1. Randomly choose 'type' and 'QUERY PARAMETER OPTIONS'.
            2. Randomly choose if 'number' is generated on client or server side. If on server - go to 5.
            3. If 'type' is 'date' - generate 2 random numbers for 'month/date', otherwise 1 random number.
            4. Based on randomly chosen 'QUERY PARAMETER OPTIONS' create query string.
            5. Combine URL and send GET request.
            6. If return status not 200 - return None, otherwise return JSON object
            7. If retrieved fact is not found, force to generate 'number' on server and go to 0.
"""


import aiohttp
import asyncio
import random

import conf


def get_random_query_param(functionality):
    """
    Creates query string based on randomly generated 'functionality'
    :param functionality: query parameter option supported by server
    :return: query string
    """
    query = '?' + functionality
    if 'notfound' == functionality:
        return query + '=' + random.choice(conf.NOT_FOUND_CHOICES)

    elif 'default' == functionality:
        return query + '=' + conf.DEFAULT_FACT

    elif 'min and max' == functionality:
        rand_min = random.randint(conf.RAND_NUM_MIN, conf.RAND_NUM_MAX)
        rand_max = random.randint(conf.RAND_NUM_MIN, conf.RAND_NUM_MAX)
        while rand_min > rand_max:
            rand_min = random.randint(conf.RAND_NUM_MIN, conf.RAND_NUM_MAX)
            rand_max = random.randint(conf.RAND_NUM_MIN, conf.RAND_NUM_MAX)
        return '?' + 'min=' + str(rand_min) + '&' + 'max=' + str(rand_max)

    else:
        return ''


def get_random_url(server_rand):
    """
    Creates URL based on randomly generated data
    :param server_rand: Specifies where random 'number' is generated - on server or client
    :return: str
    """
    if server_rand:
        rand_type = 'server_rand'
    else:
        rand_type = random.choice(['server_rand', 'client_rand'])
    type_ = random.choice(conf.TYPES)
    functionality = random.choice(conf.FUNCTIONALITIES)

    if 'server_rand' == rand_type:
        return conf.BASE_URL + 'random/' + type_
    else:
        if 'date' == type_:
            month = random.randint(conf.RAND_NUM_MIN, conf.RAND_NUM_MAX)
            day = random.randint(conf.RAND_NUM_MIN, conf.RAND_NUM_MAX)
            url = str(month) + '/' + str(day) + '/' + type_
        else:
            rand_num = random.randint(conf.RAND_NUM_MIN, conf.RAND_NUM_MAX)
            url = str(rand_num) + '/' + type_

        return conf.BASE_URL + url + get_random_query_param(functionality)


async def get_fact(url, headers=conf.HEADER):
    """
    Async function to send GET request to API server
    :param url: API Endpoint
    :param headers: Headers to add to http request
    :return: JSON object on success, otherwise None
    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if 200 == resp.status:
                try:
                    return await resp.json()
                except aiohttp.ContentTypeError:
                    print('ERROR: unexpected data type')
            return None


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coroutines = [get_fact(get_random_url(server_rand=False)) for _ in range(conf.NUMBER_OF_FACTS_TO_GET)]
    results = loop.run_until_complete(asyncio.gather(*coroutines))

    for res in results[:]:
        if res is not None and not res['found']:
            # remove response object with 'found'=False
            results.remove(res)

    if conf.NUMBER_OF_FACTS_TO_GET > len(results):
        # might happen that fact is not found, then force server to generate any random fact
        coroutines = [get_fact(get_random_url(server_rand=True)) for _ in range(conf.NUMBER_OF_FACTS_TO_GET - len(results))]
        results_server_rand = loop.run_until_complete(asyncio.gather(*coroutines))
        results.extend(results_server_rand)

    for res in results:
        print(res)

