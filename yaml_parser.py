# -*- coding: utf-8 -*-
import io
import yaml

data = yaml.safe_load(open('yml_example_files/defaults.yaml'))
url = data['url']


data2 = yaml.safe_load(open('gitlabCI_yml_example_files/.gitlab-ci.yml'))
stages = data2['stages']
job1 = data2['test-code-job2']
job1_script = job1['script']
#for s in job1_script:
#    print(s)

data3 = yaml.safe_load(open('gitlabCI_yml_example_files/apple_turicreate_gitlab-ci.yml'))
print(data3)