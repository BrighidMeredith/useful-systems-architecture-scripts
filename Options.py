"""
SysEng5400
@Author Brighid Meredith
Team 13

The following code creates a list of decisions and architectures, stored in archs/d#d#, where d#d# represents d3d4
Key is available in decision_key.pkl
"""

from systems_architecture import Architectures
import pickle
import copy

# Decisions and keys
payload = [1, 2, 3, 4]  # Standard Form
payload_key = {1:"Kinetic", 2:"Impact", 3:"Incendiary", 4:"Laser"}
platform = [1, 2, 3]  # Down Selection
platform_key = {1:"Ground", 2:"Air", 3:"Sea"}
launch = [1, 2, 3, 4, 5, 6, 7, 8]  # Down Selection
launch_key = {1:"Alaska", 2:"Japan", 3:"Philippines", 4:"Mediterranean", 5:"West Coast", 6:"Hawaii", 7:"Georgia", 8:"EU"}
monitors = [1, 2, 3, 4, 5]  # Down Selection
monitors_key = {1:"AWAC", 2:"JSTAR", 3:"Satellite", 4:"Navy", 5:"Ground Radar"}
sensor = [1, 2, 3]  # Standard Form
sensor_key = {1:"Infrared", 2:"Visual", 3:"Signal Monitor"}
spacecraft = [1, 2, 3]  # Standard Form
spacecraft_key = {1:"CubeSat", 2:"Custom Bus", 3:"Prime Bus"}
orbits = [1, 2, 3, 4, 5]  # Standard Form
orbits_key = {1:"HEO", 2:"MEO", 3:"LEO", 4:"GEO"}
hq = [1, 2, 3, 4]  # Standard Form
hq_key = {1:"Central", 2:"Airborne", 3:"Dispersed", 4:"Mobile"}

# Save decision key on server
if 1 == 0:
    decision_key = {1:payload_key, 2:platform_key, 3:launch_key, 4:monitors_key,
                    5:sensor_key, 6:spacecraft_key, 7:orbits_key, 8:hq_key}
    with open('decision_key.pkl','wb') as dec_key:
        pickle.dump(decision_key, dec_key)

a = Architectures.Architectures()

# Build List of Decisions
if 1 == 0:
    decisions = []
    decisions.append(payload)  # Standard Form
    decisions.append(a.ds_arch(platform))
    decisions.append(a.ds_arch(launch))
    decisions.append(a.ds_arch(monitors))
    decisions.append(sensor)
    decisions.append(spacecraft)
    decisions.append(orbits)
    decisions.append(hq)
    output = open('decisions.pkl', 'wb')
    pickle.dump(decisions,output)

# Build list of architectures
if 1 == 0:
    with open('decisions.pkl', 'rb') as input:
        decisions = pickle.load(input)
        print(decisions)
        # Note: Several invalid decisions where DS resulted in []
        # Screen decisions to remove nonsense
        for i,d in enumerate(decisions):
            # Look at each decision
            for j, d_j in enumerate(d):
                # Look at each element of each decision
                if d_j == []:
                    # Invalid, delete d_j
                    del decisions[i][j]
        print(decisions)
        # Invalid decisions removed
        # Calculate list of all possible architectures
        # Note: calculations timed out on PC
        if 1 == 0:
            output = open('architectures.pkl', 'wb')
            architectures = a.all_arch(decisions,[])
            pickle.dump(architectures,output)
        # Run through each decision in 3 & 4 separately (The largest number of decisions come from 3 and 4)
        arch_dump = 'archs/'
        for i, d3 in enumerate(decisions[2]):
            for j, d4 in enumerate(decisions[3]):
                t_decisions = copy.deepcopy(decisions)
                t_decisions[2] = [d3]
                t_decisions[3] = [d4]
                d3d4_archs = a.all_arch(t_decisions,[])
                filename = arch_dump + 'd'+str(i)+'d'+str(j)+'.pkl'
                with open(filename,'wb') as output:
                    pickle.dump(d3d4_archs,output)

# Sample through list of architectures on server to make sure they make sense
if 1 == 1:
    with open('archs/d0d1.pkl', 'rb') as sample:
        d0d0 = pickle.load(sample)
        print(d0d0)
        # Architectures appear as expected
