import click
import time
import datetime
import csv
import os
path = r"D:/Desktop/考研复习/总结规划/学习工具/data"

# 番茄钟-展示统计信息
# 按日、月、年展示统计的番茄钟信息
def show_tomato(show_mode):
    today_date = datetime.date.today()
    data_sum = {}
    # 统计当日信息
    if show_mode == 0:
        today_date_str = str(today_date)
        today_date_split = today_date_str.split('-')
        today_year_month_day = today_date_split[0] + today_date_split[1] + today_date_split[2]
        save_path = os.path.join(path, today_year_month_day+'.txt')
        with open(save_path, 'r') as f:
            data_lines = f.readlines()
            for line in data_lines:
                day_data = line.split('\t')
                if day_data[1] not in data_sum:
                    data_sum[day_data[1]] = 0
                data_sum[day_data[1]] += int(day_data[2])*int(day_data[3])
    # 统计当周（当前天数往前数7天）信息
    elif show_mode == 1:
        for i in range(7):
            week_date = str(today_date-datetime.timedelta(days=i))
            week_date_split =  week_date.split('-')
            week_year_month_day = week_date_split[0] + week_date_split[1] + week_date_split[2]
            temp_path = os.path.join(path, week_year_month_day+'.txt')
            if not os.path.exists(temp_path):
                continue
            with open(temp_path, 'r') as f:
                data_lines = f.readlines()
                for line in data_lines:
                    temp_data = line.split('\t')
                    if temp_data[1] not in data_sum:
                        data_sum[temp_data[1]] = 0
                    data_sum[temp_data[1]] += int(temp_data[2])*int(temp_data[3])
    # 统计当月（当前天数往前数30天）信息
    elif show_mode == 2:
        for i in range(30):
            month_date = str(today_date-datetime.timedelta(days=i))
            month_date_split =  month_date.split('-')
            month_year_month_day = month_date_split[0] + month_date_split[1] + month_date_split[2]
            temp_path = os.path.join(path, month_year_month_day+'.txt')
            if not os.path.exists(temp_path):
                continue
            with open(temp_path, 'r') as f:
                data_lines = f.readlines()
                for line in data_lines:
                    temp_data = line.split('\t')
                    if temp_data[1] not in data_sum:
                        data_sum[temp_data[1]] = 0
                    data_sum[temp_data[1]] += int(temp_data[2])*int(temp_data[3])
    # 统计昨天（当前天数往前数1天）信息
    elif show_mode == 3:
        yes_date = str(today_date-datetime.timedelta(days=1))
        yes_date_split =  yes_date.split('-')
        yes_year_month_day = yes_date_split[0] + yes_date_split[1] + yes_date_split[2]
        temp_path = os.path.join(path, yes_year_month_day+'.txt')
        if os.path.exists(temp_path):
            with open(temp_path, 'r') as f:
                data_lines = f.readlines()
                for line in data_lines:
                    temp_data = line.split('\t')
                    if temp_data[1] not in data_sum:
                        data_sum[temp_data[1]] = 0
                    data_sum[temp_data[1]] += int(temp_data[2])*int(temp_data[3])

    print("番茄钟信息：")
    sum_time = 0
    for k in data_sum.keys():
        print("{}\t{} min".format(k, data_sum[k]))     
        sum_time += data_sum[k]
    print("学习总时长\t{} min".format(sum_time)) 

# 番茄钟-保存信息
# 保存调用tomato执行番茄钟的信息
# 使用txt文件保存番茄钟执行信息，保存格式如下
# 日期 \t 番茄钟类型 \t 时长 \t 次数
# date \t category \t time \t num
def save_tomato(minute, category):
    today_date = str(datetime.date.today())
    today_date_split = today_date.split('-')
    today_year_month_day = today_date_split[0] + today_date_split[1] + today_date_split[2]
    save_path = os.path.join(path, today_year_month_day+'.txt')
    # 判断文件是否存在并创建文件
    if not os.path.exists(save_path):
        temp_flie = open(save_path, 'w')
        temp_flie.close()
    # 读取并处理数据
    date = []
    categories = []
    time = []
    num = []
    flag = 0
    with open(save_path, 'r') as f:
        data_lines = f.readlines()
        for line in data_lines:
            temp_data = line.split('\t')
            date.append(temp_data[0])
            categories.append(temp_data[1])
            time.append(temp_data[2])
            if temp_data[1] == category and temp_data[2] == str(minute):
                num.append(str(int(temp_data[3])+1)+'\n')
                flag = 1
            else:
                num.append(temp_data[3])
    if flag == 0:
        date.append(today_date)
        categories.append(category)
        time.append(minute)
        num.append("1\n")
    # 写入数据
    with open(save_path, 'w') as f:
        for i in range(len(date)):
            f.write('{}\t{}\t{}\t{}'.format(date[i],categories[i],time[i],num[i]))

# 番茄钟-主函数
# 调用本函数以开启一个番茄钟
# @param
#    minute 番茄钟时长 
#    myType 番茄钟类型
def tomato(minute, category):
    print('类型：' + category + '\t\t时长：' + str(minute))
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter()-start_time))
        total_seconds = minute*60
        left_seconds = total_seconds - diff_seconds
        if left_seconds <= 0:
            print('')
            break
        filled_len = min(minute, 25)
        filled_per = diff_seconds / total_seconds
        filled = round((filled_per)*filled_len) 
        print('\r', '**'*filled + '--'*(filled_len-filled), 
              '[{:.0%}]'.format(filled_per), 
              '{}:{}'.format(int(left_seconds/60), int(left_seconds%60)), 
              end='')
        time.sleep(1)
    save_tomato(minute, category)

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
@click.option('--function', '-f', default='tomato', help='use function')
@click.option('--minute', '-m', default=25, help='tomato clock time')
@click.option('--category', '-c', default='英语-阅读', help='tomato clock type')
@click.option('--show', '-s', default=0, help='tomato show mode')
@click.option('--finish', '-fin', default=0, help='finish work')
def main(function, minute, category, show, finish):
    if function == 'tomato' or function == 't':
        tomato(minute, category)
    elif function == 'show tomate' or function == 'st':
        show_tomato(show)
    elif function == 'set work' or function == 'setw':
        set_work()
    elif function == 'show work' or function == 'sw':
        show_work(show)
    elif function == 'finish work' or function == 'fw':
        finish_work(finish)


if __name__ == '__main__':
    main()