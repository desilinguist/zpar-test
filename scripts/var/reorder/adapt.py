import sys
import getopt
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../dep"))
import depio
import dep
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../ml"))
import orng
import gzip

#========================================

def readModel(path, bTrain):
   if bTrain: model = orng.COrangeWriter(path, bTrain)
   else: model = orng.COrange(path, bTrain)
   return model

def readAlign(path):
   retval = {}
   n=0
   file = gzip.open(path)
   for line in file:
      if not line.strip():
         continue
      if line.startswith('SENT:'):
#         number = int(line[6:-1])
#         assert number == n # make sure of sentence index
         if n>0:
            yield retval
            retval = {}
         n += 1
      else:
         assert line.startswith('S ')
         target, source = map(int, line[2:-1].split())
         if not source in retval:
            retval[source] = []
         retval[source].append(target)
   yield retval
   file.close()

#========================================

def printOrderForNode(node):
   retval = []
   for left_child in node.left_children:
      retval.extend(printOrderForNode(left_child))
   retval.append(str(node.extra))
   for right_child in node.right_children:
      retval.extend(printOrderForNode(right_child))
   return retval

def printOrder(tree):
   retlst = printOrderForNode(tree.root)
   retval = ' '.join(retlst)
   return retval

#========================================

def updateIndexForNode(node, index):
   node.extra = node.word_index
   node.word_index = index
   return index+1

def updateIndexForTree(node, index):
   for left_child in node.left_children:
      index = updateIndexForTree(left_child, index)
   index = updateIndexForNode(node, index)
   for right_child in node.right_children:
      index = updateIndexForTree(right_child, index)
   return index

def updateIndex(tree):
   updateIndexForTree(tree.root, 0)

#========================================

