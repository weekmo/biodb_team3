from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .datamodel import Base, Protein, Disease, association_table
from .mapping_parser_v2 import get_data
from .constants import URL, CONNECTION

class Manager(object):
    """Class that hanldes the database. Has functions for populating the
    database as well as querying it."""

    def __init__(self, connection=None):
        if connection is None:
            connection = CONNECTION
        self.connection = connection
        self.engine = create_engine(self.connection)
        self.session_maker = sessionmaker(bind=self.engine, autoflush=False,
                                          expire_on_commit=False)
        self.session = self.session_maker()
        self.drop_tables()
        self.create_tables()
        self.proteins = {}

    def create_tables(self):
        """Create the empty database (tables)"""
        Base.metadata.create_all(self.engine, checkfirst=True)


    def drop_tables(self):
        """Drop all the tables in the database."""
        Base.metadata.drop_all(self.engine, checkfirst=True)


    def populate_db(self, data=None):
        """
        Populates database with disease - protein association data

        :param list of list data: Disease - protein association data, each single list begins with an OMIM id, followed by associated proteins' uniprot name and accession number
        """
        if data is None:
            data = get_data(URL)

        for line in data:
            proteins = []
            for i in range(1,len(line)-1, 2):
                proteins.append(self.create_protein(line[i], line[i+1]))
            disease = Disease(omim = line[0], proteins = proteins)
            self.session.add(disease)
        self.session.commit()

    def create_protein(self, uniprot_name, uniprot_accession):
        """
        If it doesn't exist, creates a protein object and returns

        :param str uniprot_name: Uniprot name
        :param str uniprot_accession: Uniprot accession number
        """
        protein = self.proteins.get(uniprot_accession)
        if not protein:
            protein = Protein(uniprot_name=uniprot_name, uniprot_accession=uniprot_accession)
            self.proteins[uniprot_accession] = protein
        return protein

    def find_protein(self, uniprot_accession):
        """
        Returns a protein name based on its accession

        :param str uniprot_accesion: Uniprot accession number
        :rtype str: Protein name
        """
        protein = self.session.query(Protein.uniprot_name).\
        filter(Protein.uniprot_accession == uniprot_accession)
        return(protein.one_or_none()[0])

    def introspectTables(self):

        md = MetaData()
        proteins = Table('proteins', md, autoload=True, autoload_with=self.engine)
        diseases = Table('diseases', md, autoload=True, autoload_with=self.engine)
        association = Table('association', md, autoload=True, autoload_with=self.engine)
        return(proteins, diseases, association)

    def query_for_protein_single(self, omim_id, pckl = False):
        """
        This function will take an omim ID and return a list of associated protein.
        It can also return/save the pickled list for downstream pipelines

        :param string omim_id: OMIM disease ID
        :rtype: list
        """

        protein = self.session.query(Protein.uniprot_accession).\
        join(association_table).\
        join(Disease).\
        filter(Disease.omim == omim_id)

        #executing the query and parsing the result as a list
        result = [id[0] for id in protein.all()]
        if pckl:
            #if pckl (pickled) flag is given, the pickled list object will be
            #dumped to the current working directory
            self.pickleIt(result)
        else:
            return result

    def query_for_disease_single(self, uniprot_id, pckl = False):
        """
        Takes an uniprot ID as input and returns OMIM IDs of the associated diseases.
        It can also return/save the pickled list for downstream pipelines

        :param string uniprot_id: Uniprot protein ID
        :rtype: list
        """

        disease = self.session.query(Disease.omim).\
        join(association_table).\
        join(Protein).\
        filter(Protein.uniprot_accession == uniprot_id)

        #executing the query and parsing the result as a list
        result = [id[0] for id in disease.all()]
        if pckl:
            #if pckl (pickled) flag is given, the pickled list object will be
            #dumped to the current working directory
            self.pickleIt(result)
        else:
            return result

    def pickleIt(self, obj):
        """
        This function dumps the given object as a pickled file to the current
        working directory and informs the user
        """
        import os
        import pickle
        currentWD = os.getcwd()
        with open(os.path.join(currentWD, "resultList"), "wb") as fileHandle:
            pickle.dump(obj, fileHandle)
        print("Pickled result list dumped at: {}".format(currentWD))

    def get_omim_id_with_uniprot_id(self, accessions):
        """Query the database with an uniprot accession and retrieve omim ids

        :param list accession: Uniprot accession
        """
        result = []
        for accession in accessions:
            prots = self.session.query(Protein).filter(Protein.uniprot_accession == accession).all()
            for protein in prots:
                result += [disease.omim for disease in protein.diseases]
        return result

    def get_uniprot_id_with_omim_id(self, accessions):
        """Query the database with an omim identifier to then retrieve uniprot
        accessions.

        :param list accession: OMIM identifier
        """
        result = []
        for accession in accessions:
            diseases = self.session.query(Disease).filter(Disease.omim == accession).all()
            for disease in diseases:
                result += [protein.uniprot_accession for protein in disease.proteins]
        return result

    def get_associated_disease_with_omim_id(self, omim_id):
        """Query associated(share associated proteins) diseases with given omim identifier

        :param str omim_id: OMIM identifier
        """
        associated_proteins_id = self.query_for_protein_single(omim_id)
        result = self.get_omim_id_with_uniprot_id(associated_proteins_id)
        return result

    def get_shared_associated_proteins_by_omim_ids(self, omim_ids):
        """Query shared associated proteins' id by a list of omim ids

        :param list omim_ids: OMIM identifiers
        """
        associated_protein_set_list = []
        for omim in omim_ids:
            associated_protein_set_list.append(set(self.query_for_protein_single(omim)))
        result = set.intersection(*associated_protein_set_list)
        return result
