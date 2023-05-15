# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : unit_table.py & Last Modded : 2023.05.12. ###
Coded with Python 3.10 Grammar by ????
Description : Unit Table Management Class
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import random
import aircraft_spec_sheet
import coordinates

class UnitTable(dict):
    """ UnitTable Management Class """

    def __init__(self):
        super().__init__()

        # load from json file
        #TODO
        
        self.table = table_generator()
        self.time = "0600"


    def random_base(self):
        n = random.randrange(0,3)   

        if n == 0:
            return "A"
        elif n == 1:
            return "B"
        else:
            return "C"

    def is_now(self, order):
        return order["order_id"] == self.order_num


    def get_coordinate(self, typeof_point, point):
        x = coordinates[typeof_point][point]["Latitude"]
        y = coordinates[typeof_point][point]["Longtitude"]

        return (x, y)


    def get_dist(self, l1, l2):
        return ((l1[0]-l1[1])**2 + (l2[0]-l2[1])**2)**0.5
        

    def time_adder(self, t1: str, t2: int):
        if int(t1[2:]) + t2 < 60:
            return str(int(t1) + t2)
        else:
            if int(t1[1]) == 9:
                return "10" + str(int(t1[2:]) + t2 - 60)
            else:
                return "0" + str(int(t1[1])+1) + str(int(t1[2:]) + t2 - 60)
            

    # update table when order made
    def update_table(self, data, n):
            
        if int(self.time[2]) == 4:
            if int(self.time[1]) == 9:
                self.time = "1000"
            else:
                self.time = "0" + str(int(self.time[1])+1) + "00"
        else:
            self.time = str(int(self.time)+20)


        operation = filter(is_now(n), data)

        for order in operation:
            self.table[order._aircraft_id]['Ordered'] = True
            self.table[order._aircraft_id]['Available'] = False #automatically changer when returned?

            # direct to target
            if order._mission_type == 1:
                time1 = get_dist(get_coordinate("Bases", self.table[order._aircraft_id]['base']), get_coordinate("Targets", order._target)) 
                time2 = time1
            
            # indirect to target
            elif order._mission_type == 2:
                time1 = get_dist(get_coordinate("Bases", self.table[order._aircraft_id]['base']), get_coordinate("Targets", order._target[0:2])) 
                time2 = time1

            # lake, direct to target 
            elif order._mission_type == 3:
                time1 = get_dist(get_coordinate("Bases", self.table[order._aircraft_id]['base']), get_coordinate("Lakes", "L1")) + get_dist(get_coordinate("Lakes", "L1"), get_coordinate("Targets", order._target))
                time2 = get_dist(get_coordinate("Targets", order._target), get_coordinate("Bases", self.table[order._aircraft_id]['base']))
            
            # lake, indirect to target
            elif order._mission_type == 4:
                time1 = get_dist(get_coordinate("Bases", self.table[order._aircraft_id]['base']), get_coordinate("Lakes", "L1")) 
                        + get_dist(get_coordinate("Lakes", "L1"), get_coordinate("Targets", order._target[0:2]))
                time2 = get_dist(get_coordinate("Targets", order._target[0:2]), get_coordinate("Bases", self.table[order._aircraft_id]['base']))
            
            
            # time1 : time to get to target, time2 : time to return from target
            self.table[order._aircraft_id]['ETD'] = time_adder(self.time, aircraft_spec_sheet[order._aircraft_id[0:2]]['ETRDY'])
            self.table[order._aircraft_id]['ETA'] = time_adder(table[order._aircraft_id]['ETD'], time1)

            self.table[order._aircraft_id]['ETR'] = time_adder(table[order._aircraft_id]['ETA'], time2)

    # Check if a aircraft returned
    def update_state(self, time: int):

        self.time = time_adder(self.time, time)
        for aircraft in self.table:
            if aircraft['Ordered'] and aircraft['ETR'] <= int(self.time):
                aircraft['Ordered'] = False
                aircraft['Available'] = True
                aircraft['ETR'] = None
                aircraft['ETD'] = None
                aircraft['ETA'] = None
                aircraft['Curren Water'] = 0


    def table_generator(self):
        table =         
        {
            "D1-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D1-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D2-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D2-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D3-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D3-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D4-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D4-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D5-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "D5-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H1-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H1-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H2-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H2-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H3-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H3-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H4-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H4-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H5-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "H5-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A1-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A1-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A2-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A2-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A3-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A3-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A4-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A4-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A5-A": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
            "A5-B": {
                "Ordered" : False,
                "Available" : True,
                "ETR" : None,
                "ETD" : None,
                "ETA" : None,
                "Base" : random_base(),
                "Current Water" : random.randrange(0,101)
            },
        }

        return table

    def to_json(self):
        #TODO
        pass




    #TODO: Create some caluculation methods for unit table

