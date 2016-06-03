__author__ = 'paulthompson'

import pandas as pd, numpy as np, matplotlib.pyplot as plt, six, sys, json, pprint
from pylab import *

pp = pprint.PrettyPrinter(indent=4)

df = pd.read_csv('OccupationSalaryByRegion.csv')

# print df.head(n=5)

occup_col = 'Occupational Title (2010 Standard Occupational Classification)'
abbrev_col = 'Occup Abbr'
MSA_col = 'Area Name'
medsal_col = 'Median Wage Annually'
df.sort_values(by = [medsal_col, MSA_col, occup_col])

Occups = df[occup_col].unique()
MSAs = df[MSA_col].unique()

# , subplotpars = subplots_adjust(
                    # wspace=10.0, hspace=10.0)

MSAdict = {}
plt.figure(figsize=(14,9))
for i, MSA in enumerate(MSAs):
    MSArows = df.loc[df[MSA_col] == MSA]
    MSArows = MSArows.loc[MSArows[occup_col] <> 'Total all occupations']
    occupations = list(MSArows['Occup Abbr'].values)
    ytickloc = np.arange(len(occupations))+.5
    employment = [int(Emp.replace(',','').strip()) / 1000 for Emp in MSArows['May 2014 Employment Estimates'].values]
    if i < 4:
        plt.subplot(2,2,i+1)
        subplots_adjust(left = .2, wspace=.7, hspace=.3)
        barh(ytickloc, employment, align='center')
        yticks(ytickloc, occupations)
        title(MSA)
        xlabel('Employment (thousands)')
# plt.savefig('Employment.png')
plt.show()

plt.figure(figsize=(12,8))
for i, MSA in enumerate(MSAs):
    MSArows = df.loc[df[MSA_col] == MSA]
    MSArows = MSArows.loc[MSArows[occup_col] <> 'Total all occupations']
    occupations = list(MSArows['Occup Abbr'].values)
    ytickloc = np.arange(len(occupations)) + .5
    employment = [int(Emp.replace('$','').replace(',','')) / 1000 for Emp in MSArows[medsal_col].values]
    if i < 4:
        plt.subplot(2,2,i+1)
        subplots_adjust(left = .2, wspace=.7, hspace=.3)
        barh(ytickloc, employment, align='center')
        yticks(ytickloc, occupations)
        title(MSA)
        xlabel('Median Salary by Occupation (thousands')
# plt.savefig('Salary.png')
plt.show()

for MSA in enumerate(MSAs):
    MSArows = df.loc[df[MSA_col] == MSA]
    occupList = MSArows[occup_col].unique()
    MSAdict[MSA] = {'Median Wage Annually': [], 'Employment Estimates': []}
    for occup in occupList:
        row = MSArows.loc[MSArows[occup_col] == occup]
        if occup != 'Total all occupations':
            occWageDict = {'Occupation': row[occup_col].values[0].replace(' Occupations',''),
                           'Wage': int(row[medsal_col].values[0].replace('$','').replace(',',''))}
            occEmpDict = {'Occupation': row[occup_col].values[0].replace(' Occupations',''),
                          'OccupAbbrev': row[abbrev_col].values[0].strip(),
                          'Employed': int(row['May 2014 Employment Estimates'].values[0].replace(',','').strip())}
            MSAdict[MSA]['Median Wage Annually'].append(occWageDict)
            MSAdict[MSA]['Employment Estimates'].append(occEmpDict)



print pp.pprint(MSAdict)

# with open('./WI_Income/dataByMSA.json', 'w') as fp:
#     json.dump(MSAdict, fp)

salary = pd.read_csv('MedianSalaryByRegion.csv')
Areas = list(salary['Area Name'].values)
Salaries = [int(sal) for sal in salary['Median Wage Annually'].values]
ytickloc = np.arange(len(Areas)) + .5

plt.figure()
barh(ytickloc, Salaries, align='center')
yticks(ytickloc, Areas)
title('Median Individual Salary By Area')
xlabel('Median Salary')
# plt.savefig('SalaryByArea.png')
plt.show()