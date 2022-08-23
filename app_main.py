import random as rd 
import uuid
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods= ['GET'])
def index():
    return "Hello.!"

@app.route('/create', methods= ['POST'])
def test():
    priority_order = {
        5: "food prepared",
        4: "take order",
        3: "clean table",
        2: "give menu",
        1: "any other"
    }
    priority_burst = {
        "food prepared" : (3,8),
        "take order" : (5,10),
        "clean table" : (3,5),
        "give menu" : (2,5),
        "any other" : (1,8)
    }

    class Priority:

        def processData(self, no_of_processes):
            global process_data
            process_data = []
            global priority
            for i in range(no_of_processes):
                print(f"Into process {i}")
                temporary = []
                process_id = uuid.uuid1()
                list1 =list( priority_order.values())
                process_name = rd.choice(list1).lower()
                for key,value in priority_burst.items():
                    if process_name == key:
                        burst_time = rd.choice(range(value[0],value[1])) 
                for key,value in priority_order.items():
                    if process_name == value:
                        priority = key
                temporary.extend([process_id, 0, burst_time, priority, 0, burst_time,process_name])
                '''
                '0' is the state of the process. 0 means not executed and 1 means execution complete
                '''
                process_data.append(temporary)
            Priority.schedulingProcess(self, process_data)

        def schedulingProcess(self, process_data):
            start_time = []
            exit_time = []
            s_time = 0
            sequence_of_process = []
            temp_store_print = 0
            while 1:

                print(f"Into sub : {temp_store_print}")
                temp_store_print += 1

                ready_queue = []
                temp = []
                for i in range(len(process_data)):
                    print(f"Into Sub_process {i}")
                    if process_data[i][1] <= s_time and process_data[i][4] == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3],
                                    process_data[i][5]])
                        ready_queue.append(temp)
                        temp = []
                if len(ready_queue) == 0:
                    break
                if len(ready_queue) != 0:
                    ready_queue.sort(key=lambda x: x[3], reverse=True)
                    start_time.append(s_time)
                    s_time = s_time + 1
                    e_time = s_time
                    exit_time.append(e_time)
                    sequence_of_process.append(ready_queue[0][0])
                    for k in range(len(process_data)):
                        if process_data[k][0] == ready_queue[0][0]:
                            print("Breaking Loop...")
                            break
                    process_data[k][2] = process_data[k][2] - 1
                    if process_data[k][2] == 0:
                        process_data[k][4] = 1
                        process_data[k].append(e_time)
                #t_time = Priority.calculateTurnaroundTime(self, process_data)
                #w_time = Priority.calculateWaitingTime(self, process_data)
                #Priority.printData(self, process_data, t_time, w_time, sequence_of_process)

        def calculateTurnaroundTime(self, process_data):
            total_turnaround_time = 0
            for i in range(len(process_data)):
                turnaround_time = process_data[i][7] - process_data[i][1]
                '''
                turnaround_time = completion_time - arrival_time
                '''
                total_turnaround_time = total_turnaround_time + turnaround_time
                process_data[i].append(turnaround_time)
            average_turnaround_time = total_turnaround_time / len(process_data)
            '''
            average_turnaround_time = total_turnaround_time / no_of_processes
            '''
            return average_turnaround_time

        def calculateWaitingTime(self, process_data):
            total_waiting_time = 0
            for i in range(len(process_data)):
                waiting_time = process_data[i][7] - process_data[i][5]
                '''
                waiting_time = turnaround_time - burst_time
                '''
                total_waiting_time = total_waiting_time + waiting_time
                process_data[i].append(waiting_time)
            average_waiting_time = total_waiting_time / len(process_data)
            '''
            average_waiting_time = total_waiting_time / no_of_processes
            '''
            return average_waiting_time

        def printData(self, process_data, average_turnaround_time, average_waiting_time, sequence_of_process):
            process_data.sort(key=lambda x: x[3],reverse = True)
            '''
            Sort processes according to the Process ID
            '''
            print("Arrival_Time   Rem_Burst_Time    Priority       Completed    Orig_Burst_Time   process_name    Completion_Time    Turnaround_Time    Waiting_Time  ")
            for i in range(len(process_data)):
                for j in range(1,len(process_data[i])):
                    print(process_data[i][j], end="\t\t")
                print()
            print(f'Average Turnaround Time: {average_turnaround_time}')
            print(f'Average Waiting Time: {average_waiting_time}')
            #print(f'Sequence of Process: {sequence_of_process}')


    no_of_processes = 100000
    priority = Priority()
    priority.processData(no_of_processes)

    print(process_data)

    col = ['Task_ID' , 'Arrival_Time' ,  'Rem_Burst_Time' ,   'Priority'    ,   'Completed' , 'Orig_Burst_Time' ,  'process_name'  ,  'Completion_Time']
    df = pd.DataFrame(process_data , columns=col)

    df.to_csv("test.csv")

    return "Done.!"

if __name__ == '__main__':
    app.run(debug=True)
