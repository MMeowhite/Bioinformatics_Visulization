import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from mpl_toolkits.mplot3d import Axes3D  # 导入3D绘图工具
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import StandardScaler


class ClusterAlgorithm:

    def kmeans(self, X, n_clusters=3, title="KMeans Clustering Results with Cluster Boundaries",
               xlab="Feature 1", ylab="Feature 2", zlab=None, legend=True, file_name="kmeans.png", is_3d=False):
        # 创建KMeans模型
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)

        # 拟合模型
        model = kmeans.fit(X)

        # 获取聚类结果
        cluster_labels = kmeans.labels_
        cluster_centers = kmeans.cluster_centers_

        # 可视化聚类结果
        plt.figure(figsize=(10, 8))

        if is_3d:
            # 3D可视化
            ax = plt.axes(projection='3d')
            scatter = ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=cluster_labels, cmap='viridis', marker='o', edgecolor='k',
                                 alpha=0.6)
            ax.scatter(cluster_centers[:, 0], cluster_centers[:, 1], cluster_centers[:, 2], s=200, c='red', marker='X',
                       edgecolor='black', label='Cluster Centers')

            # 设置3D图表标题和标签
            ax.set_title(title)
            ax.set_xlabel(xlab)
            ax.set_ylabel(ylab)
            ax.set_zlabel(zlab)
        else:
            # 2D可视化
            scatter = plt.scatter(X[:, 0], X[:, 1], c=cluster_labels, cmap='viridis', marker='o', edgecolor='k',
                                  alpha=0.6)
            plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], s=200, c='red', marker='X', edgecolor='black',
                        label='Cluster Centers')

            # 设置2D图表标题和标签
            plt.title(title)
            plt.xlabel(xlab)
            plt.ylabel(ylab)

        if legend:
            plt.legend()

        if is_3d:
            plt.savefig(file_name)
        else:
            # 调整显示比例
            plt.axis('equal')
            plt.savefig(file_name)

        # 计算轮廓系数
        silhouette_avg = silhouette_score(X, cluster_labels)
        print(f"Silhouette Score: {silhouette_avg:.3f}")

        # 计算每个样本的轮廓系数
        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        # 可视化轮廓系数
        plt.figure(figsize=(8, 6))
        y_lower = 10
        for i in range(n_clusters):
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            plt.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values, facecolor='blue',
                              alpha=0.7)

            plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            y_lower = y_upper + 10

        plt.axvline(x=silhouette_avg, color="red", linestyle="--",
                    label=f"Average Silhouette Score ({silhouette_avg:.3f})")

        plt.title("Silhouette Plot for KMeans Clustering")
        plt.xlabel("Silhouette Coefficient")
        plt.ylabel("Cluster")
        plt.yticks([])
        plt.legend()
        plt.savefig(file_name + "_Silhouette_Plot.png")

        # 尝试不同的聚类数量
        wcss = []  # 聚类内平方和
        silhouette_scores = []

        for i in range(2, 11):
            kmeans = KMeans(n_clusters=i, random_state=42)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
            if i >= 2:
                silhouette_scores.append(silhouette_score(X, kmeans.labels_))

        # 绘制肘部法则图
        plt.figure(figsize=(12, 6))

        # WCSS图
        plt.subplot(1, 2, 1)
        plt.plot(range(2, 11), wcss, marker='o', linestyle='--')
        plt.title("Elbow Method")
        plt.xlabel("Number of Clusters")
        plt.ylabel("WCSS")

        # 轮廓系数图
        plt.subplot(1, 2, 2)
        plt.plot(range(2, 11), silhouette_scores, marker='o', linestyle='--')
        plt.title("Silhouette Scores")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Silhouette Score")

        plt.tight_layout()
        plt.savefig("clusters3.png")

        return model, cluster_labels, cluster_centers

    def hierarchy(self, X, n_clusters=3, title="Hierarchical Clustering Results with Dendrogram",
                  xlab="Feature 1", ylab="Feature 2", zlab=None, legend=True, file_name="hierarchy.png",
                  linkage_method='ward', distance_threshold=None):
        """
        层次聚类方法。

        参数:
        X : 输入数据
        n_clusters : 聚类数量
        title : 图表标题
        xlab : X轴标签
        ylab : Y轴标签
        zlab : Z轴标签（3D时使用）
        legend : 是否显示图例
        file_name : 保存的文件名
        is_3d : 是否是3D数据
        linkage_method : 层次聚类的链接方法
        distance_threshold : 距离阈值，用于截断聚类树
        """

        # 数据标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 计算层次聚类
        Z = linkage(X_scaled, method=linkage_method)

        # 截断聚类树，得到聚类标签
        cluster_labels = fcluster(Z, t=n_clusters, criterion='maxclust')
        print(f"Z: {Z}, cluster_labels: {cluster_labels}")

        # 可视化聚类结果
        plt.figure(figsize=(10, 8))

        scatter = plt.scatter(X[:, 0], X[:, 1], c=cluster_labels, cmap='viridis', marker='o', edgecolor='k',
                              alpha=0.6)
        plt.title(title)
        plt.xlabel(xlab)
        plt.ylabel(ylab)

        if legend:
            plt.legend()

        plt.savefig(file_name)

        # 绘制谱系图
        plt.figure(figsize=(10, 6))
        dendrogram(Z, truncate_mode='lastp', p=12, show_leaf_counts=True)
        plt.title('Dendrogram')
        plt.xlabel('Sample Index')
        plt.ylabel('Distance')
        plt.savefig(file_name + "_Dendrogram.png")

        # 计算轮廓系数
        silhouette_avg = silhouette_score(X, cluster_labels)
        print(f"Silhouette Score: {silhouette_avg:.3f}")

        # 计算每个样本的轮廓系数
        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        # 可视化轮廓系数
        plt.figure(figsize=(8, 6))
        y_lower = 10
        for i in range(n_clusters):
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            plt.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values, facecolor='blue',
                              alpha=0.7)

            plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            y_lower = y_upper + 10

        plt.axvline(x=silhouette_avg, color="red", linestyle="--",
                    label=f"Average Silhouette Score ({silhouette_avg:.3f})")

        plt.title("Silhouette Plot for Hierarchical Clustering")
        plt.xlabel("Silhouette Coefficient")
        plt.ylabel("Cluster")
        plt.yticks([])
        plt.legend()
        plt.savefig(file_name + "_Silhouette_Plot.png")

        # 尝试不同的聚类数量
        silhouette_scores = []

        for i in range(2, 11):
            cluster_labels = fcluster(Z, t=i, criterion='maxclust')
            silhouette_scores.append(silhouette_score(X, cluster_labels))

        # 绘制聚类数量与轮廓系数的关系图
        plt.figure(figsize=(8, 6))
        plt.plot(range(2, 11), silhouette_scores, marker='o', linestyle='--')
        plt.title("Number of Clusters vs Silhouette Score")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Silhouette Score")
        plt.savefig(file_name + "_Cluster_Silhouette.png")

        return cluster_labels


