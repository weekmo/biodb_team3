### Installation
#### Using bash (install.sh):
Download install.sh

* On windows:

```bash
# Optional database path/name

install.sh [Database name]

# Or
bash install.sh [Database name]
```

* On linux:

```bash
# Optional database path/name
./install.sh [Database name]
```
Example:

```bash 
install.sh ../biodb.db
```

```python
from biodb_team_3.db_manager import Manager
m =Manager("biodb.db")
print(m.query_for_protein_single("101400"))
```
#### Other way
$git clone https://gitlab.scai.fraunhofer.de/colin.birken/biodb_team_3.git

$cd biodb_team_3/

$pip install -e .



### Working with the package in Python

- **now you can import and work with the project like so**:

```python
from biodb_team_3 import db_manager

#creates the manager which has all the database communication and creation methods
manager = db_manager.Manager()
```

- **to obtain the data and populate the database:**

```python
from biodb_team_3 import mapping_parser_v2
from biodb_team_3 import constants

data = mapping_parser_v2.get_data(constants.URL)
manager.populate_db(data)
```

- **to query the database for the diseases related to a Uniprot identifier:**

```python
print(manager.query_for_disease("P00352"))
```

- **to query the database for the proteins related to an OMIM identifier:**

```python
print(manager.query_for_proteins("101400"))
```

- **to save the output of a query as a pickled list object, simply add "True" as the second argument to the methods above, i.e.:**

```python
print(m.query_for_disease("P00352", True))
#Pickled result list dumped at: D:\LSI\Semester III\March seminars\biodb_team_3"
```

