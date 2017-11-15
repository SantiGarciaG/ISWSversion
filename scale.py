# Basic functions of the stimuli rating application:
# TODO: 1) Collects demographics such as: id, age, exp_group, other1, other2 (the latter two being just some multipurpose fields to append more info)
# 2) Presents instructions
# 3) Displays the images in the center with the 7-point Likert rating scale below (i.e., 1=Extremely pleasant; 2=Very plesant; 3=Somewhat plesant; 4 Neutral; 5=Somewhat unpleasant; 6= Very unplesant; 7=Extremely unpleasant)
# 4) The images are presented in a semi-random fashion, with the safeguard that no image is repeated within the same block (if it has appear, it won't be presented again)
# 5) Runs as many trials as images present in the "source folder"; where any number passed to a constant BLOCKS means number of repetitions 
# TODO: 6) Returns the data where columns correspond to id, age, group, other1, other2, img1.png, img2.png, img3.png (...etc for as many images included, and the headings of the columns are taken from the images' file-name and appended in aphanumeric order -so the databases from different participants match, so they can easily be combined using R)  
#       and the rows correspond to the data and scores ratings given to each of the images, so there would be as many rows as blocks (i.e., repeated presentation of each image)
 
 
# ---- Dependencies -----: 
from pygaze import libscreen, libtime, libinput
import os # for directory functions
import random
import csv
import numpy as np
from datetime import datetime
from psychopy.visual import ImageStim
from psychopy import visual 
from constants import *
import pygaze

# --------- Experiment --------------: 
 
class StimuliRating:
                                            # First, here we create the global variables that we use across functions
    screen_width = DISPSIZE[0]  
    screen_height = DISPSIZE[1]
    button_width = 50   # for the 'confirmButton' (confirming the rating and ending the trial) 
    button_height = 30
    scale_button_size = (100, 60) # for width and height dimensions
    
    rating_log_file_name = ''
    SBY = 310 # "Scale Button Y position" to raise it or lower it
    EYP = -215 # "Emoticon Y-axis Position" 
               
                                            # Here we create the screens used in the experiment         
    def initialize_screens(self):
        self.disp = libscreen.Display()     
        self.mouse = libinput.Mouse(visible = True)
        
                                                    #------ BEGINING OF THE EXPERIMENT (INSTRUCTIONS) ----------        
        self.intro_screen = libscreen.Screen()
        self.intro_screen.draw_text(text='''             **INSTRUCTIONS**
        
You will see a series of images at the center of the screen, and a rating system below. 

Please rate each of the images in accordance to how unpleasant you find them. 

Ask the experimenter if you have any questions, otherwise 

CLICK WITH THE MOUSE TO PROCEED... ''', fontsize=26)

                                        #-------------------- END OF EXPERIMENT INSTRUCTIONS ---------------------
        self.end_instructions = libscreen.Screen()
        self.end_instructions.draw_text(text="Congratulations! \n\n\nYou've finished this part of the experiment.\n\n\nPlease let the experimener know and thanks again for taking part in this .", fontsize=26)  

                                                    #------------------------ FIXATION POINT -------------------------       
        self.fixation = libscreen.Screen() 
        self.fixation.draw_fixation(fixtype= "cross", pw=10)       

                                                    #-------------------- VISUAL STIMULI (IMAGES) -----------------------
        self.visual_stimuli = libscreen.Screen()
        self.images = ImageStim(pygaze.expdisplay, pos = (0, 100)) # , image= "img/sr_images/" + random.choice(os.listdir("img/sr_images"))   
        self.visual_stimuli.screen.append(self.images)

                                                    #-------------------- CONFIRM -RATING- BUTTON ------------------------             
