import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

class Gantt:
    def __init__(self, log = True):
        self.log = log
        self.gantt_data = {"MC": [],
                           "Order" : [],
                           "Start time" : [],
                           "Process time" : []}

    def update_gantt(self, MC, ST, PT, job):
        self.gantt_data['MC'].append("M{}".format(MC))
        self.gantt_data['Order'].append(job)
        self.gantt_data['Start time'].append(ST)
        self.gantt_data['Process time'].append(PT)

    def draw_gantt(self, save = None):
        #set color list
        plt.figure(figsize=(30, 10))
        #colors = list(mcolors.CSS4_COLORS.keys())
        colors = list(mcolors.TABLEAU_COLORS.keys())
        #np.random.shuffle(colors)
        #draw gantt bar
        y = self.gantt_data['MC']
        width = self.gantt_data['Process time']
        left = self.gantt_data['Start time']
        color = []
        for j in self.gantt_data['Order']:
            color.append(colors[int(j)])

        plt.barh(y = y, width = width, height = 0.5, color=color,left = left, align = 'center',alpha = 0.6)
        #add text
        for i in range(len(self.gantt_data['MC'])):
            text_x = self.gantt_data['Start time'][i] + self.gantt_data['Process time'][i]/2
            text_y = self.gantt_data['MC'][i]
            text = self.gantt_data['Order'][i]
            if len(text) >=10:
                text = ""
            plt.text(text_x, text_y, text, verticalalignment='center', horizontalalignment='center', fontsize=20)
        #figure setting
        plt.xlabel("time (hrs)")
        plt.xticks(np.arange(0,30))
        plt.ylabel("Machine")
        plt.title("Gantt Chart")

        plt.grid(True)

        if save == None:
            plt.show()
        else:
            plt.savefig(save)
        plt.show()


class machine(object):
    def __init__(self, working, end_time, buffer):
        #check if the machine is working or not
        self.working = working
        #end time of A B C machines finished the onhand order
        self.end_time = end_time
        #buffer of A B C machines(the waiting jobs)
        self.buffer = buffer

class job(object):
    def __init__(self, at, sequence, due, inbuffer, finished):
        #arrival time of job
        self.at = at
        #sequence of the job
        self.sequence = sequence
        #due date
        self.due = due
        #check if the job is in buffer
        self.inbuffer = inbuffer
        #check if the job is finished
        self.finished = finished


#if the job sequence is empty, then end the while loop
def check(wholelist):
    count = 0
    for i in wholelist:
        count += len(i.sequence)

    if (count != 0):
        return True
    else:
        return False

#decide the next timeline
def nexttime(s,a,b,c):
    if (a == 0 and b == 0 and c == 0 and s == 0):
        return 0
    else:
        temp = []
        if(a > s):
            temp.append(a)
        if(b > s):
            temp.append(b)
        if(c > s):
            temp.append(c)
        return min(temp)

def EDD(job_list, buffer):
    win_index = buffer[0]
    for i in buffer:
        if(job_list[i].due < job_list[win_index].due):
            win_index = i
    return win_index

process_plt = Gantt()

j1 = job(0,[['A',5],['C',1],['B',2],['C',1]],15,False,False)
j2 = job(4,[['B', 3], ['C', 1], ['A', 5], ['C', 1]],14,False,False)
j3 = job(0,[['B',4],['A',5],['C',1]],20,False,False)
j4 = job(0,[['A',4],['B',3],['C',1]],24,False,False)
j5 = job(0,[['B',2],['C',4],['B',2]],10,False,False)
j6 = job(7,[['A',5],['B',3],['C',1]],16,False,False)
j7 = job(10,[['B',5],['C',2]],20,False,False)

job_list = [j1,j2,j3,j4,j5,j6,j7]

machine_A = machine(False,0,[])
machine_B = machine(False,0,[])
machine_C = machine(False,0,[])
start_time = 0

#print the job info.
for i in job_list:
    print(i.at, i.sequence, i.due, i.inbuffer)

