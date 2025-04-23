import time
import os

starttime = time.time()
race_started = False




class racestopwatch:
     def __init__(self):
         self.start_times = [None] * 10

     def start_race(self,raceindex):
          
     # while race_started == True:
             
     #          end = time.time()
     #          time.sleep(0.1)
     #          time_taken= end -starttime
     #          #self.start_times.insert(raceindex, f"Start Time: {round(time_taken, 2)}")
     #          self.start_times[raceindex] = f"elapsed time: {round(time_taken, 3)}"
     #          print(self.start_times)

          self.start_times[raceindex] = time.time()
          #print(f"Race {raceindex} started at: {round(self.start_times[raceindex], 3)}")
     
     
     def stop_race(self,raceindex):
         self.start_times[raceindex] = None
            
    
     def get_time(self,raceindex):
          # Check if the race has started
          if self.start_times[raceindex] is None:
            return "Race hasn't started yet 😢"
          current_time = time.time()
          elapsed_time = round(current_time - self.start_times[raceindex], 3)
          return  elapsed_time
     def get_formatted_time(self,raceindex):
        duration= self.get_time(raceindex)
          # Convert duration to struct_time
        time_struct = time.gmtime(duration)

        # Extract hours, minutes, and seconds
        hours = time_struct.tm_hour
        minutes = time_struct.tm_min
        seconds = time_struct.tm_sec
        milliseconds = int((duration % 1) * 1000)

        # Format the output
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"




# race_stopwatch =racestopwatch()
# race_stopwatch.start_race(3)  # Start race at index 3

# get_time =race_stopwatch.get_time(3)
# print(get_time)

# print(race_stopwatch.get_formatted_time(3))

# Get elapsed time for race 3