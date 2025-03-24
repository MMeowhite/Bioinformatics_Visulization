import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from lifelines import CoxPHFitter
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


class RegressionAnalysis:
    def __init__(self, args, data):
        self.args = args
        self.data = data
        # self.file_name = args.file_name if hasattr(args, 'file_name') else 'regression_results.png'
        # self.dpi = args.dpi if "dpi" in args else 300

    def linear_regression(self):
        print(f"data: {self.data}")

        # 线性回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        columns_number = len(self.data.columns)
        X = self.data.iloc[:, :columns_number - 1]
        y = self.data.iloc[:, -1]

        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print("Linear Regression Results:")
        print(f"Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared: {r2:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title("Actual vs Predicted Values (Linear Regression)")
        plt.savefig("1.png", dpi=300)

        return model

    def polynomial_regression(self, degree=2):
        # 多项式回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        X = self.data.iloc[:, :len(self.data.columns) - 1]
        y = self.data.iloc[:, -1]
        print(f"X.shape: {X}")
        print(f"y.shape: {y}")

        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)

        model = LinearRegression()
        model.fit(X_poly, y)

        y_pred = model.predict(X_poly)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print(f"Polynomial Regression (degree={degree}) Results:")
        print(f"Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared: {r2:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Actual vs Predicted Values (Polynomial Regression, degree={degree})")
        plt.savefig("2.png", dpi=300)

        return model

    def logistic_regression(self, data):
        # 逻辑回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        X = self.data.iloc[:, :len(self.data.columns) - 1]
        y = self.data.iloc[:, -1]

        model = LogisticRegression()
        model.fit(X, y)

        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)

        print("Logistic Regression Results:")
        print(f"Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")
        print(f"Accuracy: {accuracy:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(y)), y, alpha=0.7, label='Actual')
        plt.scatter(range(len(y_pred)), y_pred, alpha=0.7, label='Predicted')
        plt.xlabel("Sample Index")
        plt.ylabel("Class Label")
        plt.title("Actual vs Predicted Values (Logistic Regression)")
        plt.legend()
        plt.savefig("3.png", dpi=300)

        return model

    def cox_regression(self, data):
        # Cox回归
        # Cox回归需要生存时间和事件指示
        # 假设数据框中有'T'（生存时间）和'E'（事件指示）列
        if "T" or "E" not in self.data.columns:
            raise ValueError("Missing T or E column in data")
        df = pd.DataFrame(X)
        df['T'] = data['T']
        df['E'] = data['E']

        cph = CoxPHFitter()
        cph.fit(df, duration_col='T', event_col='E')

        print("Cox Regression Results:")
        print(cph.summary)

        return cph

    def ridge_regression(self, data, alpha=1.0):
        # 岭回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        X = self.data.iloc[:, :len(self.data.columns) - 1]
        y = self.data.iloc[:, -1]

        model = Ridge(alpha=alpha)
        model.fit(X, y)

        y_pred = model.predict(X)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print(f"Ridge Regression (alpha={alpha}) Results:")
        print(f"Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared: {r2:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Actual vs Predicted Values (Ridge Regression, alpha={alpha})")
        plt.savefig("3.png", dpi=300)

        return model

    def lasso_regression(self, alpha=1.0):
        # Lasso回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        X = self.data.iloc[:, :len(self.data.columns) - 1]
        y = self.data.iloc[:, -1]

        model = Lasso(alpha=alpha)
        model.fit(X, y)

        y_pred = model.predict(X)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print(f"Lasso Regression (alpha={alpha}) Results:")
        print(f"Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared: {r2:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Actual vs Predicted Values (Lasso Regression, alpha={alpha})")
        plt.savefig("4.png", dpi=300)

        return model

    def random_forest_regression(self, n_estimators=100):
        # 随机森林回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        X = self.data.iloc[:, :len(self.data.columns) - 1]
        y = self.data.iloc[:, -1]

        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        model.fit(X, y)

        y_pred = model.predict(X)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print(f"Random Forest Regression (n_estimators={n_estimators}) Results:")
        print(f"Feature Importances: {model.feature_importances_}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared: {r2:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Actual vs Predicted Values (Random Forest Regression, n_estimators={n_estimators})")
        plt.savefig("5.png", dpi=300)

        return model

    def support_vector_regression(self, kernel='rbf'):
        # 支持向量回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        X = self.data.iloc[:, :len(self.data.columns) - 1]
        y = self.data.iloc[:, -1]

        model = SVR(kernel=kernel)
        model.fit(X, y)

        y_pred = model.predict(X)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print(f"Support Vector Regression (kernel={kernel}) Results:")
        print(f"Support Vectors: {model.support_vectors_.shape[0]}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared: {r2:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title(f"Actual vs Predicted Values (Support Vector Regression, kernel={kernel})")
        plt.savefig("6.png", dpi=300)

        return model

    def decision_tree_regression(self):
        # 决策树回归
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("data must be a pd.DataFrame object")
        X = self.data.iloc[:, :len(self.data.columns) - 1]
        y = self.data.iloc[:, -1]

        model = DecisionTreeRegressor(random_state=42)
        model.fit(X, y)

        y_pred = model.predict(X)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print("Decision Tree Regression Results:")
        print(f"Feature Importances: {model.feature_importances_}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared: {r2:.2f}")

        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title("Actual vs Predicted Values (Decision Tree Regression)")
        plt.savefig("7.png", dpi=300)

        return model


# 测试用例
if __name__ == '__main__':
    # 示例数据
    np.random.seed(42)
    X = np.random.rand(100, 2)
    y = 2 * X[:, 0] + 3 * X[:, 1] + np.random.randn(100)

    # 将数据转换为 DataFrame
    data = pd.DataFrame(X, columns=['Feature1', 'Feature2'])
    data['y'] = y

    print(data.head())


    # 线性回归
    reg_tool = RegressionAnalysis(None, data)
    reg_tool.linear_regression()

    # 多项式回归
    reg_tool.polynomial_regression(degree=3)

    # 岭回归
    reg_tool.ridge_regression(data,alpha=0.5)

    # Lasso回归
    reg_tool.lasso_regression(alpha=0.1)

    # 随机森林回归
    reg_tool.random_forest_regression()

    # 支持向量回归
    reg_tool.support_vector_regression(kernel='linear')

    # 决策树回归
    reg_tool.decision_tree_regression()