#!/bin/bash
git clone https://gitlab.scai.fraunhofer.de/colin.birken/biodb_team_3.git
cd biodb_team_3
pip install -e .
python build.py $1