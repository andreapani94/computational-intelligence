import random

class Node:
    def __init__(self, state: set, parent: 'Node' = None, action: list = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __str__(self):
        return f"(State:{self.state}, action:{self.action}, cost:{self.path_cost})"

class SetCoveringProblem:

    initial_state = set()

    def __init__(self, N):
        self.goal_state = set(range(N))
        self.possible_actions = problem(N, seed = 42)

    def is_goal(self, state):
        return state == self.goal_state

    def actions(self, state):
        return self.possible_actions

    def result(self, state, action):
        #the result is 
        return state | set(action)

    def action_cost(self, action):
        #since action is a list, the cost is defined as the length of the list
        return len(action)

               

def problem(N, seed = None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def greedy(N):
    goal = set(range(N))
    covered = set()
    solution = list()
    all_lists = sorted(problem(N, seed = 42), key = lambda l: len(l))
    #print('The problem is:')
    #print(all_lists)
    while goal != covered:
        l = all_lists.pop(0)
        if not set(l) < covered:
            solution.append(l)
            covered |= set(l)
    #print('The solution is:')
    #print(solution)
    w = sum(len(l) for l in solution)
    print('w = ' + str(w))

def best_first_search(problem: SetCoveringProblem):
    starting_node = Node(problem.initial_state)
    #simulate priority queue with an ordered list
    frontier = list()
    frontier.append(starting_node)
    reached = dict()
    reached[frozenset(problem.initial_state)] = starting_node 
    while len(frontier) > 0:
        node: Node = frontier.pop(0)
        #check if node is goal state
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            state = frozenset(child.state)
            if state not in reached or child.path_cost < reached[state].path_cost:
                reached[state] = node
                frontier.append(child)
        #to simulate a priority queue
        frontier.sort(key = lambda node: node.path_cost)
    raise Exception('No path to a goal state was found')

def expand(problem: SetCoveringProblem, node: Node):
    state = node.state
    expanded_nodes = []
    for action in problem.actions(state):
        result_state = problem.result(state,action)
        total_cost = node.path_cost + problem.action_cost(action)
        expanded_node = Node(result_state, node, action, total_cost)
        expanded_nodes.append(expanded_node)
    return expanded_nodes

def print_path(node: Node):
    path = []
    while node.parent != None:
        path.append(node)
        node = node.parent
    path.reverse()
    for node  in path:
        print(node)



if __name__ == '__main__':
    problem = SetCoveringProblem(100)
    goal = best_first_search(problem)
    print_path(goal)