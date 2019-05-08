import random
import csv
import matplotlib.pyplot as plt
import math
rows=[]
with open("tasks.csv", 'r') as csvfile: 
    csvreader=csv.reader(csvfile)
    for row in csvreader: 
        rows.append(row)      
       
class Tasks:
    task_no=0
    exec_time=0

a=0.9
b=0.8
          
def calculateMakespan(task_list):
    makespan=0
    for i in range(no_of_processor):
        time=0
        wait_time=0
        for j in range(len(task_list[i])):
            time+=task[task_list[i][j]-1].exec_time+wait_time
            wait_time+=task[task_list[i][j]-1].exec_time
            if(makespan<time):
                makespan=time
    return makespan

def calculateEnergy(task_list):
    energy=0
    max_time=0
    for i in range(no_of_processor):
        time=0
        for j in range(len(task_list[i])):
            time+=task[task_list[i][j]-1].exec_time
        if(max_time<time):
            max_time=time
    for i in range(no_of_processor):
        time=0
        for j in range(len(task_list[i])):
            time+=task[task_list[i][j]-1].exec_time
        energy+=(time*0.0010)+((max_time-time)*0.0002)    
    return energy
    
   
def createParticle():
    for i in range(no_of_particle):
        particles.append([])
        for j in range(no_of_task):
            processor=random.randint(1,no_of_processor)
            particles[i].append(processor)

def createTaskList(particle):
    task_list=[]
    for i in range(no_of_processor):
        task_list.append([])
        for j in range(no_of_task):
            if(particle[j]==i+1):
                task_list[i].append(j+1);
    makespan=calculateMakespan(task_list)
    energy=calculateEnergy(task_list)
    cost=(a*makespan)+(b*energy)
    return cost

def createTaskList2(particle):
    task_list=[]
    for i in range(no_of_processor):
        task_list.append([])
        for j in range(no_of_task):
            if(particle[j]==i+1):
                task_list[i].append(j+1);
    makespan=calculateMakespan(task_list)
    return makespan

def createTaskList1(particle):
    task_list=[]
    for i in range(no_of_processor):
        task_list.append([])
        for j in range(no_of_task):
            if(particle[j]==i+1):
                task_list[i].append(j+1);
    energy=calculateEnergy(task_list)
    return energy

personal_best=[]
global_best=[]
      
no_of_task=int(input("Enter no. of tasks : "))

task=[Tasks() for i in range(no_of_task)]

for i in range(no_of_task):
    task[i].task_no=rows[i][0]
    task[i].exec_time=int(rows[i][1])
    
no_of_processor=int(input("Enter no. of processors : "))

if(no_of_processor>no_of_task):
    no_of_processor=no_of_task

no_of_particle=20

particles=[]
particle=[]

createParticle()

optimal_makespan=999999999999

velocity=[]

for i in range(no_of_particle):
    personal_best.append([])
    for j in range(no_of_task):
        personal_best[i].append(particles[i][j])

for i in range(no_of_particle):
    makespan=createTaskList(particles[i])
    if(optimal_makespan>makespan):
        pos=i
        optimal_makespan=makespan

for i in range(no_of_task):
        global_best.append(particles[pos][i])
        
for i in range(no_of_particle):
    velocity.append([])
    for j in range(no_of_task):
        x=random.randint(-1,1)
        velocity[i].append(x)
    
no_of_iteration=10
 
makespan_list=[]   
iteration_list=[]
count=1

while(count<=no_of_iteration):
    w=0.5    
    c1=1    
    c2=2
    
    for i in range(no_of_particle):
        for j in range(no_of_task):
            r1=random.random()
            r2=random.random()
            vel_cognitive=c1*r1*(personal_best[i][j]-particles[i][j])
            vel_social=c2*r2*(global_best[j]-particles[i][j])
            velocity[i][j]=w*velocity[i][j]+vel_cognitive+vel_social
            
    for i in range(no_of_particle):
        for j in range(no_of_task):
            particles[i][j]=round(particles[i][j]+velocity[i][j])
            if(particles[i][j]<1):
                particles[i][j]=1
            if(particles[i][j]>no_of_processor):
                particles[i][j]=no_of_processor
   
    min_makespan=optimal_makespan*100
    
    for i in range(no_of_particle):
        makespan=createTaskList(particles[i])
        if(makespan<min_makespan):
                min_makespan=makespan
        if(makespan<optimal_makespan):
            for j in range(no_of_task):
                global_best[j]=particles[i][j]
            optimal_makespan=makespan
        personal_best_makespan=createTaskList(personal_best[i])
        if(personal_best_makespan>makespan):
            for j in range(no_of_task):
                personal_best[i][j]=particles[i][j]
                
    makespan_list.append(min_makespan/60)            
    iteration_list.append(count)
        
    count=count+1
    
print("\n\nOptimal Task Assignment for PSO :\n\nTask\tProccessor\tExecution Time (in sec)")

for i in range(no_of_task):
    print(" ",i+1,"\t   ",global_best[i],"\t\t      ",task[i].exec_time)
    
print("\nOptimal Makespan using PSO = ",round((createTaskList2(global_best)/60),2),"min(s)")
print("Optimal Energy using PSO = ",round(createTaskList1(global_best),2),"units")

plt.plot(iteration_list,makespan_list)
plt.xlabel('Iterations')
plt.ylabel('Makespan + Energy ')
plt.axis([1,no_of_iteration,0,optimal_makespan*2.5/60])
plt.show()

