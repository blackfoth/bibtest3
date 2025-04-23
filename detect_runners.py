from collections import Counter

class detect_runners:
    found_runners =[]
    
    
    def add_runner(self,id,value):
        runner =[]
        values= []
        found = False
        for r in self.found_runners:
            if r[0] == (id) and r[2] == False:
                r[1].append(value)
                found = True
        if found == False:
            #add ID at pos 0
            runner.append(id)
            
            values.append(value)
            # add values at pos 1
            runner.append(values)
            # add finish flag at pos 2
            runner.append(False)
            #append all above to found runners
            self.found_runners.append(runner)

    
    
    def print_runners(self):
        for entry in self.found_runners:
            print("ID: ",entry[0])
            for value in entry[1]:
                print("value: ",value)
    
    
    def finish_runner(self,id):
        for r in self.found_runners:
             if r[0] == (id):
                r[2] = True
                most_common = Counter(r[1]).most_common(1)[0][0]
        return most_common
    
    def is_finished(self,id):
        for r in self.found_runners:
             if r[0] == (id):
                 return r[2]
        return False 


