""" Project specific configuration parameters """

BASE_URL = 'http://numbersapi.com/'
HEADER = {'Content-Type': 'application/json'}  # force api server to return json
RAND_NUM_MIN = -2147483648
RAND_NUM_MAX = 2147483647
TYPES = ['trivia', 'math', 'date', 'year']  # if omitted api server defaults to 'trivia'
FUNCTIONALITIES = ['none', 'fragment', 'notfound', 'default', 'min and max']
NOT_FOUND_CHOICES = ['default', 'floor', 'ceil']
DEFAULT_FACT = 'default fact'
NUMBER_OF_FACTS_TO_GET = 100  # define number of facts to get in parallel


def veriff_rand_num_ranges():
    global RAND_NUM_MIN, RAND_NUM_MAX
    if RAND_NUM_MIN > RAND_NUM_MAX:
        RAND_NUM_MIN = -2147483648
        RAND_NUM_MAX = 2147483647


veriff_rand_num_ranges()
