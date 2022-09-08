
from ast import Return
from dataclasses import dataclass, is_dataclass
from datetime import date
from calendar import timegm
from hashlib import new
from tkinter import N
from google.protobuf.timestamp_pb2 import Timestamp
import numpy as np
import pandas as pd
import phenopackets

def nested_dataclass(*args, **kwargs):
    """Create a nested dataclass from other dataclasses	
    """
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__
        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                     new_obj = field_type(**value)
                     kwargs[name] = new_obj
            original_init(self, *args, **kwargs)
        cls.__init__ = __init__
        return cls
    return wrapper(args[0]) if args else wrapper

def get_timestamp(date_str):
    """Create Timestamp in seconds since Unix epoch
    from a date string, e.g, '1970-01-01'
    """

    y, m, d = tuple([int(i) for i in date_str.split("-")])
    timestamp = Timestamp(seconds = timegm(date(y, m, d).timetuple()))
    return timestamp


class PhenoIndividual(object):
    id: str
    alternate_ids: str
    date_of_birth: str
    time_at_last_encounter: int
    vital_status: str
    sex: int
    karyotypic_sex: str
    gender: str
    taxonomy: tuple
    
    def __init__(self, id):
        self.id = id
        self.alternate_ids = None
        self.date_of_birth = None
        self.time_at_last_encounter = None
        self.vital_status = None
        self.sex = None
        self.karyotypic_sex = None
        self.gender = None
        self.taxomony = None

    """
    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, new_id) -> None:
        self._id = new_id"""

    @property
    def alternate_ids(self):
        return self._alternate_ids
    
    @alternate_ids.setter
    def alternate_ids(self, new_ids):
        self._alternate_ids = new_ids
    
    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, new_date):
        if type(new_date) is str:
            self._date_of_birth = get_timestamp(new_date)
        else:
            self._date_of_birth = new_date
    
    @property
    def time_at_last_encounter(self):
        return self._time_at_last_encounter
    
    @time_at_last_encounter.setter
    def time_at_last_encounter(self, years):
        if type(years) is not property and years is not None:
            if not np.isnan(years):
                years = int(years)
                self._time_at_last_encounter = phenopackets.TimeElement(
                    age = phenopackets.Age(
                        iso8601duration = "P{0}Y".format(round(years))))
            else:
                self._time_at_last_encounter = None
        else:
            self._time_at_last_encounter = years

    @property
    def vital_status(self):
        return self._vital_status

    @vital_status.setter
    def vital_status(self, new_status):
        self._vital_status = new_status

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, new_sex):
        sex_dict = {'UNKNOWN_SEX': 0, 'FEMALE': 1, 'MALE': 2, 'OTHER_SEX': 3}
        if type(new_sex) is not property and new_sex is not None:
            if isinstance(new_sex, str):
                formatted_sex = sex_dict[new_sex.upper()]
            elif np.isnan(new_sex):
                formatted_sex = sex_dict["UNKNOWN_SEX"]
            else:
                raise TypeError("Unknown input type", type(new_sex), new_sex)
            self._sex = formatted_sex
        else:
            self._sex = new_sex

    @property
    def karyotypic_sex(self):
        return self._karyotypic_sex

    @karyotypic_sex.setter
    def karyotypic_sex(self, k_sex):
        k_sex_dict = {
            'UNKNOWN_KARYOTYPE': 0,# Untyped or inconclusive karyotyping
            'XX': 1,# Female
            'XY': 2,# Male
            'XO': 3,# Single X chromosome only
            'XXY': 4,# Two X and one Y chromosome
            'XXX': 5,# Three X chromosomes
            'XXYY': 6,# Two X chromosomes and two Y chromosomes
            'XXXY': 7,# Three X chromosomes and one Y chromosome
            'XXXX': 8,# Four X chromosomes
            'XYY': 9,# One X and two Y chromosomes
            'OTHER_KARYOTYPE': 10# None of the above types
        }
        if type(k_sex) is not property and k_sex is not None:
            k_sex = k_sex.upper()
            if k_sex in k_sex_dict.keys():
                self._karyotypic_sex = k_sex_dict[k_sex]
            else:
                self._karyotypic_sex = 10
        else:
            self._karyotypic_sex = k_sex
            
    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_gender):
        """
        param:
            new_gender(tuple): (label_in_str, ontology_in_str)
        """
        if type(new_gender) is not property and new_gender is not None:
            self._gender = phenopackets.OntologyClass(id = new_gender[1], 
                label = new_gender[0])
        else:
            self._gender = new_gender

    @property
    def taxonomy(self):
        return self._taxonomy
    
    @taxonomy.setter
    def taxonomy(self, new_taxonomy):
        if type(new_taxonomy) is not property and new_taxonomy is not None:
            self._taxonomy = phenopackets.OntologyClass(id = new_taxonomy[1], 
                label = new_taxonomy[0])
        else:
            self._taxonomy = new_taxonomy
        print(self._taxonomy)
 
