import sys
from biodb_team_3.db_manager import Manager
m=None
if len(sys.argv) <2:
    m = Manager()
else:
    m = Manager(str(sys.argv[1]))
m.populate_db()
