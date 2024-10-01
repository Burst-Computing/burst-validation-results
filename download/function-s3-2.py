import os
import time
from pprint import pprint
import boto3
import lithops
import sys


def my_map_function(id, total_workers):
    # id is the id of the function invocation (0..total_workers-1)
    # total_workers is the total number of function invocations
    s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='ASIASNA4IND7HJVX2U7A', aws_secret_access_key='pEzbXEWr9M7nHj/IUxaAjZSi8YSfB9QOT+/TwVbo', 
                      aws_session_token='IQoJb3JpZ2luX2VjELv//////////wEaCXVzLWVhc3QtMSJHMEUCIAOi/M4DZQeqDxIoUyAL67q2FcXRmTe1feWLILG8wktSAiEAvd8TFlz2ZaT5cJ1j6t32bY8gHwqkoYS5F2Snv2qJtYwq+AIIFBABGgwxNjU0MTU1MTIzMTgiDG578cV8ZvWv9/WHzyrVAnTUv6b+aCsI2bYS2oZz/BaGexJ8TbKqWTCz0PJ277Y0Lji4EGJ0osidzICfGg4v170igTn5di/Q/wsBapoEjaf5oTUQhhnJHVeEIvYjq4HE231wPik8xwmqn7qOVip0s/CNz9Gie6VE6r6qx2lLxgPbevpOaXs4f4TDsU4IYnLePiLNwMh4rWsWGiz0ZgnA+Xa0wNIEWa0INUy+qGKd0wW58jcO0luEIYJNJr4s7IA2TB2YVFdFs8hNcZyZ4btM0E/N917/00+sW3f234hM79fQ6cOK8FdRXwuyKjspSKcmAxpLIBn2HqMoiNXNJdCg430FGIRxrVVHGRr60VJc8jVQi978bcShNMWGPbKjNOEc1CT95mrSVeOBCYihgz4vgyLLJYo1xVph3laBg7k3BtmQ1076zfhRUcQP1CCO6awBkPnJIbw93UYQeVRuKNVkp5G4rgdMMOSR8qoGOqcBrhxDR4ho8ZBtrUxFf0qEddZBZEtLWGV3MnSn5oNUJcGT2Ea8irOihTrDqq+zaMbqPtpTZsP7pQn6ZC50MMVVfMkIGGvNSHGNJfiFj11VpHRUUqn/zObufKnLVoQ3eAwbxE0+yn35lbTnuUowSxzewv/v5BRQGkCrPB76NUxGwgyOu+FMxFiPGdIGY5KoJAqxDjTFl3uVyc17BeGPkEy7vqR+xXKUIkM=')
    start_time = time.time()
    # file_size = 1GB
    file_size = 1024*1024*1024
    print('Total workers: {}'.format(total_workers))
    # we want that eack worker download a different part of the file
    s3.get_object(Bucket='lithops-enrique', Key='1GB-0', Range='bytes={}-{}'.format(id//(48/total_workers) * file_size // total_workers, (id//(48/total_workers) + 1) * file_size // total_workers - 1))['Body'].read()
    end_time = time.time()
    download_time = end_time - start_time
    return {'start_time': start_time, 'end_time': end_time, 'download_time': download_time}


# gran from
if __name__ == "__main__":
    # fix upper line
    iterdata = [int(sys.argv[1]) for _ in range(48)]
    fexec = lithops.FunctionExecutor()
    fexec.map(my_map_function, iterdata)
    result = fexec.get_result()
    print(result)
    fexec.clean()
