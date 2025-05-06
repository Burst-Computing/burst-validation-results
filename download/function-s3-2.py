import os
import time
from pprint import pprint
import boto3
import lithops
import sys


def my_map_function(id, total_workers):
    # id is the id of the function invocation (0..total_workers-1)
    # total_workers is the total number of function invocations
    s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AKIASNA4IND7HTOF5TVP', aws_secret_access_key='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')
    start_time = time.time()
    # file_size = 1GB
    file_size = 1024*1024*1024
    print('Total workers: {}'.format(total_workers))
    # we want that eack worker download a different part of the file
    s3.get_object(Bucket='burstcomputing', Key='terasort-1g', Range='bytes={}-{}'.format(id//(48/total_workers) * file_size // total_workers, (id//(48/total_workers) + 1) * file_size // total_workers - 1))['Body'].read()
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