for i in range(no_of_particle):
    for j in range(no_of_task):
        particles[i][j]=personal_best[i][j]
        
no_of_bacteria=20
no_of_chemotactics=10
swim_length=4
no_of_reproductions=4
no_of_dispersals=2
step_size=1.45
probability_dispersal=0.25
d_attractant=-0.1
w_attractant=-0.2
h_repellant=0.1
w_repellant=-10

J_last=[]
J_health=[]
J=[]

makespan_list=[]   
chemotactics_list=[]
count=1

def interact(x):
    value=0
    for i in range(no_of_bacteria):
            for j in  range(no_of_task):      
                value+=particles[x][j]-particles[i][j]
                value=value**2
    return value
            

def interaction(x):
    attr=0
    repel=0
    for i in range(no_of_bacteria):
        if(i!=x):
            attr+=d_attractant*math.exp(w_attractant*interact(x))
            repel+=h_repellant*math.exp(w_repellant*interact(x))
    return attr+repel

for i in range(no_of_bacteria):
    J_last.append(0)
    J.append(0)
    J_health.append(0)

def generateDirection():
    direction=[]
    for i in range(no_of_task):
        x=random.randint(-1,1)
        direction.append(x)
    return direction

for i in range(no_of_bacteria):
    J_health[i]=createTaskList(particles[i])

for l in range(no_of_dispersals):
    for k in range(no_of_reproductions):
        for j in range(no_of_chemotactics):
            for i in range(no_of_bacteria):
                
                J[i]=createTaskList(particles[i])
                J_last[i]=J[i]
                direction=generateDirection()
                for m in range(no_of_task):
                    particles[i][m]=round(particles[i][m]+(step_size*direction[m]))
                    if(particles[i][m]<1):
                        particles[i][m]=1
                    if(particles[i][m]>no_of_processor):
                        particles[i][m]=no_of_processor
                J[i]=createTaskList(particles[i])
               
                if(J[i]<optimal_makespan):
                    optimal_makespan=J[i]
                    for m in range(no_of_task):
                        global_best[m]=particles[i][m]
                        personal_best[i][m]=particles[i][m]
                
                if(J[i]<=J_last[i]):
                    J_last[i]=J[i]
                    J_health[i]+=J_last[i]
                    for m in range(no_of_task):
                        personal_best[i][m]=particles[i][m]
                    
                    swim_count=0
                    for m in range(no_of_task):
                            particles[i][m]=round(particles[i][m]+(step_size*direction[m]))
                            if(particles[i][m]<1):
                                particles[i][m]=1
                            if(particles[i][m]>no_of_processor):
                                particles[i][m]=no_of_processor
                    while(swim_count<swim_length):
                        swim_count+=1
                    
                        J[i]=createTaskList(particles[i])
                        
                        
                        if(J[i]<optimal_makespan):
                            for m in range(no_of_task):
                                global_best[m]=particles[i][m]
                                personal_best[i][m]=particles[i][m]
                        
                        if(J[i]<=J_last[i]):
                            J_last[i]=J[i]
                            J_health[i]+=J_last[i]
                            for m in range(no_of_task):
                                personal_best[i][m]=particles[i][m]
                            for m in range(no_of_task):
                                particles[i][m]=round(particles[i][m]+(step_size*direction[m]))
                                if(particles[i][m]<1):
                                    particles[i][m]=1
                                if(particles[i][m]>no_of_processor):
                                    particles[i][m]=no_of_processor
        

            makespan_list.append(createTaskList(global_best)/60)
            chemotactics_list.append(count)
            count+=1
        
        
        for m in range(no_of_bacteria-1):
            for n in range(no_of_bacteria-m-1):
                if(J_health[n]>J_health[n+1]):
                    temp=J_health[n]
                    J_health[n]=J_health[n+1]
                    J_health[n+1]=temp
                    
                    for x in range(no_of_task):
                        temp=particles[n][x]
                        particles[n][x]=particles[n+1][x]
        
        kill=int(no_of_bacteria/2)
        
        for m in range(kill):
            for x in range(no_of_task):
                        particles[m+kill][x]=particles[m][x]                        

                             
    dispersal=int(no_of_bacteria*probability_dispersal)        
    for x in range(no_of_bacteria):
        if(x%dispersal==0):
            direction=generateDirection()
            for m in range(no_of_task):
                particles[x][m]=round(particles[x][m]+(step_size*direction[m]))
                if(particles[x][m]<1):
                    particles[x][m]=1
                if(particles[x][m]>no_of_processor):
                    particles[x][m]=no_of_processor         

print("\n\nOptimal Task Assignment for Hybrid PSO-BFO :\n\nTask\tProccessor\tExecution Time (in sec)")

for i in range(no_of_task):
    print(" ",i+1,"\t   ",global_best[i],"\t\t      ",task[i].exec_time)
    
print("\nOptimal Makespan using Hybrid PSO-BFO = ",round((createTaskList2(global_best)/60),2),"min(s)")
print("Optimal Energy using Hybrid PSO-BFO = ",round(createTaskList1(global_best),2),"units")
plt.plot(chemotactics_list,makespan_list)
plt.xlabel('Chemotactic Steps')
plt.ylabel('Makespan + Energy ')
plt.axis([1,count,0,optimal_makespan/30])
plt.show()



