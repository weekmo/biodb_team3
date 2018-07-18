import biodb_team_3 as bt3
import scipropath as bt2
import biodb_team_1 as bt1


class Interactor():

    def __init__(self):
        # create databases
        bt1.update(force_download=False)
        print("\n First database is created!")
        bt2.update()
        print("\n Second database is created!")
        bt3.update()
        print("\n Last database is created!")

        self.monarch_manager = bt1.create_manager()
        self.wikipathway_manager = bt2.create_manager()
        self.uniprot_manager = bt3.create_manager()


    def handle_path_prot_dict(self, pathway_dict):
        """Handles the dictionary provided by team 2 which has pathways has
        keys and lists of proteins as values"""
        for pathway in pathway_dict:
            # for the protein accessions get omim ids
            omim_ids = self.uniprot_manager.get_omim_id_with_uniprot_id(pathway_dict[pathway])
            pathway_dict[pathway] = omim_ids
        return pathway_dict

    def handle_path_omim_dict(self, pathway_dict):
        """Use team1 query to map omim id to disease name"""

        for pathway in pathway_dict:
            pathway_dict[pathway] = ["OMIM:" + x for x in pathway_dict[pathway]]
            # for the protein accessions get omim ids
            disease_names = self.monarch_manager.get_disease_names_with_omim_ids(pathway_dict[pathway])
            pathway_dict[pathway] = disease_names
        return pathway_dict

    def annotate_pathway(self, pathways):
        """Take uniprot ids connected to a pathway and annotate the pathway
        based on the diseases associas of the proteins."""

        pathway_protein_dict = self.wikipathway_manager.get_wikipathway_to_uniprot_mapping(pathways)
        path_omim_dict = self.handle_path_prot_dict(pathway_protein_dict)
        path_disease_dict = self.handle_path_omim_dict(path_omim_dict)

        for pathway in path_disease_dict:
            path_disease_dict[pathway] = set(path_disease_dict[pathway])
            path_disease_dict[pathway].remove(None)
        return path_disease_dict

    def double_annotate_pathway(self, omim_ids):
        """Annotate a pathway with disease information."""

        #prots = self.uniprot_manager.get_uniprot_id_with_omim_id(omim_ids)
        #path_prot_dict =
        #path_omim_dict = self.uniprot_manager.handle_pathway_dict(path_prot_dict)
        raise NotImplementedError

    def from_disease_to_pathway(self, diseases):
        """Takes OMIM identifiers and links this using proteins
        as intermediate step to pathways.
        """

        #proteins = self.uniprot_manager.get_uniprot_id_with_omim_id(diseases)
        #pathways = self.wikipathway_manager.    (proteins)
        #return pathways
        raise NotImplementedError

    def from_protein_to_disease(self, proteins):
        """Takes uniprot accession numbers and returns disease names.
        """

        omim = self.uniprot_manager.get_omim_id_with_uniprot_id(proteins)
        diseases = self.monarch_manager.get_disease_name_with_omim_id(omim)
        return diseases
