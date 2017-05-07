import pandas as pd
from math import sqrt
df = pd.read_csv('Movie_Ratings.csv')
df = df.fillna(value=0)
#处理缺失值，将缺失值全部设为0
df.set_index("movie_name", drop=True, inplace=True)
users = df.to_dict(orient="dict")
#DataFrame转化为Dictionarys
#pandas.DataFrame.to_dict()用法API参考如下地址
#http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_dict.html
def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2 and rating1[key] != 0 and rating2[key] !=0:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator



def computeNearestNeighbor(username, users):
	'''计算所有用户至username用户A的pearson相关系数，降序排列并返回结果列表'''
	coefficients = []
	for user in users:
		if user != username:
			coefficient = pearson(users[user], users[username])
			coefficients.append((coefficient, user))
    # 按pearson系数降序排列
	coefficients.sort(reverse = True)
	return coefficients

def recommend(username, users):	
    #返回相关系数最大的用户B推荐给用户A(没评价过的)没看过的
    nearest = computeNearestNeighbor(username, users)[0][1]
    recommendations = []
    neighborRatings = users[nearest]
    #最近用户B的电影评分列表
    userRatings = users[username]
    #用户A的电影评分列表
    for movies in neighborRatings:
        if  movies in userRatings and neighborRatings[movies] != 0 and userRatings[movies] ==0:
            #在电影字典中，找到最近用户B看过的（评分的）和用户A没看过的（没评过分的）,推荐给用户A
            recommendations.append((movies, neighborRatings[movies]))
    #将结果存储到列表中
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)

#mytest
#print(pearson(users['Bryan'], users['Zwe']))
#print(computeNearestNeighbor("Josh", users))
print( recommend('Josh', users))



