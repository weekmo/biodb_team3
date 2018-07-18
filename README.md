# BioDB Repository for Team-3
Working title under construction

## Abstract

In course of the BioDB Labcourse project we planned a framework to compare disease based on pathway and phenotype overlap. For this 3 databases need to be downloaded, structured and turned into easily queriable SQLite databases. A python package should provide the necessary functions.

![plan](biodb_figure.jpg)

#### Databases

The preliminary chosen databases are:
- **Uniprot (Team 3)**
- Wikipathways, Genenames(Team 2)
- Monarch (Team 1)


## Team task

We as team 3 need to design and implement a database, that connects diseases (OMIM ID's) to proteins (Uniprot accessions). The database should be easily queryable


## Steps of team project development

1- Choose the biomedical database and obtain raw data (txt)

2- Design and implement a data model in python (sqlalchemy)

3- provide a python package that handles querying the database

4- Query the database

4- Document the project (wiki page, doctest, comments)


## Current Workflow

- [x] Final decision on the protein database (Uniprot)
- [x] Plan data model
- [x] Download Uniprot data (CSV file)
- [x] Implement a function to parse the disease column of uniprot data csv-file
- [x] Parse: http://www.uniprot.org/docs/mimtosp.txt into a list
- [x] Implement the data model in sqlalchemy
- [x] Populate the database using sqlalchemy
- [x] Setup packages
- [x] Query functions
- [ ] Document the code (wiki page)


## Team-3 Members
- Mohammed
- (5 other students, names are hiden for privacy)
