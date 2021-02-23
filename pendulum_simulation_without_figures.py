import numpy as np
import cv2
import time

from filterpy.kalman import MerweScaledSigmaPoints
from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import JulierSigmaPoints

from tkinter import messagebox

from tkinter import *
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class pendulum_simulation:
    def __init__(self, master):
        frame=Frame(master)
        frame.pack()
        
        self.pendulumbtn1=Button(frame, text="run me",bg="orange", fg="red" ,command=self.pendulum)
        self.pendulumbtn1.pack()   
        

    def pendulum(self):
    
        messagebox.showinfo('Message title', 'End simulation by clicking Esc button')

        # visulaization parameters
        height = 600
        width = 600

        # simulation 
        center = None

        # Pendulum parameters and variables

        #    initial conditions
        theta = np.pi/4 # the angle 
        omega = 0           # the angular velocity 

        #    parametrs
        g = 9.8 # m/s^2
        L = .2 # m
        m = 0.05 # kg
        b = 0.001  # friction constant 

        # Numerical integration parameters
        framerate = 60.0 # in frames per second
        dt = 1.0/framerate # Set dt to match the framerate of the webcam or animation
        t = time.clock()

        # Drawing parametres
        thickness = 3

        # Noise parameters 
        Sigma = 30*np.array([[1, 0],[0,1]])

        #Kalman inferred state variables
        theta_kf = theta
        omega_kf = omega
        #theta_kf_old = theta_kf
        #Keep looping

        # Create background image
        frame = np.zeros((height,width,3), np.uint8)

        center_old = (300, 300)
        center_noisy_old = (300, 300)
        center_kf_old = (300, 300)


        L_kf= 200
        # Create background image
        frame = np.zeros((height,width,3), np.uint8)

        cv2.circle(frame, (300, 300), 10, (0, 255, 255), -1)  

        ##################
        # ukf functions  #
        ##################
        #function to return the nonlinear state transition vatiables (theta, omega)
        def fx(X,dt):

            theta=X[0]
            omega=X[1]

            theta= theta+ omega*dt
            omega = omega - dt*g/L_kf*np.sin(theta) - dt*b/(m*L_kf*L_kf)*omega

            return np.c_[theta,omega]


        # The update step converts the sigmas into measurement space via the h(x) ,return theta and omega function[https://share.cocalc.com/share/7557a5ac1c870f1ec8f01271959b16b49df9d087/Kalman-and-Bayesian-Filters-in-Python/10-Unscented-Kalman-Filter.ipynb?viewer=share]
        
        def hx(X):

            return X 

        points = MerweScaledSigmaPoints(2, alpha=1e-3, beta=2., kappa=4)
        #points = JulierSigmaPoints(n=2, kappa=1)

        
        kf = UKF(dim_x=2, dim_z=2, dt=dt, fx=fx, hx=hx, points=points)
        kf.x = np.array([theta_kf ,omega_kf]) # initial state
       
        kf.R = Sigma # a measurement noise matrix  
        kf.Q = np.diag([4, 4])   # process noise the smae shape as the state variables 2X2  

        ######################
        # end ukf functions  #
        ######################

        global readings_noisy, readings_after_ukf,theta_theoritical
        readings_noisy= []
        readings_after_ukf=[]
        theta_theoritical=[]



        while True:
            cv2.circle(frame, (300, 300), 10, (0, 255, 255), -1)   
        # == Simulation model ==

            # Update state 
            theta = theta + dt*omega
            theta_theoritical.append(theta)
            omega = omega - dt*g/L*np.sin(theta) - dt*b/(m*L*L)*omega 

            # Map the state to a nearby pixel location
            center = np.array((int(300+ 200*np.sin(theta)) ,int(300 + 200*np.cos( theta))) ) 

            center_noisy = tuple(center+np.matmul(Sigma,np.random.randn(2)).astype(int))

            # Draw the pendulum

            cv2.circle(frame, tuple(center_old), 10, (0, 0, 0), -1)              
            cv2.circle(frame, center_noisy_old, 10, (0, 0, 0), -1)


            cv2.circle(frame, tuple(center), 10, (0, 255, 255), -1)                
            cv2.circle(frame, center_noisy, 10, (0, 0, 255), -1)                  

            center_old = center
            center_noisy_old = center_noisy


        ####################################################################
        #### here starts  the unscented kalman filter implementation       #
        ####################################################################
            center_noisy_kf=center_noisy
            readings_noisy.append(np.arctan( (center_noisy_kf[0]-300)/(center_noisy_kf[1]-300)))
            print('theoritical theta and omega',theta,omega)
            #unscented kalman filter pridection 
            kf.predict()
            #print('predicted theta and omega',kf.x[0],kf.x[1])

            theta_kf=kf.x[0]
            omega_kf=kf.x[1]
            print('predicted theta and omega',theta_kf,omega_kf)

            #center noisy kf update   
            # unscented kalman filter updating the state variables 
            kf.update([ (np.arctan( (center_noisy_kf[0]-300)/(center_noisy_kf[1]-300))),0])
            
            #print("after updtae",theta_kf)
            #maping the updated theta to the nearest pixels 
            center_kf = np.array((int(300+ L_kf*np.sin(kf.x[0])) ,int(300 + L_kf*np.cos(kf.x[0]))) )
            readings_after_ukf.append(np.arctan( (center_kf[0]-300)/(center_kf[1]-300)))

            ####################################################################
            #### here finishes the unscented kalman filter implementation      #
            ####################################################################

            # Map the state to a nearby pixel location

            cv2.circle(frame, tuple(center_kf_old), 10, (0, 0, 0), -1)
            center_kf_old = center_kf
            cv2.circle(frame, tuple(center_kf), 10, (255, 0, 255), -1)

            # show the frame to our screen
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(int(dt*400)) & 0xFF

            #if the 'Esc' key is pressed, stop the loop
            if key == 27:
                break


        # Wait with calculating next animation step to match the intended framerate
        t_ready = time.clock()
        d_t_animation = t + dt -  t_ready
        t += dt
        if  d_t_animation > 0:
            time.sleep(d_t_animation)


        # close all windows
        cv2.destroyAllWindows()
    


root = Tk()
root.geometry('350x350')

my_gui = pendulum_simulation(root)
root.mainloop()