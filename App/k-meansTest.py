import time

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import os
import time

maxIter = 5  # 似乎对于时间的影响不大

isRandomData = True
isShowFigure = True

# 锁死线程为1 避免内存泄漏
# 但是写了之后还是有问题,这里说可以改环境变量
# 在conda里面用代码改就好 这代码训练和预测也用的这个
# 警告: UserWarning: KMeans is known to have a memory leak on Windows with MKL,
# when there are less chunks than available threads. You can avoid it by setting the environment variable OMP_NUM_THREADS=4.
# warnings.warn(
os.environ["OMP_NUM_THREADS"] = "1"

# packet = np.array([(1,1,1),(2,2,2),(3,3,3)])
if isRandomData:
    # 种子用来复现
    np.random.seed(42)
    # 随机生成一些三维点云数据
    data = np.random.rand(1000, 3) * 100
else:
    data = np.array([(1, 1, 1), (2, 2, 2), (3, 3, 3)])

# 可以加一个Canopy算法，这个作为预处理点云，但是T1 T2 必须要经过调参确定

# 初始化开始时间
init_start_time = time.time()
# 初始化KMeans模型 聚成3个类
kmeans = KMeans(n_clusters=3, max_iter=maxIter)
# 初始化结束时间
init_end_time = time.time()

# 推理开始时间
fit_start_time = time.time()
labels = kmeans.fit_predict(data)
# 推理结束时间
fit_end_time = time.time()
# 获取聚类中心点
centers = kmeans.cluster_centers_
if isShowFigure:

    # 使用Matplotlib绘制聚类结果的3D散点图
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 调整角度
    # 仰角 方位角
    ax.view_init(elev=20, azim=30)

    # 为每个聚类选择一个颜色
    colors = ['r', 'g', 'b']

    # 绘制每个点，颜色由其标签决定
    for i in range(len(data)):
        ax.scatter(data[i, 0], data[i, 1], data[i, 2], c=colors[labels[i]], marker='o')

    # 绘制聚类中心，用黑色的“X”标记表示
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], marker='x', c='black', s=300, linewidth=3)

    # 设置图表标题和坐标轴标签
    ax.set_title('3D Scatter Plot of KMeans Clustering')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    # 显示图表
    plt.show()
else:
    print(centers[0], centers[1], centers[2])
# 保存似乎有点问题 但是SciView能看，这个打印是相当的慢
# plt.savefig('./K-MeansTest.png')

# 计算初始化时间和推理时间
init_time = init_end_time - init_start_time
inference_time = fit_end_time - fit_start_time

print("KMeans初始化耗时：{:.2f}秒".format(init_time))
print("KMeans推理耗时：{:.2f}秒".format(inference_time))
print("KMeans迭代次数：{}".format(kmeans.n_iter_))
