#implement huffman

initial = ['B', 'E', 'E', 'C', 'A', 'A', 'D', 'D', 'E', 'D', 'C', 'C', 'A', 'C', 'A', 'C', 'A', 'C']
initialBits = len(initial) * 8
#print(initialBits)

#calculate frequency
frequencies = {}

for letter in initial:
    if letter in frequencies:
        frequencies[letter] += 1
    else:
        frequencies[letter] = 1

#print(frequencies)
class Node:
    def __init__(self,frequency=None,parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.frequency = frequency
        self.value = None
        self.bit = -1

def huffman():
    sortedDict = dict(sorted(frequencies.items(), key=lambda item: item[1]))
    sortedNodes = [Node(frequency=freq) for freq in sortedDict.values()]

    #assign the values to each node
    for ind, keys in enumerate(sortedDict.keys()):
        sortedNodes[ind].value = keys

    Z = Node()
    root = []
    valueCounter = 1
    while len(sortedNodes) > 0:
        #create empty Node
        
        if Z not in root:
            root.append(Z)

        #assign min frequency to left child of z, and second minimum to right child
        Z.left = getMin(sortedNodes)
        for i in sortedNodes:
            if i.value == Z.left.value:
                sortedNodes.remove(i)     

        if len(sortedNodes) == 0:
            break
        
        #second min to the right
        Z.right=getMin(sortedNodes)
        for i in sortedNodes:
            if i.value == Z.right.value:
                sortedNodes.remove(i)
        
        #assigning Z freq, and making it parent of the left and right
        Z.frequency = Z.right.frequency + Z.left.frequency
        Z.right.parent = Z
        Z.left.parent = Z
        Z.left.bit = 0
        Z.right.bit = 1
        Z.value = str(valueCounter)
        valueCounter += 1
        sortedNodes.append(Z)
    
        if len(sortedNodes)>0:#idk if this if is necessary but still keep the Z=Node()
            Z = Node()
     
    #I FUCKING DID IT
    for r in root:
        print(r)
        print("My freq:"+ str(r.frequency))
        if r.left:
            print("Left:" + str(r.left.frequency))
        if r.right:
            print("Right:" + str(r.right.frequency))
        if r.parent:
            print("Parent:" + str(r.parent.frequency))
        print("\n\n")
    #SO WHEN YOU ACTUALLY DO THE TRAVERSAL, REMOVE THE LAST NODE IN 'ROOT' BECAUSE ITS BS
    #https://www.programiz.com/dsa/huffman-coding

    return root

res = []
def traverse(node, arr=[]):
    if node:
        tmp = [*arr, node.bit] #instead, replace this node value with associated bit
        if not node.left and not node.right:
            res.append(tmp)
        traverse(node.left, tmp)
        traverse(node.right, tmp)

def getMin(sortedNodes):
    minimum = sortedNodes[0]
    for node in sortedNodes:
        if node.frequency < minimum.frequency:
            minimum = node
    return minimum

if __name__ == '__main__':
    root = huffman()
    traverse(root[-2])
    #removing the root node from path because it doesnt have bit val
    for code in range(len(res)):
        res[code] = res[code][1:]
    print(res)
