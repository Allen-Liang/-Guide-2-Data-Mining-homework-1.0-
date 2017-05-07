import pandas as pd
df = pd.read_csv('Movie_Ratings.csv')
df = df.fillna(value=0)
#处理缺失值，将缺失值全部设为0
df.set_index("movie_name", drop=True, inplace=True)
users = df.to_dict(orient="dict")
#DataFrame转化为Dictionarys
#pandas.DataFrame.to_dict()用法API参考如下地址
#http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_dict.html

def manhattan(rating1, rating2):
    distance = 0
    commonRatings = False 
    for key in rating1:
        if key in rating2 and rating1[key] != 0 and rating2[key] !=0:
        	#如果缺失，则不计算两者的曼哈顿距离
            distance += abs(rating1[key] - rating2[key])
            commonRatings = True
    if commonRatings:
        return distance
    else:
        return -1

def computeNearestNeighbor(username, users):
	'''计算所有用户至username用户的距离，倒序排列并返回结果列表'''
	distances = []
	for user in users:
		if user != username:
			distance = manhattan(users[user], users[username])
			distances.append((distance, user))
    # 按距离排序——距离近的排在前面
	distances.sort()
	return distances

def recommend(username, users):	
    #返回距离最近的用户B推荐给用户A(没评价过的)没看过的
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
#print(df.fillna(value=0))
#print(users)
#print(users['Bryan'])
#print(manhattan(users['Josh'], users['Zwe']))
#print(computeNearestNeighbor("Josh", users)))
print( recommend('Josh', users))



