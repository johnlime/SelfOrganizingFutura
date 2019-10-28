import torch
import random
import math
import numpy

class AngeniolSOM:
    def __init__(self, weight_matrix, total_nodes=None, node_size=2, update_iterations=100, init_rank=3):
        self.w = torch.cumsum(torch.tensor(weight_matrix), dim = 0)
        self.m = total_nodes
        self.tau = update_iterations
        self.rank = init_rank*torch.ones(self.m, 1)
        self.g = 1

    def select_winner(self, x):
        return torch.argmin(torch.norm(torch.sqrt((x-self.w)**2), p=1, dim=1), dim=0)

    def h(self, c, t):
        d = torch.zeros(self.m, 1)
        for i in range(0, c):
            d[:i+1] += torch.norm((self.w[i]-self.w[i+1]), p=2)+0.001
        for i in range(c+1, self.m):
            d[i:] += torch.norm((self.w[i]-self.w[i-1]), p=2)+0.001
        return 1/math.sqrt(2)*torch.exp(-1*d/self.g**2)

    def update(self, x=None, t=None, indices=None):
        x = torch.cumsum(x, dim = 0).float()
        for index in indices:
            part_x = x[index] #Extract input vector
            c = self.select_winner(part_x) #winner index
            self.rank[c] += 1
            self.w += self.h(c, t)*(part_x - self.w)

        self.g *= 0.9
        self.rank -= 1
        i=0
        while i < self.m:
            if self.rank[i] == 0:
                #Rank
                upper = self.rank[:i]
                lower = self.rank[i+1:]
                self.rank = torch.cat((upper, lower), dim=0)
                #Weights
                upperw = self.w[:i]
                lowerw = self.w[i+1:]
                self.w = torch.cat((upperw, lowerw), dim=0)
                #Change Size
                self.m -= 1
            elif self.rank[i] > 3:
                self.rank[i] = 3
                #Rank
                upper = self.rank[:i]
                lower = self.rank[i+1:]
                self.rank = torch.cat((torch.cat((upper, self.rank[i].expand(2, -1)), dim=0), lower), dim=0)
                #Weights
                upperw = self.w[:i]
                lowerw = self.w[i+1:]
                self.w = torch.cat((torch.cat((upperw, self.w[i].expand(2, -1)), dim=0), lowerw), dim=0)
                #Change Size
                self.m += 1
                i += 2
            else:
                i += 1

def run(path_polygon, target_path_polygon):
    torch.manual_seed(1)
    random.seed(1)

    source = []
    for i in range(len(path_polygon[0])):
        source.append([path_polygon[0][i][1], path_polygon[0][i][2]])

    total_itr = 10
    som = AngeniolSOM(source, total_nodes=len(source), node_size=2, update_iterations=total_itr)

    target = torch.empty(len(target_path_polygon[0]), 2)
    for i in range(len(target_path_polygon[0])):
        target[i][0] = target_path_polygon[0][i][1]
        target[i][1] = target_path_polygon[0][i][2]

    indices = list(range(target.size()[0]))
    random.shuffle(indices)
    output = []
    index = 0
    for t in range(total_itr):
        som.update(target, t, indices)
        output.append([])
        output[index].append(['M', som.w[0][0].numpy(), som.w[0][1].numpy()])
        for i in range(1, len(som.w)):
            output[index].append(['l', (som.w[i][0] - som.w[i - 1][0]).numpy(), (som.w[i][1] - som.w[i - 1][1]).numpy()])
        index += 1
    return output
