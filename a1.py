########################################
#
# @file 01logit.py
# @author: Michel Bierlaire, EPFL
# @date: Thu Sep  6 15:14:39 2018
#
# Logit model
# Three alternatives: Train, Car and Swissmetro
# SP data
#
#######################################

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio

pandas = pd.read_table("tripdata.dat")
database = db.Database("tripdata",pandas)

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

from headers import *

# Removing some observations can be done directly using pandas.
#remove = (((database.data.PURPOSE != 1) & (database.data.PURPOSE != 3)) | (database.data.CHOICE == 0))
#database.data.drop(database.data[remove].index,inplace=True)

# Here we use the "biogeme" way for backward compatibility
#exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) +  ( CHOICE == 0 )) > 0
#database.remove(exclude)


ASC_AUTO_DRIVE = Beta('ASC_AUTO_DRIVE',0,None,None,0)
ASC_AUTO_PASS = Beta('ASC_AUTO_PASS',0,None,None,0)
ASC_METRO = Beta('ASC_METRO',0,None,None,0)
ASC_TRAIN = Beta('ASC_TRAIN',0,None,None,0)
ASC_WALK = Beta('ASC_WALK',0,None,None,0)

B_IVTT = Beta('B_IVTT',0,None,None,0)

#SM_COST =  SM_CO   * (  GA   ==  0  ) 
#TRAIN_COST =  TRAIN_CO   * (  GA   ==  0  )

#CAR_AV_SP =  DefineVariable('CAR_AV_SP',CAR_AV  * (  SP   !=  0  ),database)
#TRAIN_AV_SP =  DefineVariable('TRAIN_AV_SP',TRAIN_AV  * (  SP   !=  0  ),database)

#TRAIN_TT_SCALED = DefineVariable('TRAIN_TT_SCALED',\
#                                 TRAIN_TT / 100.0,database)
#TRAIN_COST_SCALED = DefineVariable('TRAIN_COST_SCALED',\
#                                   TRAIN_COST / 100,database)
#SM_TT_SCALED = DefineVariable('SM_TT_SCALED', SM_TT / 100.0,database)
#SM_COST_SCALED = DefineVariable('SM_COST_SCALED', SM_COST / 100,database)
#CAR_TT_SCALED = DefineVariable('CAR_TT_SCALED', CAR_TT / 100,database)
#CAR_CO_SCALED = DefineVariable('CAR_CO_SCALED', CAR_CO / 100,database)

V1 = ASC_AUTO_DRIVE + \
     B_IVTT * ivtt1
V2 = ASC_AUTO_PASS + \
     B_IVTT * ivtt2
V3 = ASC_METRO + \
     B_IVTT * ivtt3
V4 = ASC_TRAIN + \
     B_IVTT * ivtt4
V5 = ASC_WALK + \
     B_IVTT * ivtt5

# Associate utility functions with the numbering of alternatives
V = {1: V1,
     2: V2,
     3: V3,
     4: V4,
     5: V5}

# Associate the availability conditions with the alternatives

av = {1: avail1,
      2: avail2,
      3: avail3,
      4: avail4,
      5: avail5}

logprob = bioLogLogit(V,av,choice)
biogeme  = bio.BIOGEME(database,logprob) # This is my log likelihood function
biogeme.modelName = "A1Practice"
results = biogeme.estimate()

# Print the estimated values
betas = results.getBetaValues()
for k,v in betas.items():
    print(f"{k}=\t{v:.3g}")

# Get the results in a pandas table
pandasResults = results.getEstimatedParameters()
print(pandasResults)