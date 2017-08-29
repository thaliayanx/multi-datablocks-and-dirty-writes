import simpy
import random
from random import randint


num_of_dirty_write=0
dirty=True
RANDOM_SEED = 42
NEW_REQUEST = 100
NUM_DATA_BLOCK=70
INTERVAL = 10.0
last_read_write=[]

def source(env, number, interval, data):
    for i in range(number):
        j = random.uniform(0.0,1.0)
        duration=random.uniform(1,10)
        
        if j>0.5:
            c = action(env, 'read%d' % i, data )
        else:
            c = action(env, 'write%d' % i, data)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def action(env, name, data):
    
    global last_read_write
    global num_of_dirty_write
    global dirty
    dirty=True
    arrive = env.now
    datablock=randint(0,NUM_DATA_BLOCK-1)
    print('%7.4f %s: Received' % (arrive, name))
    if name[0]=='r':
        duration = random.uniform(20,50)
        last_read_write[datablock]=arrive+duration
        yield env.timeout(duration)
        print('%7.4f %s: Finished' % (env.now, name))
    
    else:
        while dirty:
            arrive = env.now
            if arrive<last_read_write[datablock]:
                num_of_dirty_write+=1
                duration = random.uniform(20,50)
                yield env.timeout(duration)
            else:
                dirty=False
                duration = random.uniform(20,50)
                last_read_write[datablock]=arrive+duration
                yield env.timeout(duration)
                print('%7.4f %s: Finished' % (env.now, name))



# Setup and start the simulation
print('Typical Reader and Writer')
random.seed(RANDOM_SEED)
env = simpy.Environment()

for i in range(NUM_DATA_BLOCK):
    last_read_write.append(0.00)

# Start processes and run
for i in range(NUM_DATA_BLOCK):
    data = simpy.Resource(env, capacity=1)
    env.process(source(env, NEW_REQUEST, INTERVAL, data))
    env.run()
print('percentage of dirty write =%d%%' %(num_of_dirty_write/(NEW_REQUEST*NUM_DATA_BLOCK)*100))
