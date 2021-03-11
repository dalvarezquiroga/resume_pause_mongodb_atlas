<img src="/assets/pythonmasses.jpg">

# resume_pause_mongodb_atlas
Python script to resume/pause MongoDB Atlas clusters. It will use API from MongoDB Atlas to know the real name of the cluster with groupID.

Also it's important to know that it will use "AWS SSM Parameter Store" to save and read from script the credentials for each cluster.

## Getting Started

### Prerequisites

You have to have locally installed Python 3 *(Python 3.8 preferible)* as long as `pip3` ,  `git`.

Script return automatically and decrypt both MongoDB_keys using KMS.

So in your AWS account you need to create 2 parameters like this:

```
/name_of_cluster/mongodb-atlas-public-key
/name_of_cluster/mongodb-atlas-private-key
````

Example:

<img src="/assets/ssm_aws.png">

### Installing

To get this project Up and Running in your local environment you must follow this guide:

#### Clone the repository

```bash
$ git clone https://github.com/dalvarezquiroga/resume_pause_mongodb_atlas.git /tmp/app
Clonando en '/tmp/app'...
remote: Enumerating objects: 171, done.
remote: Counting objects: 100% (171/171), done.
remote: Compressing objects: 100% (115/115), done.
remote: Total 171 (delta 90), reused 110 (delta 52)
Recibiendo objetos: 100% (171/171), 23.92 KiB | 116.00 KiB/s, listo.
Resolviendo deltas: 100% (90/90), listo.
$ cd /tmp/app
```

#### Create a python 3.8 virtual environment

This projects runs using python 3.8 interprete so it's really important to create a virtual environment to run this application locally.

```bash
$ pwd
/tmp/app
$ virtualenv -p python3.8 .venv
Running virtualenv with interpreter /usr/bin/python3.8
Using base prefix '/usr'
New python executable in /tmp/app/.venv/bin/python3.8
Also creating executable in /tmp/app/.venv/bin/python
Installing setuptools, pip, wheel...
done.
$ source .venv/bin/activate
```

#### Installing development dependencies

In order to create your local environment ready to develop, please install the development dependencies:

```yaml
$ (.venv) pip3 install -r requirements.txt
```

## Usage

```bash
python3.8 mongodb_atlas_resume_pause_clusters.py  [name_of_cluster] [pause or resume]
```

<img src="/assets/pole.gif">

## Licence

MIT

## References

* https://docs.atlas.mongodb.com/configure-api-access/

* https://towardsdatascience.com/python-and-aws-ssm-parameter-store-7f0e211bb91e

* https://docs.atlas.mongodb.com/reference/api/clusters-modify-one/

David Álvarez Quiroga
