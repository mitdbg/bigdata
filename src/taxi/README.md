
Running locally

    for f in $(ls Hackathon*.zip); do python mrfilter.py ${f:0:$(( ${#f}-4 ))}.csv; done