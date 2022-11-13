import phenopackets
import pandas as pd
import numpy as np

class Pheno_individual(id):
    def __init__(self, id, sex, age, phenotypic_features):
        self.id = phenopackets.Individual[id]
        self.sex = phenopackets.Sex[sex]
        self.age = age
        self.taxonomy = phenopackets.OntologyClass(
            id = "NCBITaxon:9606", label = "Homo sapiens")
        self.phenotypic_features =  phenotypic_features

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, input_id):
        self._id = input_id

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, years):
        """Create Age object from age in years
        """
        if not np.isnan(years):
            self._age = phenopackets.TimeElement(
                age = phenopackets.Age(
                    iso8601duration = "P{0}Y".format(round(years))))
        else:
            self._age = None

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, input_sex):
        """Convert values for column 'Sex' to Phenopackets Sex
        https://phenopacket-schema.readthedocs.io/en/latest/sex.html#rstsex
        """
        if isinstance(input_sex, str):
            formatted_sex = input_sex.upper()
        elif np.isnan(input_sex):
            formatted_sex = "UNKNOWN_SEX"
        else:
            raise TypeError("Unknown input type", type(input_sex), input_sex)
        self._sex = formatted_sex

    @property
    def phenotypic_features(self):
        return self._phenotypic_features
    
    @phenotypic_features.setter
    def phenotypic_features(self, list_of_features):
        self._phenotypic_features = list_of_features
    

def read_file_csv_to_df(f):
    df = pd.read_csv(f)
    return df

def create_individual(df):
    """Create Phenopackets Individual from row.
    Also see phenopackets schema documentation
    https://phenopacket-schema.readthedocs.io/en/latest/individual.html#rstindividual
    """
    individuals = []
    for row in df.iterrows():
        individual = Pheno_individual()
        individual.id = row["Study Subject"]
        individual.age = row["Age-Years"]
        individual.sex = row["Sex"]
        individuals.append(individual)
    return individuals