tardiness = 0
#store the winning job index of A B C
indexA = indexB = indexC = 0

process_plt.draw_gantt()

while(check(job_list)):
    #determine the next start time
    start_time = nexttime(start_time,machine_A.end_time,machine_B.end_time,machine_C.end_time)
    print("\nT",start_time)

    #if the start_time == end_time of machine
    #then set the job to next sequence and set the machine condition to no working
    if(start_time == machine_A.end_time and start_time != 0):
        machine_A.working = False
        job_list[indexA].inbuffer = False
        machine_A.buffer.remove(indexA)
        del job_list[indexA].sequence[0]
    if(start_time == machine_B.end_time and start_time != 0):
        machine_B.working = False
        job_list[indexB].inbuffer = False
        machine_B.buffer.remove(indexB)
        del job_list[indexB].sequence[0]
    if(start_time == machine_C.end_time and start_time != 0):
        machine_C.working = False
        job_list[indexC].inbuffer = False
        machine_C.buffer.remove(indexC)
        del job_list[indexC].sequence[0]


    for i in job_list:
        #calculate tardiness
        if(len(i.sequence) == 0 and (not i.finished)):
            tardiness += max(0,start_time - i.due)
            i.finished = True
        #if the order is arrived and not processing, then add it into the buffer it should be
        if((i.at <= start_time) and (not i.inbuffer) and (not i.finished)):
            if(i.sequence[0][0] == 'A'):
                machine_A.buffer.append(job_list.index(i))
            elif(i.sequence[0][0] == 'B'):
                machine_B.buffer.append(job_list.index(i))
            else:
                machine_C.buffer.append(job_list.index(i))
            i.inbuffer = True

    print("\nbuffer_A:" , machine_A.buffer ,"\nbuffer_B:" , machine_B.buffer , "\nbuffer_C:" , machine_C.buffer)
    print("\nmachine condition:\nA:",machine_A.working,"\nB:",machine_B.working,"\nC:",machine_B.working)

    #machine A
    if(not machine_A.working and len(machine_A.buffer) != 0):
        #index store the win job
        indexA = machine_A.buffer[0]
        #EDD
        indexA = EDD(job_list, machine_A.buffer)
        #store the data into gantt chart
        process_plt.update_gantt('A',start_time,job_list[indexA].sequence[0][1],str(indexA))
        #update end_time of A and job processing state
        machine_A.end_time = start_time + job_list[indexA].sequence[0][1]

        #set the machine condition to using
        machine_A.working = True

    #machine B
    if(not machine_B.working and len(machine_B.buffer) != 0):
        #index store the win job
        indexB = machine_B.buffer[0]
        #EDD
        indexB = EDD(job_list, machine_B.buffer)
        #store the data into gantt chart
        process_plt.update_gantt('B',start_time,job_list[indexB].sequence[0][1],str(indexB))
        #update end_time of A and job processing state
        machine_B.end_time = start_time + job_list[indexB].sequence[0][1]

        #set the machine condition to using
        machine_B.working = True

    #machine C
    if(not machine_C.working and len(machine_C.buffer) != 0):
        #index store the win job
        indexC = machine_C.buffer[0]
        #EDD
        indexC = EDD(job_list, machine_C.buffer)
        #store the data into gantt chart
        process_plt.update_gantt('C',start_time,job_list[indexC].sequence[0][1],str(indexC))
        #update end_time of A and job processing state
        machine_C.end_time = start_time + job_list[indexC].sequence[0][1]

        #set the machine condition to using
        machine_C.working = True

    print("\nEnd_time of A B C:\nTA:",machine_A.end_time,"\nTB:",machine_B.end_time,"\nTC:",machine_C.end_time)

    print("\nSequence:")
    for i in job_list:
        print(i.sequence)
    print("-------------------")
    process_plt.draw_gantt()

print("\nMakespan = %d hrs \n" %start_time)

print("Total Tardiness = %d\nAverage Tardiness = %.3f hrs\n" %(tardiness,(tardiness/len(job_list))))
