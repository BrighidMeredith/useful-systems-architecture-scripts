"""
Syseng5400
@Brighid Meredith
Team 13
Purpose: provide metrics for each decision in a given architecture
"""
import pickle


class Metrics:

    def __init__(self):
        costs = {}
        self.reliability = {'Air':0.02,'Airborne':0.01,'AWAC':0.01,'Central':0.001,'CubeSat':0.3,'Custom Bus':0.01,'Dispersed':0.05,
                       'EU':0,'GEO':0.04,'Georgia':0,'Ground':0.01,'Ground Radar':0.001,
                        'Hawaii':0,'HEO':0.03,'Impact':0.25,'Incendiary':0.1,'Infrared':0.01,'Japan':0,
                        'JSTAR':0.02,'Kinetic':0.25,'Laser':0.01,'LEO':0.02,'Mediterranean':0,'MEO':0.02,
                        'Mobile':0.05,'Navy':0.05,'Philippines':0,'Prime Bus':0.003,
                        'Satellite':0.02,'Sea':0.04,'Signal Monitor':0.5,'Visual':0.2,'West Coast':0}
        self.cost = {'Air':30,'Airborne':500,'AWAC':200,'Central':750,'CubeSat':1.5,'Custom Bus':500,'Dispersed':100,
                'EU':750,'GEO':248,'Georgia':500,'Ground':100,'Ground Radar':50,'Hawaii':1000,
                'HEO':225,'Impact':700,'Incendiary':100,'Infrared':1000,'Japan':2000,'JSTAR':200,'Kinetic':800,
                'Laser':500,'LEO':185,'Mediterranean':2000,'MEO':198,'Mobile':200,'Navy':50,'Philippines':2000,
                'Prime Bus':400,'Satellite':1000,'Sea':624,'Signal Monitor':500,'Visual':1500,'West Coast':500}
        self.key = pickle.load(open('decision_key.pkl','rb'))
        # test key
        if 1 == 0:
            print(self.key)
            for i in range(1,len(self.key)+1):
                #print(self.key[i])
                for j in range(1,len(self.key[i])+1):
                    #print(self.key[i][j])
                    k = self.key[i][j]
                    try:
                        print(k)
                        r = self.reliability[k]
                        c = self.cost[k]
                        print("cost:{}\treliability:{}".format(c,r))
                    except KeyError:
                        print('missing:{}'.format(k))

    def get_cost(self,arch):
        cost = 0
        for i,d in enumerate(arch):
            decision_i = i+1
            # Some decisions have multiple parts
            if type(d) == list:
                for j,dj in enumerate(d):
                    key = self.key[decision_i][dj]
                    try:
                        cost += self.cost[key]
                        #print(cost)
                    except KeyError:
                        pass
            else:
                key = self.key[decision_i][d]
                cost += self.cost[key]
                #print(key)
        return cost

    def get_reliability(self,arch):
        r = 1
        for i,d in enumerate(arch):
            decision_i = i+1
            # Some decisions have multiple parts
            if type(d) == list:
                pr = 1
                for j,dj in enumerate(d):
                    key = self.key[decision_i][dj]
                    try:
                        pr = pr * self.reliability[key]
                    except KeyError:
                        pr = 0
                r = r * (1-pr)
            else:
                key = self.key[decision_i][d]
                r = r * (1 - self.reliability[key])
        return r


if __name__ == "__main__":
    #  Sample Arch
    sa = [1, [1], [1], [1, 2], 1, 1, 1, 3]

    m = Metrics()
    m.get_cost(sa)
    print(m.get_reliability(sa))