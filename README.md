# Asynchronous API client for [NumbersAPI](http://numbersapi.com/)
        API URL structure: http://numbersapi.com/number/type?querystring
        Retrieves random fact based on randomly chosen 'type', 'number' and 'QUERY PARAMETER OPTIONS' supported by API endpoint.
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
