import math
import sys
import random
import matplotlib.pyplot as plt
from CONSTANT import *
x = []
y = []
for i in range(n):
	x.append(random.randrange(5,95))
	y.append(random.randrange(5,95))
ans = []
a = x.copy()
b = y.copy()

def _sort(x,y):
	for i in range(len(x)):
		for j in range(len(x)-1):
			if x[j] > x[j+1]:
				a = x[j]
				b = y[j]
				x[j] = x[j+1]
				x[j+1] = a
				y[j] = y[j+1]
				y[j+1] = b
	ans.append([x[0],y[0]])
	ans.append([x[-1],y[-1]])
	return [x[0],y[0],x[-1],y[-1]]

def make_vec(x1,y1,x2,y2):
	return [(y2-y1),-(x2-x1)]

def distance(x0,y0,x1,y1,x2,y2,n):
	ans = abs(n[0]*x0 + n[1]*y0 - x1*n[0] - y1*n[1]) / math.sqrt(n[0]**2+n[1]**2)
	return round(ans,5)
	
def area(x1,y1,x2,y2,x3,y3):
	ans = abs((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1))/2
	return ans

def inside_are(x1,y1,x2,y2,x3,y3,x0,y0):
	a = area(x1,y1,x2,y2,x0,y0) + area(x1,y1,x3,y3,x0,y0) + area(x2,y2,x3,y3,x0,y0)
	if area(x1,y1,x2,y2,x3,y3)/a > 0.99:
		return True
	return False

def remove_line(x1,y1,x2,y2,n):
	i = 0
	while True:
		if n[0]*(x[i]-x1) + n[1] * (y[i]-y1) == 0:
			x.pop(i)
			y.pop(i)			
			i -= 1
		i +=1
		if i == len(x):
			break


def remove_area(x1,y1,x2,y2,x3,y3):
	if len(x) != 0:
		i = 0
		while True:
			if inside_are(x1,y1,x2,y2,x3,y3,x[i],y[i]):
				x.pop(i)
				y.pop(i)
				i-=1
			i+=1
			if i == len(x):
				break

def first_4_point(x1,y1,x2,y2):
	x_max_up = None
	y_max_up = None
	x_max_down = None
	y_max_down = None
	max_up = 0
	max_down = 0
	n = make_vec(x1,y1,x2,y2)
	remove_line(x1,y1,x2,y2,n)
	for i in range(len(x)):
		d = distance(x[i],y[i],x1,y1,x2,y2,n)
		if y[i] > (- n[0]*(x[i]-x1) / n[1]) + y1:
			if max_up < d:
				max_up = d
				x_max_up = x[i]
				y_max_up = y[i]
				i_max_up = i
		else:
			if max_down < d:
				max_down = d
				x_max_down = x[i]
				y_max_down = y[i]
				i_max_down = i
	if x_max_up != None:
		remove_area(x1,y1,x2,y2,x_max_up,y_max_up)
		ans.append([x_max_up, y_max_up])
	if x_max_down != None:
		remove_area(x1,y1,x2,y2,x_max_down,y_max_down)
		ans.append([x_max_down,y_max_down])
	return [x_max_up, y_max_up,x_max_down,y_max_down]

def _area(x1,y1,x2,y2, up):
	max_down = 0
	max_up = 0
	n = make_vec(x1,y1,x2,y2)
	if n[1] == 0:
		return False
	for i in range(len(x)):
		d = distance(x[i],y[i],x1,y1,x2,y2,n)
		if y[i] > (- n[0]*(x[i]-x1) / n[1]) + y1:
			if up:
				if max_up < d:
					max_up = d
					x_max_up = x[i]
					y_max_up = y[i]
					i_max_up = i
		else:
			if up == False:
				if max_down < d:
					max_down = d
					x_max_down = x[i]
					y_max_down = y[i]
					i_max_down = i
	if up:
		if max_up != 0:
			return [x_max_up, y_max_up]
		else:
			return False
	if not up:
		if max_down != 0:
			return [x_max_down, y_max_down]
		else:
			return False

def _areas(x1,y1,x2,y2,x3,y3, up):
	remove_area(x1,y1,x2,y2,x3,y3)
	left = _area(x1,y1,x3,y3,up)
	right = _area(x2,y2,x3,y3,up)
	if left != False:
		ans.append([left[0],left[1]])
		_areas(x1,y1,x3,y3,left[0],left[1],up)
	if right != False:
		ans.append([right[0],right[1]])
		_areas(x3,y3,x2,y2,right[0],right[1],up)

def graph(x,y, ans):
	ans.sort()
	A = ans[0]
	B = ans[-1]
	u = [B[0]-A[0], B[1]-A[1]]
	d = u[0]*A[1]-u[1]*A[0]

	up = []
	down = []
	down.append(ans[0])
	up.append(ans[0])
	for i in range(1,len(ans)-1):
		if ans[i][0]*u[1]-ans[i][1]*u[0]+d < 0:
			up.append(ans[i])
		else:
			down.append(ans[i])
	up.append(ans[-1])
	down.append(ans[-1])

	a_up = [up[i][0] for i in range(len(up))]
	b_up = [up[i][1] for i in range(len(up))]
	a_down = [down[i][0] for i in range(len(down))]
	b_down = [down[i][1] for i in range(len(down))]
	a = [ans[i][0] for i in range(len(ans))]
	b = [ans[i][1] for i in range(len(ans))]
	plt.scatter(x, y, color='green')
	plt.scatter(a,b, color='b')
	plt.plot(a_up, b_up, color='red')
	plt.plot(a_down, b_down, color='red')

	# setting x and y axis range
	plt.ylim(0,W)
	plt.xlim(0,H)
	  
	# naming the x axis
	plt.xlabel('x - axis')
	# naming the y axis
	plt.ylabel('y - axis')
	  
	# giving a title to my graph
	plt.title('Some cool customizations!')
	# function to show the plot
	plt.show()

if __name__ == "__main__":
	first_line = _sort(x,y)
	up_down_point = first_4_point(first_line[0],first_line[1],first_line[2],first_line[3])
	if up_down_point[0] != None:
		_areas(first_line[0],first_line[1],first_line[2],first_line[3],up_down_point[0],up_down_point[1], True)
	if up_down_point[2]!= None:
		_areas(first_line[2],first_line[3],first_line[0],first_line[1],up_down_point[2],up_down_point[3], False)
	graph(a,b, ans)