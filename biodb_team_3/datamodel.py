from sqlalchemy import Table, Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('proteins_id', Integer, ForeignKey('proteins.id')),
    Column('diseases_id', Integer, ForeignKey('diseases.id'))
)

class Protein(Base):
    __tablename__ = 'proteins'

    id = Column(Integer, primary_key = True)
    uniprot_accession = Column(String, nullable=False, unique=True)
    uniprot_name = Column(String, nullable=False)

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True)
    omim = Column(String, nullable=False)
    proteins = relationship("Protein", secondary=association_table,
                            backref="diseases")
