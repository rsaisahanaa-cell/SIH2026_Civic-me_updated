RULES=[
 {'code':'SPCB-CONSENT','name':'Pollution Control Consent','authority':'State Pollution Control Board','sector':'Manufacturing','sla_days':30,'sequence':1,'documents':['Project Report','Land/Lease Proof','Process Flow','Water/Energy Details']},
 {'code':'FACTORY-LIC','name':'Factory / Industrial Establishment Licence','authority':'Factory Inspectorate','sector':'Manufacturing','sla_days':21,'sequence':2,'documents':['Site Plan','Machinery Layout','Occupier ID','Safety Plan']},
 {'code':'FIRE-NOC','name':'Fire Safety NOC','authority':'Fire & Emergency Services','sector':'Manufacturing','sla_days':15,'sequence':3,'documents':['Building Plan','Fire Safety Plan','Electrical Safety Certificate']},
 {'code':'FSSAI','name':'Food Safety Registration / Licence','authority':'Food Safety Department','sector':'Food Processing','sla_days':15,'sequence':2,'documents':['Premises Proof','Food Category Details','Water Test Report']},
 {'code':'ELECTRICAL','name':'Electrical Safety Approval','authority':'Electrical Inspectorate','sector':'Manufacturing','sla_days':14,'sequence':2,'documents':['Single Line Diagram','Load Details','Test Certificate']},
]
def applicable(profile):
 out=[]
 for r in RULES:
  if r['sector'] not in (profile.sector,'Any'): continue
  out.append(r)
 return sorted(out,key=lambda x:x['sequence'])
