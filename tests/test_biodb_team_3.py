#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `biodb_team_3` package."""


import unittest
from biodb_team_3.db_manager import Manager
from biodb_team_3.mapping_parser_v2 import filter_text

class TestBiodb_team_3(unittest.TestCase):
    """Tests for `biodb_team_3` package."""

    def setUp(self):
        self.m=Manager("uniprot_disease.db")

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_query_for_protein_single(self):
        self.assertEqual(set(self.m.query_for_protein_single("101400")),set(['P21802','Q15672']))

    def test_query_for_disease_single(self):
        self.assertEqual(set(self.m.query_for_disease_single("Q15672")),set(['101400','123100','180750','601622']))

    def test_get_omim_id_with_uniprot_id(self):
        testlist=['101200','101400','101600','123150','123500','123790','149730','176943','207410','609579','614592','101400','123100','180750','601622']
        self.assertEqual(set(self.m.get_omim_id_with_uniprot_id(['P21802','Q15672'])),set(testlist))

    def test_get_uniprot_id_with_omim_id(self):
        testlist=['P21802','P11362','P21802']
        self.assertEqual(set(self.m.get_uniprot_id_with_omim_id(['614592','101600'])),set(testlist))
        
    def test_get_shared_associated_proteins_by_omim_ids(self):
        testlist={'Q15672'}
        self.assertEqual(set(self.m.get_shared_associated_proteins_by_omim_ids(["101400", "123100", "180750", "601622"])),set(testlist))
    
    def test_get_associated_disease_with_omim_id(self):
        testlist=['101200', '101400', '101600', '123150', '123500', '123790', '149730', '176943', '207410', '609579', '614592', '101400', '123100', '180750', '601622']
        self.assertEqual(set(self.m.get_associated_disease_with_omim_id("101400")),set(testlist))

    def test_filter_text(self):
        self.assertEqual(filter_text(None),False)


if __name__=="__main__":
    unittest.main()