# 测试用例
if __name__ == '__main__':
    # 设置随机种子以确保结果可重复
    np.random.seed(42)

    # 生成模拟数据
    n_samples = 300  # 样本数量
    n_features = 3  # 特征数量
    n_clusters = 3  # 真实的聚类数量
    X, y = make_blobs(n_samples=n_samples, n_features=n_features, centers=n_clusters, cluster_std=1.5, random_state=42)
    print(X)

    # 可视化生成的数据
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap='viridis', marker='o', edgecolor='k')
    ax.set_title("Generated Data with True Labels")
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_zlabel("Feature 3")
    plt.savefig("clusters_data_3d.png")

    # 进行3D聚类分析
    # ClusterAlgorithm.kmeans(X, n_clusters=3, title="3D KMeans Clustering Results with Cluster Boundaries",
    #                         xlab="Feature 1", ylab="Feature 2", zlab="Feature 3", file_name="kmeans_3d.png",
    #                         is_3d=True)
    # 进行层次聚类分析
    cluster_algo = ClusterAlgorithm()
    cluster_algo.hierarchy(X, n_clusters=3, title="Hierarchical Clustering Results with Dendrogram",
                           xlab="Feature 1", ylab="Feature 2", zlab="Feature 3", file_name="hierarchy_3d.png",
                           is_3d=True, linkage_method='ward')