from cataloguer import cataloguer
from helpers.stack import Stack
from helpers.random_string import random_string
import concurrent.futures
import os
import json

# specify the files you want to upload in `search_term`
search_terms: list[str] = ['SEARCH TERM']

batch_size: int = 20 # number of files per upload batch
scope: str = "SCOPE" # Rucio scope to upload data to
rse: str = "RSE" # RSE to upload data to
max_containers: int = 10 # the maximum number of simultaneous containers to run


def upload(to_upload: list):

    container_id: str = random_string(10)
    dir: str = "working_dirs/" + container_id
    os.system("mkdir -p " + dir)
    os.system("cp dac-upload-tool-v2.sif " + dir + "/dac-upload-tool-v2.sif")

    path_list: list = []
    for file in to_upload:
        path_from_container = file.path
        path_list.append(path_from_container)
    path_string = str(path_list)[1:-1]    
    paths = path_string.replace(",", '')

    cmd = "apptainer exec working_dirs/" + container_id + "/dac-upload-tool-v2.sif rucio -v upload --scope " + scope + " --rse " + rse + " --impl gfal.NoRename --lifetime 3600 " + paths + " --register-after-upload --summary"
    print(cmd)
    os.system(cmd)
    
    os.system("rm -rf " + dir + "/dac-upload-tool-v2.sif")

    thread_summary_name: str = dir + "/rucio_upload.json"
    print(thread_summary_name)
    with open(thread_summary_name, 'r') as f:
        thread_summary = json.load(f)

    return thread_summary
    


if __name__ == "__main__":
    
    catalogue: Stack = cataloguer(search_terms)
    batches: list = []
    
    while catalogue.size() > 0:
        batch: list = catalogue.pop_many(batch_size)
        batches.append(batch)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_containers) as executor:
        results = executor.map(upload, batches)

    with open('summary.json', 'a') as summary:
        for i in results:
            json.dump(i, summary)