def create_individual(id, alternate_ids = None, date_of_birth = None,
    time_at_last_encounter = None, vital_status = None, sex = None, 
    karyotypic_sex = None, gender = None, taxonomy = None):
    a = PhenoIndividual(id)
    for inp in list(locals().keys()):
        print(inp, a.taxomony)
        #if hasattr(a, inp):
        #print(hasattr(a, inp),locals()[inp],  ",,,,,,,,,,,,")
        setattr(a, inp, locals()[inp])
            #print(getattr(a, inp), "...........")
        """
        a.id = id
        a.alternate_ids = alternate_ids
        a.date_of_birth = date_of_birth
        a.time_at_last_encounter = time_at_last_encounter
        a.vital_status = vital_status
        a.sex = sex
        a.karyotypic_sex = karyotypic_sex
        a.gender = gender
        a.taxonomy = taxonomy"""
    return a

def read_file_xls_to_df(f):
    df = pd.read_excel(f, skiprows = 1)
    return df

def create_individual_from_df(df):
    a_s = []
    for index, row in df.iterrows():
        a = create_individual(
            id = row['Study Subject'], 
            time_at_last_encounter = row["Age-Years"],
            sex = row['Sex'],
            taxonomy = ("NCBITaxon:9606", "Homo sapiens"))
        a_s.append(a)
    return a_s

def convert_phenopackets(list_of_phenoindividual):
    new_indivs = []
    for indiv in list_of_phenoindividual:
        new_indiv = phenopackets.Individual()
        for k in indiv.__dict__:
            #print(k, '1')
            if k[0] == '_':
                k = k[1:]
                #print(k, '2')
            #if k in phenopackets.Individual.__dict__:
                #print(k, '3')
            if getattr(indiv, k) is not None:
                try :
                    setattr(new_indiv, k, getattr(indiv, k))
                except AttributeError as a:
                    if k == 'time_at_last_encounter': 
                        new_indiv.time_at_last_encounter = getattr(indiv, k)
                    elif k == 'taxonomy':
                        new_indiv.taxonomy = getattr(indiv, k)
            #print(new_indiv)
        print(new_indiv)
        new_indivs.append(new_indiv)
    return new_indivs

# main testing script
if __name__ == '__main__':

    #f = r'C:\Users\z370170\Projects\TWOC\phenopackets\create_phenopackets\python_pheno_dataclasses\TWOC-MultiOmics-Studies-COVID_300Samples (1).xlsx'
    #f = r'~/xomics/create_phenopackets/python_pheno_dataclasses/TWOC-MultiOmics-Studies-COVID_300Samples (1).xlsx'
    f = r"D:\CMBI_work\Projects\create_phenopackets\data\TWOC-MultiOmics-Studies-COVID_300Samples.xlsx"
    df = read_file_xls_to_df(f)
    a_s = create_individual_from_df(df)
    
    new_a_s = convert_phenopackets(a_s)
    #print(new_a_s)

    #for i in new_a_s:
     #   print(i, '!!!!!!!!!!!!!!!!!!!')
    """
    for i in a_s[0:2]:
        a = i.id
        b = i.sex
        print(a, b, "!!!!!!!!!!!!!!!!!")
        for j in i.__dict__:
            #j = j.replace('_', '')
            print(j)
            if hasattr(i, j):
                print(getattr(i, j))"""
    #b = [phenopackets.Individual_to_json(i) for i in a_s]
    #print(phenopackets.Individual.__dict__)
    #print(phenopackets.Individual.taxonomy)

