import sys


from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np


def curce_data(x,y,y_pred):
    x = x.tolist()
    y = y.tolist()
    y_pred = y_pred.tolist()

    results = zip(x,y,y_pred)
    results = ["{},{},{}".format(s[0][0],s[1][0],s[2][0]) for s in results]
    return results

def read_data(path):
    with open(path) as f:
        lines =f.readlines()

    lines = [eval(line.strip()) for line in lines]
    X,y =zip(*lines)
    X =np.array(X)
    y= np.array(y)
    return X,y

X_train,y_train = read_data("train_data")
X_test,y_test = read_data("test_data")

model = LinearRegression()
model.fit(X_train,y_train)
print( model.coef_)
print(model.intercept_)

# 模型已经训练好了
y_pred_train = model.predict(X_train)
# sklearn 求 mse

train_mse = metrics.mean_squared_error(y_train,y_pred_train)
print("训练集MSE:",train_mse)


y_pred_test=model.predict(X_test)
test_mse = metrics.mean_squared_error(y_test,y_pred_test)


print("测试集MSE:",test_mse)

train_curve=curce_data(X_train,y_train,y_pred_train)
test_curve=curce_data(X_test,y_test,y_pred_test)
print("推广mse差", test_mse-train_mse)

print(train_curve)
print(test_curve)