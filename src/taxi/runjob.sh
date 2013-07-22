#!/bin/bash

# 2 instances
# j-3RBP0QV3PJXKH


python mrfilter.py -r emr --emr-job-flow-id=j-3RBP0QV3PJXKH  -o "s3://mitbigdata/taxi/filtered" --no-output "s3://mitbigdata/taxi/sample.csv"