#        self.confirmButton_pos = (self.screen_width/2 - self.button_width/2, 335 + (self.screen_height/2 - self.button_height/2))
#        self.visual_stimuli.draw_rect(colour=(200,200,200),
#                                    x= self.confirmButton_pos[0], y= self.confirmButton_pos[1], 
#                                    w= self.button_width, h= self.button_height, pw=3)
#        self.visual_stimuli.draw_text(text="Confirm", pos=(self.screen_width/2, 335 + self.screen_height/2))

                                                    #--------------------- LIKERT SCALE BUTTON 0 -------------------------                     
        self.button0 = visual.Rect(win=pygaze.expdisplay, width=self.scale_button_size[0], height=self.scale_button_size[1],
                                lineColor=(200,200,200), lineWidth=3, lineColorSpace='rgb255', fillColor=None)
        self.button0_text = visual.TextStim(win=pygaze.expdisplay, text='No sensation', height=18)

        self.visual_stimuli.screen.append(self.button0)
        self.visual_stimuli.screen.append(self.button0_text)

                                                    #--------------------- LIKERT SCALE BUTTON 1 -------------------------                     
        self.button1_pos = ((self.screen_width/2 - self.scale_button_size[0]/2) - 500, self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2))
        self.visual_stimuli.draw_rect(x= (self.screen_width/2 - self.scale_button_size[0]/2) - 500, y= self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2), 
                                    w= self.scale_button_size[0], h= self.scale_button_size[1], pw=2)
        self.visual_stimuli.draw_text(text="Tickles", pos=(self.screen_width/2 - 500, self.SBY + self.screen_height/2), fontsize=18)                                    

                                                    #--------------------- LIKERT SCALE BUTTON 2 -------------------------                     
        self.button2_pos = ((self.screen_width/2 - self.scale_button_size[0]/2) - 330, self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2))
        self.visual_stimuli.draw_rect(x= (self.screen_width/2 - self.scale_button_size[0]/2) - 330, y= self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2), 
                                    w= self.scale_button_size[0], h= self.scale_button_size[1], pw=2)
        self.visual_stimuli.draw_text(text="Weak", pos=(self.screen_width/2 - 330, self.SBY + self.screen_height/2), fontsize=18)                                    

                                                    #--------------------- LIKERT SCALE BUTTON 3 -------------------------                     
        self.button3_pos = ((self.screen_width/2 - self.scale_button_size[0]/2) - 165, self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2))
        self.visual_stimuli.draw_rect(x= (self.screen_width/2 - self.scale_button_size[0]/2) - 165, y= self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2), 
                                    w= self.scale_button_size[0], h= self.scale_button_size[1], pw=2)
        self.visual_stimuli.draw_text(text="Mild", pos=(self.screen_width/2 - 165, self.SBY + self.screen_height/2), fontsize=18)                                    

                                                    #--------------------- LIKERT SCALE BUTTON 4 -------------------------                     
        self.button4_pos = (self.screen_width/2 - self.scale_button_size[0]/2, self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2))
        self.visual_stimuli.draw_rect(#colour= 'green',
                                    x= self.screen_width/2 - self.scale_button_size[0]/2, y= self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2), 
                                    w= self.scale_button_size[0], h= self.scale_button_size[1], pw=2)
        self.visual_stimuli.draw_text(text="Moderate", pos=(self.screen_width/2, self.SBY + self.screen_height/2), fontsize=18) #colour= 'black'                                    

                                                    #--------------------- LIKERT SCALE BUTTON 5 -------------------------                     
        self.button5_pos = ((self.screen_width/2 - self.scale_button_size[0]/2) + 165, self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2))
        self.visual_stimuli.draw_rect(x= (self.screen_width/2 - self.scale_button_size[0]/2) + 165, y= self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2), 
                                    w= self.scale_button_size[0], h= self.scale_button_size[1], pw=2)
        self.visual_stimuli.draw_text(text="Tolerable", pos=(self.screen_width/2 + 165, self.SBY + self.screen_height/2), fontsize=18)                                    

                                                    #--------------------- LIKERT SCALE BUTTON 6 -------------------------                     
        self.button6_pos = ((self.screen_width/2 - self.scale_button_size[0]/2) + 330, self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2))
        self.visual_stimuli.draw_rect(x= (self.screen_width/2 - self.scale_button_size[0]/2) + 330, y= self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2), 
                                    w= self.scale_button_size[0], h= self.scale_button_size[1], pw=2)
        self.visual_stimuli.draw_text(text="Strong", pos=(self.screen_width/2 + 330, self.SBY + self.screen_height/2), fontsize=18)                                    

                                                    #--------------------- LIKERT SCALE BUTTON 7 -------------------------                     
        self.button7_pos = ((self.screen_width/2 - self.scale_button_size[0]/2) + 500, self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2))
        self.visual_stimuli.draw_rect(x= (self.screen_width/2 - self.scale_button_size[0]/2) + 500, y= self.SBY + (self.screen_height/2 - self.scale_button_size[1]/2), 
                                    w= self.scale_button_size[0], h= self.scale_button_size[1], pw=2)
        self.visual_stimuli.draw_text(text="Unbearable", pos=(self.screen_width/2 + 500, self.SBY + self.screen_height/2), fontsize=18)                                    



                                        ## --------------------------------- SCALE EMOTICONS ------------------------------------  
        self.happyFace_img = visual.ImageStim(pygaze.expdisplay, image= 'resources/happyFace.png', pos = (-500, self.EYP))
        self.visual_stimuli.screen.append(self.happyFace_img)                                          
        
        self.neutralFace_img = visual.ImageStim(pygaze.expdisplay, image= 'resources/neutralFace.png', pos = (0, self.EYP))
        self.visual_stimuli.screen.append(self.neutralFace_img)  

        self.scaredFace_img = visual.ImageStim(pygaze.expdisplay, image= 'resources/scaredFace.png', pos = (500, self.EYP))
        self.visual_stimuli.screen.append(self.scaredFace_img)                                       

                                        #------ FUNCTIONS CONTAINING THE DIFFERENT PHASES OF THE EXPERIMENT ----------        


