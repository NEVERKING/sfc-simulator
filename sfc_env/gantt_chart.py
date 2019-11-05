# import datetime
# import gantt
#
# # Change font default
# gantt.define_font_attributes(fill='black', stroke='black', stroke_width=0, font_family="Verdana")
#
# # Add vacations for everyone
# gantt.add_vacations(datetime.date(2014, 12, 25))
# gantt.add_vacations(datetime.date(2015, 1, 1))
# gantt.add_vacations(datetime.date(2015, 1, 13))
#
# # Create two resources
# rANO = gantt.Resource('ANO')
# rJLS = gantt.Resource('JLS')
#
# # Add vacations for one lucky resource
# rANO.add_vacations(
#     dfrom=datetime.date(2014, 12, 29),
#     dto=datetime.date(2015, 1, 4)
#     )
# rANO.add_vacations(
#     dfrom=datetime.date(2015, 1, 6),
#     dto=datetime.date(2015, 1, 8)
#     )
#
# # Test if this resource is  avalaible for some dates
# print(rANO.is_available(datetime.date(2015, 1, 5)))
# print(rANO.is_available(datetime.date(2015, 1, 8)))
# print(rANO.is_available(datetime.date(2015, 1, 6)))
# print(rANO.is_available(datetime.date(2015, 1, 2)))
# print(rANO.is_available(datetime.date(2015, 1, 1)))
#
#
# # Create some tasks
# t1 = gantt.Task(name='tache1', start=datetime.date(2014, 12, 25), duration=4, percent_done=44, resources=[rANO], color="#FF8080")
# t2 = gantt.Task(name='tache2', start=datetime.date(2014, 12, 28), duration=6, resources=[rJLS])
# t7 = gantt.Task(name='tache7', start=datetime.date(2014, 12, 28), duration=5, percent_done=50)
# t3 = gantt.Task(name='tache3', start=datetime.date(2014, 12, 25), duration=4, depends_of=[t1, t7, t2], resources=[rJLS])
# t4 = gantt.Task(name='tache4', start=datetime.date(2015, 1, 1), duration=4, depends_of=t1, resources=[rJLS])
# t5 = gantt.Task(name='tache5', start=datetime.date(2014, 12, 23), duration=3)
# t6 = gantt.Task(name='tache6', start=datetime.date(2014, 12, 25), duration=4, depends_of=t7, resources=[rANO])
# t8 = gantt.Task(name='tache8', start=datetime.date(2014, 12, 25), duration=4, depends_of=t7, resources=[rANO, rJLS])
#
#
# # Create a project
# p1 = gantt.Project(name='Projet 1')
#
# # Add tasks to this project
# p1.add_task(t1)
# p1.add_task(t7)
# p1.add_task(t2)
# p1.add_task(t3)
# p1.add_task(t5)
# p1.add_task(t8)
#
#
#
# # Create another project
# p2 = gantt.Project(name='Projet 2', color='#FFFF40')
#
# # Add tasks to this project
# p2.add_task(t2)
# p2.add_task(t4)
#
#
# # Create another project
# p = gantt.Project(name='Gantt')
# # wich contains the first two projects
# # and a single task
# p.add_task(p1)
# p.add_task(p2)
# p.add_task(t6)
#
#
# # Test cases for milestones
# # Create another project
# ptcm = gantt.Project(name='Test case for milestones')
#
# tcm11 = gantt.Task(name='tcm11', start=datetime.date(2014, 12, 25), duration=4)
# tcm12 = gantt.Task(name='tcm12', start=datetime.date(2014, 12, 26), duration=5)
# ms1 = gantt.Milestone(name=' ', depends_of=[tcm11, tcm12])
# tcm21 = gantt.Task(name='tcm21', start=datetime.date(2014, 12, 30), duration=4, depends_of=[ms1])
# tcm22 = gantt.Task(name='tcm22', start=datetime.date(2014, 12, 30), duration=6, depends_of=[ms1])
# ms2 = gantt.Milestone(name='MS2', depends_of=[ms1, tcm21, tcm22])
# tcm31 = gantt.Task(name='tcm31', start=datetime.date(2014, 12, 30), duration=6, depends_of=[ms2])
# ms3 = gantt.Milestone(name='MS3', depends_of=[ms1])
#
#
# ptcm.add_task(tcm11)
# ptcm.add_task(tcm12)
# ptcm.add_task(ms1)
# ptcm.add_task(tcm21)
# ptcm.add_task(tcm22)
# ptcm.add_task(ms2)
# ptcm.add_task(tcm31)
# ptcm.add_task(ms3)
#
#
# p.add_task(ptcm)
#
#
# ##########################$ MAKE DRAW ###############
# p.make_svg_for_tasks(filename='./test_full.svg', today=datetime.date(2014, 12, 31), start=datetime.date(2014,8, 22), end=datetime.date(2015, 1, 14))
# p.make_svg_for_tasks(filename='./test_full2.svg', today=datetime.date(2014, 12, 31))
# p.make_svg_for_tasks(filename='./test.svg', today=datetime.date(2014, 12, 31), start=datetime.date(2015, 1, 3), end=datetime.date(2015, 1, 6))
# p1.make_svg_for_tasks(filename='./test_p1.svg', today=datetime.date(2014, 12, 31))
# p2.make_svg_for_tasks(filename='./test_p2.svg', today=datetime.date(2014, 12, 31))
# p.make_svg_for_resources(filename='./test_resources.svg', today=datetime.date(2014, 12, 31), resources=[rANO, rJLS])
# p.make_svg_for_tasks(filename='./test_weekly.svg', today=datetime.date(2014, 12, 31), scale=gantt.DRAW_WITH_WEEKLY_SCALE)
# ##########################$ /MAKE DRAW ###############

