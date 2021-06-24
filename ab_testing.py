import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

ctrl_group = pd.read_excel("ab_testing_data.xlsx", sheet_name="Control Group")
test_group = pd.read_excel("ab_testing_data.xlsx", sheet_name="Test Group")


ctrl_group.info()
test_group.info()

ctrl_group.isnull().sum()
test_group.isnull().sum()

test_group.describe([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]).T
ctrl_group.describe([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]).T


ctrl_group["Group"] = "C"
test_group["Group"] = "T"


AB_test = pd.concat([ctrl_group,test_group],axis=0)
AB_test["Group"].value_counts()

############################
# Confidence Interval
############################
import statsmodels.stats.api as sms



sms.DescrStatsW(ctrl_group["Purchase"]).tconfint_mean()
sms.DescrStatsW(test_group["Purchase"]).tconfint_mean()


############################
# AB Testing
############################
from scipy.stats import shapiro



############################
# 1. Varsayım Kontrolü
############################

# 1.1 Normallik Varsayımı
# 1.2 Varyans Homojenliği

############################
# 1.1 Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_istatistigi, pvalue = shapiro(AB_test.loc[AB_test["Group"] == "C", "Purchase"])
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
#Test İstatistiği = 0.9773, p-değeri = 0.5891

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


test_istatistigi, pvalue = shapiro(AB_test.loc[AB_test["Group"] == "T", "Purchase"])
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
#Test İstatistiği = 0.9589, p-değeri = 0.1541


# A ve B gruplarımızda p value değerimiz 0.05 den küçük olmadığı için h0 reddedilmedi.
#Bu yüzden normal dağılım varsıyımı sağlanmaktadır.

############################
# 1.2 Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

from scipy import stats

stats.levene(AB_test.loc[AB_test["Group"] == "C", "Purchase"],
             AB_test.loc[AB_test["Group"] == "T", "Purchase"])

#LeveneResult(statistic=2.6392694728747363, pvalue=0.10828588271874791)
#p value değeri 0.05 den küçük olmadığı için h0 reddedilmedi.
#Varyanslar homojendir.



############################
# 2. Hipotezin Uygulanması
############################


# Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
test_istatistigi, pvalue = stats.ttest_ind(AB_test.loc[AB_test["Group"] == "C", "Purchase"],
                                           AB_test.loc[AB_test["Group"] == "T", "Purchase"],
                                           equal_var=True)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
#Test İstatistiği = -0.9416, p-değeri = 0.3493
#p value değeri 0.05 den küçük olmadığı için h0 reddedilmedi.