#    def initialize_log(self, exp_info):
#        log_name = 'data/' + exp_info['subj_id'] + '_' + exp_info['start_time'] + '_%s.txt'
#        self.rating_log_file_name = log_name % 'img_rating'
#
#        with open(self.rating_log_file_name, 'ab+') as fp:
#            writer = csv.writer(fp, delimiter = '\t')
#            writer.writerow(['subj_id', 'img_name', 'rating', 'latency'])
#                   
                             
#    def write_trial_log(self, log):     
#        with open(self.rating_log_file_name, 'ab+') as fp:
#            writer = csv.writer(fp, delimiter = '\t')
#            writer.writerow(log)
                   
        
#    def generate_subj_id(self):
#        existing_subj_ids = np.loadtxt('subj_ids.txt')
#        subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
#        while subj_id in existing_subj_ids:
#            subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
#
#        with open('subj_ids.txt', 'ab+') as fp:
#            writer = csv.writer(fp, delimiter = '\t')
#            writer.writerow([str(subj_id)])
#        return str(subj_id)


    def run_exp(self):
        
        self.initialize_screens()
#        exp_info = {}
#        exp_info['subj_id'] = self.generate_subj_id()        
#        exp_info['start_time'] = datetime.strftime(datetime.now(), '%b_%d_%Y_%H_%M_%S')        
        
#        self.initialize_log(exp_info)
        
        self.disp.fill(self.intro_screen)           # We show the screen we created with the begining of exp instructions
        self.disp.show()
        while True:
            if (self.mouse.get_pressed()[0]==1):
                break
        libtime.pause(500)  
        
        

        img_list = os.listdir("resources/neutral")
#        random.shuffle(img_list) #This shuffles the imgs before the for loop goes one by one 
        
        for img_name in img_list[:2]:
            
            self.disp.fill(self.fixation)      
            self.disp.show()
            libtime.pause(500)
            
#            self.images.setImage("img/sr_images/" + img_name) # I set the random img before presenting it
            self.disp.fill(self.visual_stimuli)      
            self.disp.show()

#            image_start_time = libtime.get_time()


            while True:
                mouse_position = self.mouse.get_pos()
    
                if (self.mouse.get_pressed()[0]==1):
                    if ((abs(mouse_position[0] - (self.button1_pos[0]+self.scale_button_size[0]/2)) < self.scale_button_size[0]/2) and 
                        (abs(mouse_position[1] - (self.button1_pos[1]+self.scale_button_size[1]/2)) < self.scale_button_size[1]/2)):
                        rating = 1
                        break
    
                    elif ((abs(mouse_position[0] - (self.button2_pos[0]+self.scale_button_size[0]/2)) < self.scale_button_size[0]/2) and 
                        (abs(mouse_position[1] - (self.button2_pos[1]+self.scale_button_size[1]/2)) < self.scale_button_size[1]/2)):
                        rating = 2
                        break
                    
                    elif ((abs(mouse_position[0] - (self.button3_pos[0]+self.scale_button_size[0]/2)) < self.scale_button_size[0]/2) and 
                        (abs(mouse_position[1] - (self.button3_pos[1]+self.scale_button_size[1]/2)) < self.scale_button_size[1]/2)):
                        rating = 3
                        break
    
                    elif ((abs(mouse_position[0] - (self.button4_pos[0]+self.scale_button_size[0]/2)) < self.scale_button_size[0]/2) and 
                        (abs(mouse_position[1] - (self.button4_pos[1]+self.scale_button_size[1]/2)) < self.scale_button_size[1]/2)):
                        rating = 4
                        break
    
                    elif ((abs(mouse_position[0] - (self.button5_pos[0]+self.scale_button_size[0]/2)) < self.scale_button_size[0]/2) and 
                        (abs(mouse_position[1] - (self.button5_pos[1]+self.scale_button_size[1]/2)) < self.scale_button_size[1]/2)):
                        rating = 5 
                        break
    
                    elif ((abs(mouse_position[0] - (self.button6_pos[0]+self.scale_button_size[0]/2)) < self.scale_button_size[0]/2) and 
                        (abs(mouse_position[1] - (self.button6_pos[1]+self.scale_button_size[1]/2)) < self.scale_button_size[1]/2)):
                        rating = 6
                        break
                
                    elif ((abs(mouse_position[0] - (self.button7_pos[0]+self.scale_button_size[0]/2)) < self.scale_button_size[0]/2) and 
                        (abs(mouse_position[1] - (self.button7_pos[1]+self.scale_button_size[1]/2)) < self.scale_button_size[1]/2)):
                        rating = 7
                        break
                    
                if self.mouse.mouse.isPressedIn(self.button0):
                    rating = 0
                    break                
                    
                    
#            latency = libtime.get_time() - image_start_time
            
#            trial_info = [exp_info['subj_id'], img_name, rating, latency]
#            self.write_trial_log(trial_info)            
            
            libtime.pause(500) 

        self.disp.fill(self.end_instructions)
        self.disp.show()
        while True:
            if (self.mouse.get_pressed()[0]==1):
                break
        libtime.pause(500)  

        self.disp.close()



sr_app = StimuliRating()
sr_app.run_exp()
