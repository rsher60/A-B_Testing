# Import the libraries
import pandas as pd
import numpy as np
import math
import scipy.stats as stats

# read the data using pandas
df = pd.read_csv('medium_ab_test.csv',usecols=['COOKIE_ID','CONVERTED', \
                'ENGAGEMENT_SCORE','TREATMENT_OR_CONTROL']  )
df.head()


df_pre = df.groupby('COOKIE_ID')['CONVERTED'].sum().to_frame().reset_index()
a= df_pre[df_pre['CONVERTED'] > 1]['COOKIE_ID'].index
df_final = df[~df.index.isin(df_pre[df_pre['CONVERTED'] > 1]['COOKIE_ID'].index)]
df_final.head()

# this dataframe has no duplicates and the cookie is either exposed to treatment
# or control group.

# pivot calculation ( 1 - cookie clicked on the click to chat button , 0 -
# did not click on the click to chat button)
pd.crosstab(df_final['TREATMENT_OR_CONTROL'] , df_final['CONVERTED'])

import math

def ABTest_sample_size(p1,mde,alpha,beta, n_side):
  """
  Parameters:
  p1 :"Baseline conversion Rate"
  mde : "Minimum detectable Effect"
  alpha : significance level
  beta : "statistical power"
  n_side:"two tailed t-test or 1 tail t-test"
  """
  p2 = p1+mde
  z_crit = stats.norm.ppf(alpha/n_side)
  z_crit2 = stats.norm.ppf(1-beta)
  n_sample = ( (z_crit*(math.sqrt(2*p1*(1-p1)))) + (z_crit2*(math.sqrt((p1*(1-p1))+(p2*(1-p2)))) )       )**2 / mde**2

  return math.ceil(n_sample)

#calcualate the sample size using the above function

"""
our base line conversion rate as mentioned in the business case is 5.05%
the mde or minimum detectable effect is 1%
the 
"""
n_required = ABTest_sample_size(0.0505,0.01,0.05,0.80,2)

from pandas.core.common import random_state

controlGroup_sample = df_final[df_final['TREATMENT_OR_CONTROL']=='CONTROL'].sample(n=n_required,random_state=242)
treatmentGroup_sample = df_final[df_final['TREATMENT_OR_CONTROL']=='TREATMENT'].sample(n=n_required,random_state=242)
ab_testfinal = pd.concat([controlGroup_sample , treatmentGroup_sample],axis=0)
ab_testfinal.reset_index(drop=True,inplace=True)

ab_testfinal.info()

pd.crosstab(ab_testfinal['TREATMENT_OR_CONTROL'],ab_test['CONVERTED'])

from statsmodels.stats.proportion import proportions_ztest, proportion_confint

controlGroup_results = ab_testfinal[ab_testfinal['TREATMENT_OR_CONTROL'] == 'CONTROL']['CONVERTED']
treatmentGroup_results = ab_testfinal[ab_testfinal['TREATMENT_OR_CONTROL'] == 'TREATMENT']['CONVERTED']

n_control = controlGroup_results.count()
n_treatment = treatmentGroup_results.count()
successes = [controlGroup_results.sum(), treatmentGroup_results.sum()]
nobs = [n_control, n_treatment]

z_statistic, pval = proportions_ztest(successes, nobs=nobs)


# function to calculate the confidence interval and evaluate the practical significance
def ci_calculator(x, N, alpha, n_side):
    """
    x= success cases
    N = total sample size
    alpha = significance level
    n_side = one tail or two tailed test

    """

    _p = x / N
    if ((_p * N < 5) or ((1 - _p) * N < 5)):
        raise ValueError('the distribution cannot be assumed as normal')
    else:
        m = stats.norm.ppf(alpha / n_side) * math.sqrt((_p * (1 - _p)) / N)
    return f'[{_p + m:.3f} , {_p - m:.3f}]'


control_ci = ci_calculator(567, 7734, 0.05, 2)  # 567 conversions and sample size 7734
treatment_ci = ci_calculator(645, 7734, 0.05, 2)  # 645 conversions and sample size 7734

print(f'p-value: {pval:.3f}')
print(f'ci 95% for control group: {control_ci}')
print(f'ci 95% for treatment group: {treatment_ci}')

