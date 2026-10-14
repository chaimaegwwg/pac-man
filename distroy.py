
def ft_find_paths(self,position_pacman,pos_ghost,num):
    paths = []
    directions = self.directions
    current = [pos_ghost[0],pos_ghost[1]]
    self.n = num
    all_paths = []
    def recursion_dfs(path,current):
        # print("======>", current)
        if current == position_pacman:
            all_paths.append(path.copy())
            self.n +=1
            return
        if self.n == 1:
            return
        else:
            for x, y in directions:
                pos = [x, y]
                if [current[0]+x ,current[1]+y] in path:
                    continue
                if 0 <= current[0] <= self.size[0]-1 and 0 <= current[1] <= self.size[1] -1:
                    if self.ft_check_walls(pos,current[0],current[1]):
                        path.append(current)
                        recursion_dfs(path,[current[0]+x, current[1]+y])
                        path.pop()

    recursion_dfs([],current)
    return all_paths