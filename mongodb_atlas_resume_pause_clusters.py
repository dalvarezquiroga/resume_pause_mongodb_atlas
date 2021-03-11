#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import boto3
import os
import sys
import requests
from requests.auth import HTTPDigestAuth

# Inicial configuration SSM client.
ssm = boto3.client("ssm")

# Empty dictionary that contains all {GROUP-ID}
dict_with_groupid_of_all_projects = {}

# Empty list that contains all real NAME from Clusters
list_with_real_name_of_cluster = []

# Empty list and TEMPORAL to convert response from dict_with_groupid_of_all_projects in a list to later create dict KEY, VALUE.
list_temporal_to_convert = []

# HEADERS
headers = {
    'Content-Type': 'application/json'
}

# BODY_WITH_TRUE
body_with_true = '{"paused": "true"}'

# BODY_WITH_FALSE
body_with_false = '{"paused": "false"}'

"""
  Function: mongodb_atlas_resume_pause_clusters.py
  Input: 1º Name of Cluster , 2º the action resume or pause.
  Output: Result of resume/pause.
  Descr: AWS Lambda that execute to PAUSE/RESUME MongoDB Atlas clusters.
"""

def get_mongodb_public_key_ssm_secret(name_of_cluster):
    return ssm.get_parameter(
        Name=f"/{(name_of_cluster)}/mongodb-atlas-public-key",
        WithDecryption=True
    )

def get_mongodb_private_key_ssm_secret(name_of_cluster):
    print(name_of_cluster)
    return ssm.get_parameter(
        Name=f"/{(name_of_cluster)}/mongodb-atlas-private-key",
        WithDecryption=True
    )

def handler():
  # WARNING: The name of the cluster_name should be the SAME name of AWS SYSTEM PARAMETER STORE SECRET.
  name_of_cluster_mongodb  = sys.argv[1]
  resume_or_pause_argument = sys.argv[2]

  # Call to funtion to get secrets.
  try:
    mongodb_public_key = get_mongodb_public_key_ssm_secret(name_of_cluster_mongodb)
    mongodb_private_key = get_mongodb_private_key_ssm_secret(name_of_cluster_mongodb)
  except:
    print ("ERROR getting SECRETS for SSM. Please check if you have permissions to access in EC2-role or local desktop")

  # Save Public key + Private key in a variable to later use --> SSM knows which key to use to decrypt the secret with.
  mongodb_public_key_decrypt = mongodb_public_key.get("Parameter").get("Value")
  mongodb_private_key_decrypt = mongodb_private_key.get("Parameter").get("Value")

  # We are going to do a request to GET all projects/{GROUP-ID} that MongoDB Atlas contains.
  req_get_all_project_url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"
  req_result_all_project = requests.get(req_get_all_project_url, headers=headers, verify=True, auth=HTTPDigestAuth(mongodb_public_key_decrypt, mongodb_private_key_decrypt), timeout=10)

  # We load response in JSON format.
  jsonResponse = json.loads(req_result_all_project.text)

  # We are going to filter to get group id from only name_of_cluster_mongodb previous introduced by argv in MongoDB Atlas.
  for name_complete in jsonResponse['results']:
    print(name_complete['name']) # List all names
    if name_of_cluster_mongodb in name_complete['name']:
      dict_with_groupid_of_all_projects.update({name_complete['name'] : name_complete['id']})
  print(dict_with_groupid_of_all_projects)

  # We are going to do request for each {GROUP-ID} to get {NAME} for each cluster.
  for group_id in dict_with_groupid_of_all_projects.values():
    req_get_each_project_url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{(group_id)}/clusters"
    req_result_each_project = requests.get(req_get_each_project_url, headers=headers, verify=True, auth=HTTPDigestAuth(mongodb_public_key_decrypt, mongodb_private_key_decrypt), timeout=10)
    jsonResponse_each_project = json.loads(req_result_each_project.text)
    list_with_real_name_of_cluster.append(jsonResponse_each_project['results'][0]['name'])

  print(list_with_real_name_of_cluster)

  # We are going to CONVERT first DICT with value that we need to LIST.
  for value in dict_with_groupid_of_all_projects.values():
    temporal = value
    list_temporal_to_convert.append(temporal)

  # We are going to create a new DICT with previous objects. We need two list.
  new_dictionary = dict(zip(list_with_real_name_of_cluster, list_temporal_to_convert))

  # We are going to iterate: For each REAL_NAME (KEY) and for each GROUP-ID (VALUE) get information about latest snapshots.
  if resume_or_pause_argument == 'pause':
    for key, value in new_dictionary.items():
      req_pause_cluster_url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{(value)}/clusters/{(key)}"
      req_result_pause_cluster_url = requests.patch(req_pause_cluster_url, headers=headers, verify=True, data=body_with_true, auth=HTTPDigestAuth(mongodb_public_key_decrypt, mongodb_private_key_decrypt))
      jsonResponse_pause_cluster_url = json.loads(req_result_pause_cluster_url.text)
      if(req_result_pause_cluster_url.status_code == 409) and ('Cannot pause a cluster that is already paused.' in req_result_pause_cluster_url.text):
        print ("ERROR : Cannot pause a cluster that is already paused.")
      else:
        print(jsonResponse_pause_cluster_url)

  elif resume_or_pause_argument == 'resume':
    for key, value in new_dictionary.items():
      req_pause_cluster_url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{(value)}/clusters/{(key)}"
      req_result_pause_cluster_url = requests.patch(req_pause_cluster_url, headers=headers, verify=True, data=body_with_false, auth=HTTPDigestAuth(mongodb_public_key_decrypt, mongodb_private_key_decrypt))
      jsonResponse_pause_cluster_url = json.loads(req_result_pause_cluster_url.text)
      if(req_result_pause_cluster_url.status_code == 200):
        print ("OK Starting MongoDB Cluster Atlas...")
      else:
        print(jsonResponse_pause_cluster_url)

handler()