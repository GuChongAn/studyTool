import click
import time
import datetime
import csv
import os
path = r"D:/Desktop/考研复习/总结规划/studyTool/data"

# 任务与奖励-设置任务
# 设置任务和完成任务的奖励，并保存，保存格式
# 任务类型 \t 任务内容 \t 任务奖励
# work_type \t work_cnt \t work_reward
def set_work():
    temp_path = os.path.join(path, 'work_data.txt')
    work_type = input("请输入任务类型（日常、成就、单次）：\n")
    work_cnt = input("请输入任务内容：\n")
    work_reward = int(input("请输入任务奖励：\n"))
    with open(temp_path, 'a+') as f:
        f.write("{}\t{}\t{}\n".format(work_type, work_cnt, work_reward))

# 任务与奖励-显示任务
# 显示所有任务
def show_work(show_mode):
    temp_path = os.path.join(path, 'work_data.txt')
    with open(temp_path, 'r') as f:
        lines = f.readlines()
        i = 1
        for line in lines:
            print("{}:".format(i), end='')
            print(line, end='')
            i += 1

# 任务与奖励-完成任务
# 完成指定任务，成就和单次任务完成后自动删除，成就任务移入成就列表
def finish_work(finish):
    temp_path = os.path.join(path, 'work_data.txt')
    temp_data = []
    with open(temp_path, 'r') as f:
        lines = f.readlines()
        i = 1
        for line in lines:
            temp_data.append(line)
            if i == int(finish):
                work_type = '['+line.split('\t')[0]+']' + line.split('\t')[1] 
                work_reward = line.split('\t')[2][:-1]
                continue
            i += 1
    with open(temp_path, 'w') as f:
        for t in temp_data:
            f.write(t)
    print("已完成任务：{}".format(work_type))
    print("获得奖励：{} 积分".format(work_reward))

@click.command()
@click.option('--set', '-set', default=0, help='set work')
@click.option('--show', '-s', default=0, help='work show mode')
@click.option('--finish', '-f', default=0, help='finish work')
def main(set, show, finish):
    if set != 0:
        set_work()
    elif show != 0:
        show_work(show)
    elif finish != 0:
        finish_work(finish)


if __name__ == '__main__':
    main()