def recordOrder(bReorder, node1, node, nPUBetween, model):
   def normalize(i):
      if i > 10: return '10'
      elif i > 5: return '5'
      else: return str(i)
   node_reordered = 'n'
   if bReorder:
      node_reordered = 'y'
   head_word = node.token
   head_pos = node.pos
   head_size = normalize(node.size)
   modifier_word = node1.token
   modifier_pos = node1.pos
   modifier_size = normalize(node1.size)
   pu_between = normalize(nPUBetween)
   modifier_lmod_word = "-NONE-"
   modifier_lmod_pos = "-NONE-"
   if node1.left_children:
      modifier_lmod_word = node1.left_children[0].token
      modifier_lmod_pos = node1.left_children[0].pos
   modifier_rmod_word = "-NONE-"
   modifier_rmod_pos = "-NONE-"
   if node1.right_children:
      modifier_rmod_word = node1.right_children[-1].token
      modifier_rmod_pos = node1.right_children[-1].pos
   modifier_lleaf_word = "-NONE-"
   modifier_lleaf_pos = "-NONE-"
   if node1.leftmost_leaf:
      modifier_lleaf_word = node1.leftmost_leaf.token
      modifier_lleaf_pos = node1.leftmost_leaf.pos
   modifier_rleaf_word = "-NONE-"
   modifier_rleaf_pos = "-NONE-"
   if node1.rightmost_leaf:
      modifier_rleaf_word = node1.rightmost_leaf.token
      modifier_rleaf_pos = node1.rightmost_leaf.pos
   model.setFeatureDefs(['head_word', 'head_pos', 'head_size', 'modifier_word', 'modifier_pos', 'modifier_size', 'pu_between', 'modifier_lmod_word', 'modifier_lmod_pos', 'modifier_rmod_word', 'modifier_rmod_pos', 'modifier_lleaf_word', 'modifier_lleaf_pos', 'modifier_rleaf_word', 'modifier_rleaf_pos', 'reorder'], ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd'], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'class'])
   model.addExample([head_word, head_pos, head_size, modifier_word, modifier_pos, modifier_size, pu_between, modifier_lmod_word, modifier_lmod_pos, modifier_rmod_word, modifier_rmod_pos, modifier_lleaf_word, modifier_lleaf_pos, modifier_rleaf_word, modifier_rleaf_pos, node_reordered])

def crossLink(node1, node2, align):
   count = 0
   total = 0

   # do not crosslink if head non
   indice = align.get(node2.word_index, [])
   if not indice:
      return False
   head_index = indice[0]

   for index in range(node1.leftmost_leaf.word_index, node1.rightmost_leaf.word_index):
      indice = align.get(index, 0)
      if not indice:
         continue
      total += 1
      if indice[0] > head_index:
         count += 1

   # do not crosslink if non
   if not total:
      return False

   if count > total / 2:
      return True
   return False

def reorderVV(node, align, model):
   left_children = []
   nPUBetween = 0
   while node.left_children:

      left_child = node.left_children.pop(-1) # for each left
      bReorder = False

      if left_child.pos in ['P']:
         if align and crossLink(left_child, node, align):
            node.right_children.append(left_child)
            bReorder = True
      elif left_child.pos in ['NT', 'M', 'CD', 'OD']:
         if align and crossLink(left_child, node, align):
            node.right_children.insert(0, left_child)
            bReorder = True
      elif left_child.pos in ['PU']:
         nPUBetween += 1

      if not bReorder: 
         left_children.insert(0, left_child)

      if align:
         recordOrder(bReorder, left_child, node, nPUBetween, model)

   node.left_children = left_children

def reorderNN(node, align, model):
   left_children = []
   nPUBetween = 0
   while node.left_children:
      left_child = node.left_children.pop(-1) # for each left
      bReorder = False
      if left_child.pos == 'DEC' or left_child.pos == 'DEG':
         if align and crossLink(left_child, node, align):
            reorderDEG(left_child, align, model)
            node.right_children.insert(0, left_child)
            bReorder =  True
      elif left_child.pos == 'PU':
         nPUBetween += 1

      if not bReorder: 
         left_children.insert(0, left_child)

      if align:
         recordOrder(bReorder, left_child, node, nPUBetween, model)

   node.left_children = left_children

def reorderDEG(node, align, model):
   while node.left_children:
      left_child = node.left_children.pop(0)
      node.right_children.insert(0, left_child)

def reorderLC(node, align, model):
   while node.left_children:
      left_child = node.left_children.pop(0)
      node.right_children.insert(0, left_child)

def reorderNode(node, align, model):
   # recursion
   for left_child in node.left_children:
      reorderNode(left_child, align, model)
   for right_child in node.right_children:
      reorderNode(right_child, align, model)
   # ver
   if node.pos == 'VV':
      reorderVV(node, align, model)
   # n.
   elif node.pos in ['NN', 'NR']:
      reorderNN(node, align, model)
   # lc
   elif node.pos == 'LC':
      reorderLC(node, align, model)

def reorder(tree, align, model):
   reorderNode(tree.root, align, model)
   updateIndex(tree)

#========================================

def posCompare(pos1, pos2):
   order = {'PU':-1, 'NN':10, 'AS':11}
   return cmp(order.get(pos1, 0), order.get(pos2, 0))

def sizeCompare(node1, node2):
   if node1.size > 1.5*node2.size: # significantly smaller
      return -1 # nearer
   if node2.size > 1.5*node1.size:
      return 1
   return 0

def compare(node1, node2):
   retval = posCompare(node1.pos,node2.pos)
   if retval:
      return retval
   retval = sizeCompare(node1, node2)
   return retval

def deg(node):
   assert node.pos == 'DEG'
   for left_child in node.left_children:
      if left_child.pos == 'JJ':
         return False
   return True

#========================================

if __name__ == '__main__':
   opts, args = getopt.getopt(sys.argv[1:], "o:i:")
   if len(args) < 1:
      print 'adapt [-ia|c] [-oi|r|p|d] input model [align]'
      sys.exit(0)

   # get parameter
   sOutput = 'd'
   sInput = 'a'
   for opt, val in opts:
      if opt == '-o':
         sOutput = val
      if opt == '-i':
         sInput = val

   # input
   alignFile = None
   align = None
   model = None
   if sInput == 'a':
      if len(args) != 3:
         print "The alignment file must be provided with -ia"
         sys.exit(0)
      model = readModel(args[1], True)
      alignFile = readAlign(args[2]) 
   elif sInput == 'c':
      model = readModel(args[1], False)
   else:
      print 'The input format is invalid'
      sys.exit(0)

   for tree in depio.depread(args[0]):
      if alignFile:
         align = alignFile.next()
      dept = dep.CDep(tree)
      reorder(dept, align, model)
      if sOutput == 'd':
         print dept
      elif sOutput == 'p':
         print dept.toPOS()
      elif sOutput == 'r':
         print dept.toRaw()
      elif sOutput == 'i':
         print printOrder(dept)
      else:
         print "The output type is not valid"
         sys.exit(0)
   if align:
      model.train()
