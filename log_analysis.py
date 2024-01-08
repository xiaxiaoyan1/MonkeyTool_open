import re
#第一步读取monkey日志
#第二步查找monkey日志中带ANR无响应,CARSH崩溃,GC内存泄漏,Exception异常问题比如空指针
#第三步解析日志，使用正则表达式分离出崩溃信息、堆栈信息等
#第四步统计崩溃率

def read_log(find_path):
    with open(find_path, encoding='utf-8') as f:
        log_lines = f.readlines()
        #print(type(log_lines))
        return log_lines
'''
1、无响应问题可以在日志中搜索 “ANR” 。

2、崩溃问题搜索 “CRASH” 。

3、内存泄露问题搜索"GC"（需进一步分析）。

4、异常问题搜索 “Exception”（如果出现空指针， NullPointerException，需格外重视）。
'''
def search_bug(log_lines):
    anr_log=[]
    anr_count=0
    crash_log=[]
    crash_count=0
    gc_log=[]
    gc_count=0
    exception_log=[]
    exception_count=0
    anr_pattern=re.compile(r'.*ANR.*')
    crach_pattern=re.compile(r'.*CRASH.*')
    gc_pattern=re.compile(r'.*GC.*')
    exception_pattern=re.compile(r'.*Exception.*')
    for line in log_lines:
        if anr_pattern.match(line):
            anr_log.append(line)
            anr_count=anr_count+1
        if crach_pattern.match(line):
            crash_log.append(line)
            crash_count=crash_count+1
        if gc_pattern.match(line):
            gc_log.append(line)
            gc_count=gc_count+1
        if exception_pattern.match(line):
            exception_log.append(line)
            exception_count=exception_count+1
    return anr_log,crash_log,gc_log,exception_log,anr_count,crash_count,gc_count,exception_count

## 使用正则表达式分离出崩溃信息、堆栈信息等
def analyze_log(anr_log,crash_log,gc_log,exception_log):
    anr_info_list=[]
    crash_info_list = []
    gc_info_list=[]
    exception_info_list=[]

    for anr_data in anr_log:
        anr_info_partern = re.compile(r'.*ANR: (\s+.*): pid=(\d+),(.*):')
        anr_match=anr_info_partern.match(anr_data)
        if anr_match:
            activity_info=anr_match.group(1)
            pid=anr_match.group(2)
            crash_type = anr_match.group(3)
            anr_info_list.append((activity_info,pid,crash_type))

    for crash_data in crash_log:
        crash_info_parterb = re.compile(r'.*CRASH: (\s+.*): pid=(\d+),(.*):')
        crash_match = crash_info_parterb.match(crash_data)
        if crash_match:
            activity_info = crash_match.group(1)
            pid = crash_match.group(2)
            crash_type = crash_match.group(3)
            crash_info_list.append((activity_info, pid, crash_type))

    for gc_data in gc_log:
        gc_info_parterb = re.compile(r'.*GC: (\s+.*): pid=(\d+),(.*):')
        gc_match=gc_info_parterb.match(gc_data)
        if gc_match:
            activity_info = gc_match.group(1)
            pid = gc_match.group(2)
            crash_type = gc_match.group(3)
            gc_info_list.append((activity_info, pid, crash_type))

    for exception_data in exception_log:
        exception_info_parterb = re.compile(r'.*Exception: (\s+.*): pid=(\d+),(.*):')
        exception_match=exception_info_parterb.match(exception_data)
        if exception_match:
            activity_info = exception_match.group(1)
            pid = exception_match.group(2)
            crash_type = exception_match.group(3)
            exception_info_list.append((activity_info, pid, crash_type))

    return anr_info_list,crash_info_list,gc_info_list,exception_info_list





