import pandas as pd

data = pd.read_csv('D:\softwave engineer\scientific research\进展汇报\compacity.csv',encoding='gbk')

data = data.groupby(lambda x: data['research_id'][x]).first()

writer = pd.ExcelWriter('Documents_2/AdvMed.xlsx', engine='xlsxwriter')
data.to_excel(writer)

writer.save()
