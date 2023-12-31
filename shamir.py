from PIL import Image
import numpy as np
from scipy.interpolate import lagrange as lag

n = 5
r = 3
path = "test2.png"


def read_image(path):
    img = Image.open(path).convert('RGB')  # 打开彩色图像
    img_array = np.asarray(img)
    return img_array, img_array.shape


def polynomial(img, n, r):
    num_pixels = img.shape[0]
    coef = np.random.randint(low=0, high=256, size=(num_pixels, 3, r - 1))
    gen_imgs = []
    for i in range(1, n + 1):
        base = np.array([i ** j for j in range(1, r)])
        base = np.matmul(coef, base)
        img_ = img + base
        img_ = img_ % 256
        gen_imgs.append(img_)
    return np.array(gen_imgs)


def lagrange(x, y, num_points, x_test):
    # 所有的基函数值，每个元素代表一个基函数的值
    l = np.zeros(shape=(num_points,))

    # 计算第k个基函数的值
    for k in range(num_points):
        # 乘法时必须先有一个值
        # 由于l[k]肯定会被至少乘n次，所以可以取1
        l[k] = 1
        # 计算第k个基函数中第k_个项（每一项：分子除以分母）
        for k_ in range(num_points):
            # 这里没搞清楚，书中公式上没有对k=k_时，即分母为0进行说明
            # 有些资料上显示k是不等于k_的
            if k != k_:
                # 基函数需要通过连乘得到
                l[k] = l[k] * (x_test - x[k_]) / (x[k] - x[k_])
            else:
                pass
                # 计算当前需要预测的x_test对应的y_test值
    L = 0
    for i in range(num_points):
        # 求所有基函数值的和
        L += y[i] * l[i]
    return L


def decode(imgs, index, r, n):
    assert imgs.shape[0] >= r
    # print(imgs.shape)
    x = np.array(index)
    dim = imgs.shape[1]
    img = []
    for i in range(dim):
        if (i + 1) % 10000 == 0:
            print("decoding {} th pixel".format(i + 1))
        y = imgs[:, i, :]
        channel = []
        for j in range(3):
            poly = lag(x, y[:, j])
            pixel = poly(0) % 256
            channel.append(pixel)
        # print(x)
        # print(y)
        # pixel = lagrange(x, y, r, 0) % 251
        img.append(channel)
    return np.array(img)


if __name__ == "__main__":
    img, shape = read_image(path)  # 读取彩色图像
    img_flattened = img.reshape(-1, 3)  # 将彩色图像转换为一维数组
    gen_imgs = polynomial(img_flattened, n=n, r=r)
    to_save = gen_imgs.reshape(n, *shape)
    for i, img in enumerate(to_save):
        img = img.astype(np.uint8)
        Image.fromarray(img).save("test2_{}.jpeg".format(i + 1))

    origin_img = decode(gen_imgs[0:r, :], list(range(1, r + 1)), r=r, n=n)
    origin_img = origin_img.reshape(*shape)
    Image.fromarray(origin_img.astype(np.uint8)).save("test2_origin.jpeg")
