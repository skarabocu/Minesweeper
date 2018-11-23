import random

class Map():
    rand_nums = []
    # two dimensional array of the mine field
    map = [[], [], [], [], [], [], [],[]]

    def __init__(self):
        # filling the random numbers
        while len(self.rand_nums) < 18:
            numX= random.randint(0,7)#x position
            numY= random.randint(0,6)#y position
            newPos =[numX,numY]#position of the bomb
            if newPos not in self.rand_nums:
                self.rand_nums.append(newPos)


    def draw_map(self):
        for a in range(len(self.map)):
            for b in range(7):
                self.map[a].append(str("0"))#fills whole map with 0s


        for c in range(0,18):
            bombPos = self.rand_nums[c]
            self.map[bombPos[0]][bombPos[1]] = "X"#changes the mines which has bombs with an X sign

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] != "X":
                    amount = self.check_neighbours(i,j)
                    self.map[int(i)][int(j)] = str(amount)
        return self.map

    def check_neighbours(self,num1,num2):
        count=0
        #check the north neighbour
        if int(num1-1) >=0:
            if self.map[int(num1-1)][int(num2)]=="X":
                count += 1
        #check the south neighbour
        if int(num1+1) <=7:
            if self.map[int(num1+1)][int(num2)]=="X":
                count += 1
        #check the west neighbour
        if int(num2-1) >=0:
            if self.map[int(num1)][int(num2-1)]=="X":
                count += 1
        #check the east neighbour
        if int(num2+1) <=6:
            if self.map[int(num1)][int(num2+1)]=="X":
                count += 1
        # check the northwest neighbour
        if int(num1 -1) >= 0 and int(num2-1)>=0:
            if self.map[int(num1-1)][int(num2 -1)] == "X":
                count += 1
        # check the northeast neighbour
        if int(num1 - 1) >= 0 and int(num2 + 1) <= 6:
            if self.map[int(num1 - 1)][int(num2 + 1)] == "X":
                count += 1
        # check the southwest neighbour
        if int(num1 + 1) <= 7 and int(num2 - 1) >= 0:
            if self.map[int(num1 + 1)][int(num2 - 1)] == "X":
                count += 1
        # check the southeast neighbour
        if int(num1 + 1) <=7 and int(num2 + 1) <= 6:
            if self.map[int(num1 + 1)][int(num2 + 1)] == "X":
                count += 1
        return count


