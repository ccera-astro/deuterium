"""
A Logger for the IDEA Deuterium project

We accumulate average spectra in two categories
   o Main -- 97% of the samples go here
   o Baseline - 3% of the samples go here

The idea is that because the D1 line is soooooo very weak, we can
  "baseline" just using a very small amount of the sky data itself, because
  less than 1 part in 1e6 will contain the actual line.

We log on a daily basis, so baselining is done on a daily basis. The resulting
  baselined spectrum is logged once per day.  In post-processing a "grand"
  integration can be done over many many days, and many many stations.
  
"""

import numpy as np
from gnuradio import gr
import time
import random
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """A Logger for the IDEA Deuterium project """

    def __init__(self, fftsize=1024,outfile="deuterium-"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Deuterium Logger',   # will show up in GRC
            in_sig=[(np.float32,fftsize)],
            out_sig=None
        )
        #
        # Output file prefix here
        #
        self.outfile = outfile
        
        #
        # Create averaging buffers for both main and baseline
        #
        self.main = np.zeros(fftsize)
        self.baseline = np.zeros(fftsize)
        self.maincount = 0
        self.basecount = 0
        
        #
        # Record start time
        #
        self.startt = time.time()
        
        #
        # Seed the random number generator
        #
        random.seed()

    def work(self, input_items, output_items):
        """Log vector from FFT"""
        
        for v in input_items[0]:
			#
			# With P ~= 0.03, compute a baseline average
			#
			#
			# Else add it to the main average
			#
            x = random.randint(0,30)
            if (x == 1):
                self.baseline = np.add(self.baseline,v)
                self.basecount += 1
            else:
                self.main = np.add(self.main, v)
                self.maincount += 1
            #
            # Once a day, compute averages, log
            #
            if ((time.time() - self.startt) >= 86100):
				
				#
				# Determine filename
				#
                ltp = time.gmtime()
                fn = self.outfile + "%04d%02d%02d" % (ltp.tm_year,ltp.tm_mon,ltp.tm_mday) + ".csv"
                
                #
                # Open it
                #
                fp = open (fn, "w")
                
                #
                # Write the TOD header
                # Removed for now to make plotting easier
                #
                #fp.write ("%02d,%02d,%02d," % (ltp.tm_hour, ltp.tm_min, ltp.tm_sec))
                # 
                
                #
                # Compute the average of the main buffer
                #
                avgmain = np.divide(self.main,self.maincount)
                
                #
                # Compute the average of all samples on the input
                # We'll use that to adjust the baselined version
                #
                avg = sum(avgmain)/len(v)
                
                #
                # If there ARE baseline samples
                if (self.basecount > 0):
                    avgbase = np.divide(self.baseline, self.basecount)
                else:
                    avgbase = self.baseline
                    
                #
                # Subtract out the baseline
                adjusted = np.subtract(avgmain, avgbase)
                
                #
                # Adjust back up to average previous level
                #
                adjusted = np.add(adjusted, avg)
                
                #
                # Reset both averaging buffers and counters
                #
                self.main = np.zeros(len(v))
                self.baseline = np.zeros(len(v))
                self.maincount = 0
                self.basecount = 0
                
                #
                # Write out the (adjusted) values
                #
                i = 0
                for val in adjusted:
                    fp.write ("%9.5e" % val)
                    i += 1
                    #
                    # Don't write a trailing ","
                    #
                    if (i < len(v)):
                        fp.write(",")
                fp.write("\n")
                fp.close()
                
                #
                # Reset our logging timer
                #
                self.startt = time.time()
                    
            
        return len(input_items[0])