# import matplotlib.pyplot as plt
# import numpy as np
#
# ax = plt.gca()
# [ax.spines[i].set_visible(False) for i in ["top", "right"]]
#
#
# def gatt(m, t):
#     """甘特图
#     m机器集
#     t时间集
#     """
#     for j in range(len(m)):  # 工序j
#         i = m[j] - 1  # 机器编号i
#         if j == 0:
#             plt.barh(i, t[j])
#             plt.text(np.sum(t[:j + 1]) / 8, i, 'J%s\nT%s' % ((j + 1), t[j]), color="white", size=8)
#         else:
#             plt.barh(i, t[j], left=(np.sum(t[:j])))
#             plt.text(np.sum(t[:j]) + t[j] / 8, i, 'J%s\nT%s' % ((j + 1), t[j]), color="white", size=8)
#
#
# if __name__ == "__main__":
#     """测试代码"""
#     m = np.random.randint(1, 7, 35)
#     t = np.random.randint(15, 25, 35)
#     gatt(m, t)
#     plt.yticks(np.arange(max(m)), np.arange(1, max(m) + 1))
#     plt.show()


import numpy as np
import matplotlib.pyplot as plt

from param import args


def gatt(m, job, t):
    """甘特图
    m机器集
    job工序顺序集
    t时间集
    """
    for j in range(len(m)):  # 工序j
        i = m[j] - 1  # 机器编号i
        if j == 0:
            plt.barh(i, t[j])
            plt.text(np.sum(t[:j + 1]) / 8, i, 'J%s\nT%s' % ((job[j]), t[j]), color="white", size=8)
        else:
            plt.barh(i, t[j], left=(np.sum(t[:j])))
            plt.text(np.sum(t[:j]) + t[j] / 8, i, 'J%s\nT%s' % ((job[j]), t[j]), color="white", size=8)
    plt.yticks(np.arange(max(m)), np.arange(1, max(m) + 1))


def plot_gantt(env):
    """甘特图
    m机器集
    job工序顺序集
    t时间集
    """
    completed_sfcs = [s for s in env.completed_sfcs]
    failed_sfcs = [s for s in env.failed_sfcs]
    plt.rcParams['figure.dpi'] = 300  # 分辨率
    plt.rcParams['figure.figsize'] = (20.0, 10.0)  # 设置figure_size尺寸
    for s in completed_sfcs:
        for n in s.nodes:
            if n.start_time is not np.nan and n.vm_node is not None:
                # print('J%s V%s id%s v%s: start at %s, end at %s' % (
                #     s.idx, n.vnf_idx, n.idx, n.type, n.start_time,
                #     min(n.finish_time, n.sibling_finish_time, n.fail_time)))
                plt.barh(n.vm_node.idx,
                         min(n.finish_time, n.sibling_finish_time, n.fail_time) - n.start_time,
                         left=n.start_time
                         )
                plt.text(n.start_time, n.vm_node.idx, ' J%s V%s\nid%s\nv%s' % (s.idx, n.vnf_idx, n.idx, n.type),
                         color="black",
                         size=6)

    for s in failed_sfcs:
        for n in s.nodes:
            if n.start_time is not np.nan and n.vm_node is not None:
                # print('J%s V%s id%s v%s: start at %s, end at %s' % (
                #     s.idx, n.vnf_idx, n.idx, n.type, n.start_time,
                #     min(n.finish_time, n.sibling_finish_time, n.fail_time)))
                plt.barh(n.vm_node.idx,
                         min(n.finish_time, n.sibling_finish_time, n.fail_time) - n.start_time,
                         left=n.start_time
                         )
                plt.text(n.start_time, n.vm_node.idx, ' J%s V%s\nid%s\nv%s' % (s.idx, n.vnf_idx, n.idx, n.type),
                         color="black",
                         size=6)

    # for j in range(len(m)):  # 工序j
    #     i = m[j] - 1  # 机器编号i
    #     if j == 0:
    #         plt.barh(i, t[j])
    #         plt.text(np.sum(t[:j + 1]) / 8, i, 'J%s\nT%s' % ((job[j]), t[j]), color="white", size=8)
    #     else:
    #         plt.barh(i, t[j], left=(np.sum(t[:j])))
    #         plt.text(np.sum(t[:j]) + t[j] / 8, i, 'J%s\nT%s' % ((job[j]), t[j]), color="white", size=8)
    plt.yticks(np.arange(args.num_vm), np.arange(args.num_vm))
    plt.show()


if __name__ == "__main__":
    """测试代码"""
    m = np.random.randint(1, 7, 15)  # 生成工序所在机器编号
    job = np.arange(1, 16)  # 生成工序编号
    np.random.shuffle(job)
    t = np.random.randint(18, 25, 15)  # 生成工序时间
    gatt(m, job, t)
    plt.show()

# import plotly.figure_factory as ff

# def plot_gantt(env):
#     df = []
#     completed_sfcs = [s for s in env.completed_sfcs]
#     for s in completed_sfcs:
#         for n in s.nodes:
#             if n.start_time and n.vm_node:
#                 df.append(
#                     dict(Task='VM %s' % n.vm_node.idx,
#                          Start=str(n.start_time),
#                          Finish=str(min(n.finish_time, n.sibling_finish_time, n.fail_time)),
#                          Resource='Job %s' % n.sfc_dag.idx
#                          ))
#     r = lambda: random.randint(0, 255)
#     colors = []
#     for i in range(len(env.completed_sfcs)):
#         colors.append('#%02X%02X%02X' % (r(), r(), r()))
#
#     fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True,
#                           title='Job shop Schedule')
#     fig.show()
