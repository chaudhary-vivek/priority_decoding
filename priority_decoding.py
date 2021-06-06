# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 18:51:07 2021

@author: Vivek
"""
##############################################################################
# inputs : 
# chromosome
# capacity of nodes
# types of nodes
# cost matrix

##############################################################################
# output (in single dataframe) : 
# quantity shipped between nodes.
# cost of shipping between nodes.


##############################################################################
#importing the libraries
##############################################################################
import pandas as pd


##############################################################################
#entering the inputs : 
# input 1, chromosome, a list containing 7 digits from 1 to 6
# input 2 list of nodes containing the chromosome index, type and capacity
##############################################################################
chromosome = [2,5,3,7,4,1,6]
lists = [[0, 0, 's', 550],[1, 1, 's', 300],[2, 2, 's', 450],
         [3, 0, 'd', 300],[4, 1, 'd', 350],[5, 2, 'd', 300],[6, 3, 'd', 350]]
cost_lists = [[11,19,17,18,],[16,14,18,15],[15,16,19,13]]


##############################################################################
#encoding the inputs as dataframes : node details and the rate matrix
############################################################################## 
nodes = pd.DataFrame(lists, columns = ['cind', 'typeind', 'nodetype', 'capacity'])
costs = pd.DataFrame(cost_lists, columns = ['0', '1', '2', '3'])


##############################################################################
#encoding the output as a df that will contain the fromand to node and qty
############################################################################## 
vertices = []


##############################################################################
#max_priority is the index of the highest priority node in the chromosome.
#top_node_type contains if the node is a source or depot(s or d)
#top_nodetype_ind is the index of the node in its own type (souce or depot)
##############################################################################
max_priority = 9999999999999999999999
i = 0
while max_priority != 0 : 
    print('iteration ' +str(i) )    
    max_priority = chromosome.index(max(chromosome))
    top_node = nodes[nodes.cind == max_priority]
    top_node_type = top_node.iloc[0,2]
    type_index = top_node.iloc[0,1]
        
    
    ##############################################################################
    #returns the best corresponding node with the lowest cost.
    #best_cost is the lowest cost in the correspomding node type
    #best_cost_index returns the index of the node with the lowest cost
    ##############################################################################
    if top_node_type == 'd':
        best_cost = costs.min(axis =0)[type_index]
        best_cost_index = int(costs.idxmin(axis =0)[type_index])
        best_cost_cind = best_cost_index
    elif top_node_type == 's':
        best_cost = costs.min(axis =1)[type_index]
        best_cost_index = int(costs.idxmin(axis =1)[type_index])
        #change  3 based on the number of source noeds
        #
        #
        #
        best_cost_cind = best_cost_index+3
        
    print('the best cost is: \n ' + str(best_cost))
    print('the best cost index is: \n ' + str(best_cost_cind))
        
    ##############################################################################
    #this will take bes_cost_index and type_index as input
    #return quantity shipped
    #update the capacity in nodes df 
    #update the chromosome
    ##############################################################################
    nodea = nodes[nodes.cind == best_cost_cind]
    nodeb = nodes[nodes.cind == max_priority]
    
    #finding the amount transferable between the two nodes
    nodea_capacity = nodea.iloc[0,3]
    nodeb_capacity = nodeb.iloc[0,3]
    transferable = min(nodea_capacity, nodeb_capacity)
    
    #Updating the capacities in the node table
    nodes.iloc[max_priority, 3] = nodes.iloc[max_priority, 3] - transferable
    nodes.iloc[best_cost_cind, 3] = nodes.iloc[best_cost_cind, 3] - transferable
    
    #Updating the costs to 999999 in nodes which have 0 capacity
    #Change the number of 999 based on the matrix size
    #
    #
    #
    
    if nodes.iloc[max_priority, 3] == 0:
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print( nodes.iloc[max_priority, 2])
        exhausted_cap_type = nodes.iloc[max_priority, 2]
        exhausted_cap_typeind = int(nodes.iloc[max_priority, 1])
        if exhausted_cap_type == 'd':
            costs.iloc[:,exhausted_cap_typeind] = [999,999,999]
        elif exhausted_cap_type == 's':
            costs.loc[exhausted_cap_typeind, :] = [999,999,999,999]
                
    if nodes.iloc[best_cost_cind, 3] == 0:
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        nodes.iloc[best_cost_cind, 2]
        exhausted_cap_type = nodes.iloc[best_cost_cind, 2]
        exhausted_cap_typeind = int(nodes.iloc[best_cost_cind, 1])
        if exhausted_cap_type == 'd':
            costs.iloc[:,exhausted_cap_typeind] = [999,999,999]
        elif exhausted_cap_type == 's':
            costs.loc[exhausted_cap_typeind, :] = [999,999,999,999]    
   
    #updating the chromosome
    
    if nodea.iloc[0,3] < nodeb.iloc[0,3]:
        satisfied_node_cind = nodea.iloc[0,0]
        chromosome[satisfied_node_cind] = 0
    elif nodea.iloc[0,3] > nodeb.iloc[0,3]:
        satisfied_node_cind = nodeb.iloc[0,0]
        chromosome[satisfied_node_cind] = 0
    elif nodea.iloc[0,3] == nodeb.iloc[0,3]:
        satisfied_node_cind = nodea.iloc[0,0]
        satisfied_node_cind2 = nodeb.iloc[0,0]
        chromosome[satisfied_node_cind] = 0
        chromosome[satisfied_node_cind2] = 0
    print('chromosome == ' + str(chromosome))
    

    
    #updating the output table
    if nodea.iloc[0,2] == 's':
        source = nodea.iloc[0,1]
        destination = nodeb.iloc[0,1]
    else:
        source = nodeb.iloc[0,1]
        destination = nodea.iloc[0,1]
        
    total_cost = transferable*best_cost

    
    df_item = {
       'from' : source,
       'to': destination,
       'quantity': transferable,
       'cost' : total_cost}
    
    vertices.append(df_item)
    
    i = i+ 1
    print( '#########################################################')




vertices_df = pd.DataFrame(vertices)

