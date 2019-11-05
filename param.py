import argparse

parser = argparse.ArgumentParser()

# 系统中V M结点的数量
parser.add_argument('--num_vm', type=int, default=10,
                    help='Number of total virtual machines (default: 100)')
# 系统中初始的 SFC 数量
parser.add_argument('--num_init_sfc', type=int, default=20,
                    help='Number of initial SFC requests in system(default:100)')
# 最大 SFC 长度
parser.add_argument('--max_length', type=int, default=8,
                    help='Maximum length of Service Function Chain (default: 8)')
# 中途到达的 SFC 请求个数
parser.add_argument('--num_stream_dags', type=int, default=10,
                    help='number of streaming SFCs (default: 100)')
# 泊松到达过程的参数
parser.add_argument('--stream_interval', type=int, default=1,
                    help='inter job arrival time in milliseconds (default: 3)')
# 结点可靠性
parser.add_argument('--rel', type=float, default=0.99,
                    help='the reliability of a vm node (default: 0.99)')
# 学习率
parser.add_argument('--lr', type=float, default=0.001,
                    help='learning rate (default: 0.001)')
# SFC长度的均值
parser.add_argument('--len_avg', type=float, default=4,
                    help='Normal distribution mean of SFC length (default: 4)')
# SFC长度标准差
parser.add_argument('--len_sigma', type=float, default=3,
                    help='Normal distribution standard deviation of SFC length (default: 3)')
# Delta
parser.add_argument('--delta', type=float, default=2,
                    help='delta time (default: 2)')
# np.random seed
parser.add_argument('--seed', type=int, default=4,
                    help='numpy random seed (default: 4)')

reliable_list = [0.95, 0.99, 0.999, 0.9995]
# reliable_list = [0.1, 0.1, 0.1, 0.1]
workload_list = [400, 200, 160, 100, 300, 360, 420, 240]
speed_list = [5, 8, 10, 12]
speed_weights = [2, 3, 3, 2]

args = parser.parse_args()
