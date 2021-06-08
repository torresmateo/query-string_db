import pandas as pd
import os
from rich.progress import track
import requests
import argparse
aparser = argparse.ArgumentParser()
required_arguments = aparser.add_argument_group('required arguments')
required_arguments.add_argument('-g','--genes', help='file with one gene per line', required=True)
args = aparser.parse_args()

string_api_url = "https://string-db.org/api"
output_format = "tsv"
method = "interaction_partners"

remaining = set([g.strip() for g in open(args.genes)])

with open(f'{args.genes}.interactions', 'w', newline='\n') as f:
    for gene in track(remaining):
        request_url = "/".join([string_api_url, output_format, method])

        params = {

            "identifiers" : "%0d".join([gene]), # your protein
            #"species" : 9606, # species NCBI identifier 
            "limit" : 5000,
            "caller_identity" : "www.awesome_app.org" # your app name

        }
        response = requests.post(request_url, data=params)
        for line in response.text.strip().split("\n"):
            f.write(line + '\n')