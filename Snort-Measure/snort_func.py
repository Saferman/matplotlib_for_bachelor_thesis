# encoding:utf-8

# encoding:utf-8
import os
import subprocess
import platform

outname = "bayesian.txt"
def output(s):
    with open(outname, "a") as f:
        f.write(str(s)+"\n")


def change_conf(conf = "/usr/local/snort/rules/rules/etc/snort.conf", x=20):
    with open(conf, "r") as f:
        lines= f.readlines()
    for i in xrange(0,len(lines)):
        if lines[i].find("max-pattern-len")!=-1:
            lines[i] = "config detection: search-method ac-split search-optimize max-pattern-len" +" " + str(x)
            lines[i] = lines[i] + "\n"
            # output(lines[i])
    with open(conf, "w") as f:
        f.writelines(lines)

def f(x):
    y = 0.0
    x = int(x)  # 转成整数
    if x < 0 or x> 40:
        output("[-]Out of range")
    else:
        if 'windows' in platform.platform().lower():
            command = 'net'
            command = command.split()
            child = subprocess.Popen(command, stdout=subprocess.PIPE)
            child.wait()
            return y
        change_conf(x=x)
        command = "snort -d -A fast -r /home/lcx/snortEXP/insideHTTP.pcap -c  /usr/local/snort/rules/rules/etc/snort.conf"
        # command = "cat /etc/passwd"
        command = command.split()
        child = subprocess.Popen(command, stdout=subprocess.PIPE)
        child.wait()
        # raw_input(">Pause:")
        # content = child.stdout.readlines()
        # for line in content:
        #     if line.find("Run time for packet")!=-1:
        #         print line
        #         output(line)
        # output(content)
        with open("time_measure_handled.txt","r") as f:
            lines = f.readlines()
        for line in lines:
            if line.find("seconds")!= -1:
                timeline = line.split()[2]
                # output(timeline)
                y += float(timeline)
        # output(y)

    return -1 * y


if __name__=='__main__':
    if os.path.exists(outname):
        os.remove(outname)
    print f(20.0)


