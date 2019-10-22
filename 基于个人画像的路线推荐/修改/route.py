import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import math
from multiprocessing import Pool

pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth',1000)



column = ['channel_name','user_id','trip_id','city_code','trip_time_start','trip_time_end','road_level_0','road_level_1','road_level_2','road_level_3','road_level_4',
		'road_level_6','road_level_8','road_two_way','toll_road','function_level_1','function_level_2','function_level_3','function_level_4',
		'function_level_5','elevated_road','non_invest','limit_StoE_0','limit_StoE_1','limit_StoE_2','limit_StoE_3','limit_StoE_4',
		'limit_EtoS_0','limit_EtoS_1','limit_EtoS_2','limit_EtoS_3','limit_EtoS_4','no_overtake','overtake','parking_road','nonparking_road',
		'split_road','lights_num','crossroads_num','road_len','limit_speed','lane','speed_mean','speed_max','speed_var']

column_new = ['limit_speed_50','limit_speed_100','limit_speed_150','limit_speed_200','limit_speed_250','limit_speed_300','limit_speed_350',
			'limit_speed_400','limit_speed_450','limit_speed_500','limit_speed_550','limit_speed_600','limit_speed_650','limit_speed_700',
			'limit_speed_800','limit_speed_900','limit_speed_1000','limit_speed_1100','limit_speed_1200',
			'lane_1','lane_2','lane_3','lane_4','lane_5','lane_6','lane_7','lane_8','lane_9','lane_10','lane_11','lane_12',
			'lane_13','lane_14','lane_15','lane_16']

column_var = ['var_1','var_2','var_3','var_4','var_5','var_6','var_7','var_8','var_9','var_10',
			'var_11','var_12','var_13','var_14','var_15','var_16','var_17','var_18','var_19','var_20',
			'var_21','var_22','var_23','var_24','var_25','var_26','var_27','var_28','var_29','var_30',
			'var_31','var_32','var_33','var_34','var_35','var_36','var_37','var_38','var_39','var_40',
			'var_41','var_42','var_43','var_44','var_45','var_46','var_47','var_48','var_49','var_50',
			'var_51','var_52','var_53','var_54','var_55','var_56','var_57','var_58','var_59','var_60',
			'var_61','var_62','var_63','var_64','var_65','var_66','var_67','var_68','var_69','var_70',
			'var_71','var_72','var_73','var_74','var_75','var_76','var_77','var_78']

def process(dic,file):
#处理原始数据
	
	column = ['channel_name','user_id','trip_id','city_code','trip_time_start','trip_time_end','road_level_0','road_level_1','road_level_2','road_level_3','road_level_4',
		'road_level_6','road_level_8','road_two_way','toll_road','function_level_1','function_level_2','function_level_3','function_level_4',
		'function_level_5','elevated_road','non_invest','limit_StoE_0','limit_StoE_1','limit_StoE_2','limit_StoE_3','limit_StoE_4',
		'limit_EtoS_0','limit_EtoS_1','limit_EtoS_2','limit_EtoS_3','limit_EtoS_4','no_overtake','overtake','parking_road','nonparking_road',
		'split_road','lights_num','crossroads_num','road_len','limit_speed','lane','speed_mean','speed_max','speed_var',
		'limit_speed_50','limit_speed_100','limit_speed_150','limit_speed_200','limit_speed_250','limit_speed_300','limit_speed_350',
			'limit_speed_400','limit_speed_450','limit_speed_500','limit_speed_550','limit_speed_600','limit_speed_650','limit_speed_700',
			'limit_speed_800','limit_speed_900','limit_speed_1000','limit_speed_1100','limit_speed_1200',
			'lane_1','lane_2','lane_3','lane_4','lane_5','lane_6','lane_7','lane_8','lane_9','lane_10','lane_11','lane_12',
			'lane_13','lane_14','lane_15','lane_16']
	df = pd.DataFrame(pd.read_csv('../trip_infos/'+dic+'/'+file,sep='#',header=None,names=column))

	for i in tqdm(df.index):
		limit_speed = df.loc[i,'limit_speed']
		for temp in limit_speed.split(';'):
			xx = temp.split(',')
			df.loc[i,'limit_speed_'+xx[0]]=xx[1]
		lane = df.loc[i,'lane']
		if type(lane)!=str:
			continue
		for temp in lane.split(';'):
			xx = temp.split(',')
			df.loc[i,'lane_'+xx[0]]=xx[1]
	
	df = df.fillna(0)
	df[column_new]=df[column_new].astype('float')
	for i in range(5):
		df['var_'+str(1+i)] = df['road_level_'+str(i)]/df['road_len']	
	df['var_6'] = df['road_level_6']/df['road_len']
	df['var_7'] = df['road_level_8']/df['road_len']
	# df['var_8'] = df['road_two_way']
	df['var_9'] = df['road_two_way']/df['road_len']
	# df['var_10'] = df['toll_road']
	df['var_11'] = df['toll_road']/df['road_len']
	for i in range(5):
		df['var_'+str(12+i)] = df['function_level_'+str(1+i)]/df['road_len']	
	df['var_17'] = df['non_invest']/df['road_len']
	df['var_18'] = df['elevated_road']/df['road_len']
	for i in range(5):
		df['var_'+str(23+i)] = df['limit_StoE_'+str(i)]/df['road_len']
	for i in range(5):	
		df['var_'+str(28+i)] = df['limit_EtoS_'+str(i)]/df['road_len']	
	df['var_33'] = df['no_overtake']/df['road_len']
	df['var_34'] = df['overtake']/df['road_len']
	df['var_35'] = df['parking_road']/df['road_len']
	df['var_36'] = df['nonparking_road']/df['road_len']
	df[['var_37','var_38','var_39']]=df[['speed_mean','speed_max','speed_var']]
	for i in range(14):
		df['var_'+str(40+i)] = df['limit_speed_'+str((i+1)*50)]/df['road_len']
	for i in range(5):
		df['var_'+str(54+i)] = df['limit_speed_'+str((i+8)*100)]/df['road_len']
	for i in range(16):
		df['var_'+str(59+i)] = df['lane_'+str(i+1)]/df['road_len']
	df[['var_75','var_76','var_77']]=df[['lights_num','road_len','crossroads_num']]
	df['var_78']=df['split_road']/df['road_len']
	df.to_csv('./trip_infos_new/'+dic+file+'.csv',index=False)

