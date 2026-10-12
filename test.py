class Solution(object):
    def shortestPathBinaryMatrix(self, grid):
        directions = [[0,1],[1,0],[-1,0],[0,-1],[1,1],[-1,1],[1, -1],[-1,-1]]
        current  = [0, 0]
        queue = {}
        visited = []
        d = [0,0]

        def recursion(current, previous):
            neighbors = []
            # if current == [len(grid) - 1, len(grid) - 1]:
            #     visited.append(current)
            #     queue[(current[0],current[1])] = previous
            #     return
            # if (current[0],current[1]) in queue:
            #     queue[(current[0],current[1])].append((previous[0],previous[1]))
            # else:
            # if (current[0],current[1]) not in queue:
            #     queue[(current[0],current[1])] = (previous[0],previous[1])
            # previous = current
            # visited.append(current)
            current = [0, 0]
            previous = [0, 0]
            visited = {tuple(current)}
            to_visit = [current]
            while to_visit:
                current = to_visit.pop(0)
                if current == [len(grid) - 1, len(grid) - 1]:
                    break
                neighbors = []
                for i in directions:
                    x, y = i
                    if current[0] - x < 0 or current[1] -y < 0 or current[0] - x > len(grid)-1 or current[1]-y > len(grid)-1:
                        continue
                    if [current[0]-x, current[1]-y] in visited or grid[current[0]-x][current[1]-y] == 1:
                        continue
                    neighbors.append([current[0] - x,current[1] -y])
                    # if (current[0],current[1]) not in queue:
                    #     queue[(current[0],current[1])] = (previous[0],previous[1])
                # previous = current
                for n in neighbors:
                    visited.add(n)
                    queue[tuple(n)] = tuple(current)
                    to_visit.append(n)

                to_visit.append(current)
            

        recursion(current, d)
        res = []
        
        prevs = (len(grid)-1, len(grid)-1)
        for key ,value in queue.items():
            print("==>",key,value)
        # for key ,value in reversed(queue.items()):
            # print("the difference between them ",(value[0],value[1]), prevs)
            # if (value[0],value[1]) == prevs:
            #     prevs = (key[0],key[1]) 
            #     res.append(value)
            # print(type(value),type(prevs))
            # print("search for the problem ",key , value, prevs)
            
        print("the result =>",res)
        return queue


def main():
    s = Solution()
    res = s.shortestPathBinaryMatrix([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
])
    print(res)

main()