def merge():
#合并成新的文件
	column.extend(column_new)
	column.extend(column_var)
	df = pd.DataFrame(columns=column)
	for file in os.listdir('./trip_infos_new/'):
		dfx = pd.DataFrame(pd.read_csv('./trip_infos_new/'+file))			
		df = pd.concat([df,dfx],ignore_index=True)
		print(df.shape,dfx.shape)

	#去除轨迹数量少于60的用户
	column_var.append('user_id')
	df = df[column_var]
	df = df.sort_values(by = 'user_id',axis = 0,ascending = True)
	tmp = df['user_id'].value_counts()
	df = df[df['user_id'].isin(tmp[tmp>60].index)]	
	df.to_csv('./trip_infos.csv',index=False)
	
def corr():
#计算因子相关性，相关系数
	
	df = pd.DataFrame(pd.read_csv('./trip_infos.csv'))[column_var]
	df = df.corr().round(3)
	for i in df.columns:
		print(i,df.loc[(df[i]>0.7)|(df[i]<-0.5),:].index.values)
	df.to_excel('./因子相关性.xlsx')

def model_a():
#计算模型的权重
	df = pd.DataFrame(pd.read_csv('./trip_infos.csv'))
	var_drop=[8,10,11,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,37,38,39,42,58,77,78]
	var = [1,2,3,4,5,6,7,9,12,13,14,15,16,33,34,35,36,40,41,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,59,60,
			61,62,63,64,65,66,67,68,69,70,71,72,73,74]
	with open('./weight_1.txt','a+') as file:
		for user_id in df.drop_duplicates('user_id')['user_id']:
			dfx = df.loc[df['user_id']==user_id,:].drop(['user_id'],axis=1)
			tmp = [1-c for c in dfx.mean().values]
			# for c in dfx.mean().values:
			# 	tmp = 1-c

			# for i in var_drop:
			# 	tmp[i-1]=0
			tmp[15] = 0.532*tmp[15]
			tmp[74] = math.log(2-tmp[74],10)
			tmp[75] = math.log(1-tmp[75],10)
			#取出有效的特征
			tmp = [tmp[i-1] for i in var]
			# for i in var:
			# 	tmp=tmp[i-1]
			tmp.insert(7,1-tmp[7])
			# print(len(tmp))
			file.write(user_id+',')
			file.write(str(tmp))
			file.write('\n')
			



if __name__ == '__main__':

	# p=Pool(5)	
	# for dic in os.listdir('../trip_infos/'):
	# 	for file in os.listdir('../trip_infos/'+dic):
	# 		if file!='_SUCCESS':
	# 			p.apply_async(process, args=(dic,file,))
	# p.close()
	# p.join()

	# merge()
	model_a()
	# corr()
	# process('char_fact_20190530','part-00000')