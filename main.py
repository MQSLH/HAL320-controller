import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.constants import HORIZONTAL
import serialComm
import serial.tools.list_ports
import logging
import time


class mainWindow:
    def __init__(self,tkRoot):

        tkRoot.protocol("WM_DELETE_WINDOW",self.onWindowClose)
        tkRoot.report_callback_exception = self.handleExceptions
        self.master = tkRoot
        self.master.title("HAL320W control")

        self.choppingOnTime = 1
        self.choppingOffTime = 1
        self.chopping = False
        self.timerRunning = False


        buttonWidth = 10
        buttonHeight = 5

        framePady = 5
        framePadx = 5
        elementPadx = 20

        self.mainFrame = tk.Frame(tkRoot)

        self.mainFrame.grid(row=1, column=0, padx=5)

        self.lampFrame = ttk.Labelframe(self.mainFrame, text='lamp')
        self.lampFrame.grid(row = 3,column= 0, padx = framePadx, pady = framePady, sticky='w')

        self.connectionFrame = ttk.Labelframe(self.mainFrame, text='connection', width=150, height=100)
        self.connectionFrame.grid(row = 3,column= 1, rowspan=2, padx = framePadx, pady = framePady, sticky='nw')

        self.intensityFrame = ttk.Labelframe(self.mainFrame, text='intensity (%)')
        self.intensityFrame.grid(row = 4,column= 0, padx = framePadx, pady = framePady, sticky='w')

        self.shutterTimerFrame = ttk.Labelframe(self.mainFrame, text='shutter timer (s)')
        self.shutterTimerFrame.grid(row = 5,column= 0, padx = framePadx, pady = framePady, sticky='w')
         
        self.lampTimerFrame = ttk.Labelframe(self.mainFrame, text='lamp timer (s)')
        self.lampTimerFrame.grid(row = 6,column= 0, padx = framePadx, pady = framePady, sticky='w')

        self.chopFrame = ttk.Labelframe(self.mainFrame, text='chopping')
        self.chopFrame.grid(row = 7,column= 0, columnspan=2, padx = framePadx, pady = framePady, sticky='w')

        self.btn_power = tk.Button(self.lampFrame, text='power', width=buttonWidth, command=self.onPowerButton)
        self.btn_power.grid(row=0,column=0, pady = framePady)  

        self.lbl_conn_status = tk.Label(self.connectionFrame, text = 'No lamp connected',font=("Helvetica", 12))
        self.lbl_conn_status.place(x=5,y=0,anchor='nw')

        self.btn_shutter = tk.Button(self.lampFrame, text='shutter', width=buttonWidth, command=self.onShutterButton)
        self.btn_shutter.grid(row=0, column=1, pady = 10)
        
        self.btn_intensity = tk.Button(self.intensityFrame, text='set', width=buttonWidth, command = self.onIntensityButton)
        self.btn_intensity.grid(row=0,column = 0, pady = 10)
        


        intvcmd = (tkRoot.register(self.validateIntensity), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        intivcmd = (tkRoot.register(self.invalidIntensity), '%s', '%W')
        self.entry_intensity = tk.Entry(self.intensityFrame, width = 10, validate = 'key',validatecommand = intvcmd,invalidcommand=intivcmd)
        self.entry_intensity.grid(row = 0, column = 1, padx = 5)
        self.entry_intensity.insert(0,'20')

        self.btn_timer = tk.Button(self.shutterTimerFrame, text='start', width=buttonWidth, command=self.onTimerButton)
        self.btn_timer.grid(row=0, column=0, pady = 10)

        vcmd = (tkRoot.register(self.validateTimer), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ivcmd = (tkRoot.register(self.invalid), '%s', '%W')
        self.entry_timer = tk.Entry(self.shutterTimerFrame, width = 10, validate = 'key',validatecommand = vcmd,invalidcommand=ivcmd)
        self.entry_timer.grid(row=0,column=1, padx = 5)
        self.entry_timer.insert(0,'10')


        self.btn_lamptimer = tk.Button(self.lampTimerFrame, text='start', width=buttonWidth, command=self.onLampTimerButton)
        self.btn_lamptimer.grid(row=0, column=0, pady = 10)

        vcmd = (tkRoot.register(self.validateLampTimer), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        ivcmd = (tkRoot.register(self.invalid), '%s', '%W')
        self.entry_lamptimer = tk.Entry(self.lampTimerFrame, width = 10, validate = 'key',validatecommand = vcmd,invalidcommand=ivcmd)
        self.entry_lamptimer.grid(row=0,column=1, padx = 5)
        self.entry_lamptimer.insert(0,'10')


        self.btn_chop = tk.Button(self.chopFrame, text= 'chop', width=buttonWidth, command=self.onChopButton)
        self.btn_chop.grid(row = 1, column = 0, pady = 10)

        self.lbl_chop_on = tk.Label(self.chopFrame, text = 'on time (s)')
        self.lbl_chop_off = tk.Label(self.chopFrame, text = 'off time (s)')

        self.lbl_chop_on.grid(row = 0, column = 1, padx = 5)
        self.lbl_chop_off.grid(row = 0, column = 2, padx = 5)

        self.entry_chop_on = tk.Entry(self.chopFrame, width = 5, validate = 'key',validatecommand = vcmd,invalidcommand=ivcmd)
        self.entry_chop_off = tk.Entry(self.chopFrame, width = 5, validate = 'key',validatecommand = vcmd,invalidcommand=ivcmd)
        
        self.entry_chop_on.grid(row = 1, column = 1, padx = 5)
        self.entry_chop_off.grid(row = 1, column = 2, padx = 5)
        self.entry_chop_on.insert(0,'1')
        self.entry_chop_off.insert(0,'1')


        self.disableButtons([])

        ports = serial.tools.list_ports.comports()
        available_ports = ['test']

        for p in ports:
            available_ports.append(p.device)

        available_ports = sorted(available_ports)
        s = ', '
        logging.info('Ports found:' +s.join(available_ports))

        self.commOption = tk.StringVar(self.mainFrame)
        self.commOption.set('Select Port')
        self.commOption.trace("w",self.onPortSelect)
        
        self.opt_comm = tk.OptionMenu(self.connectionFrame,self.commOption,*available_ports)
        self.opt_comm.config(width=10)
        self.opt_comm.place(x = 5, y = 40, anchor='nw')

        logging.info('GUI constructed')




    def validateTimer(self,action,index,value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if not value_if_allowed:
            valid = True
        else:
            try:
                value = float(value_if_allowed)
                valid = value>=0 and value <= 99999
            except ValueError:
                valid = False
        return valid

    def validateLampTimer(self,action,index,value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if not value_if_allowed:
            valid = True
        else:
            try:
                value = float(value_if_allowed)
                valid = value>=0 and value <= 999999
            except ValueError:
                valid = False
        return valid


    def invalid(self, prior_value, widget_name):

        widget = self.entry_timer.nametowidget(widget_name)

        widget.delete(0,'end')
        widget.insert(0,prior_value)
        widget.after_idle(lambda: widget.config(validate='key'))

 
    def validateIntensity(self,action,index,value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if not value_if_allowed:
            valid = True
        else:
            try:
                value = int(value_if_allowed)
                valid = value>=0 and value <= 1000
            except ValueError:
                valid = False
        return valid

    def invalidIntensity(self, prior_value, widget_name):

        widget = self.entry_timer.nametowidget(widget_name)

        widget.delete(0,'end')
        widget.insert(0,prior_value)
        widget.after_idle(lambda: widget.config(validate='key'))

    def onIntensityButton(self):
        try:
            intensity = int(float(self.entry_intensity.get()))
            if intensity < 20:
                intensity = 20
                self.entry_intensity.delete(0,'end')
                self.entry_intensity.insert(0,'20')

            if intensity > 100:
                intensity = 100
                self.entry_intensity.delete(0,'end')
                self.entry_intensity.insert(0,'100')


            self.comm.setIntensity(intensity)
            self.lamp.intensity = intensity
            logging.info('intensity set to '+str(intensity))
        except:
            logging.exception('Error setting intensity')

    def onPowerButton(self):
        if self.lamp.lampOn:
            togglecheckstr = 'Are you sure you want to turn off the lamp?'
        else:
            togglecheckstr = 'Are you sure you want to turn on the lamp?'

        powercheck = messagebox.askokcancel('Toggle lamp?',togglecheckstr, default = 'cancel', parent=self.mainFrame)
        if powercheck:
            try:
                self.lamp.lampOn = self.comm.togglePower(self.lamp.lampOn)
                logging.info('lamp set to '+str(self.lamp.lampOn))
            except:
                logging.exception('Error setting lamp')

    def onShutterButton(self):
        try:
            self.lamp.shutterOpen = self.comm.toggleShutter(self.lamp.shutterOpen)
            logging.info('shutter set to '+str(self.lamp.shutterOpen))
        except:
            logging.exception('Error setting shutter')


    def onTimerButton(self):
        try:
            if self.timerRunning:
                self.mainFrame.after_cancel(self.timerAfter) # pylint: disable=access-member-before-definition
                self.mainFrame.after(1000,self.timerEndShutterClose)
                logging.info('stopped timer early')

            else:
                self.timerRunning = True
                delay = int(1000*float(self.entry_timer.get()))

                logging.info('started timer: '+str(delay/1000)+' s')   
                if not self.lamp.shutterOpen:
                    self.lamp.shutterOpen = self.comm.toggleShutter(self.lamp.shutterOpen)
                
                self.timerCountDown(delay)
                self.disableButtons([self.btn_timer])
        except:
            logging.exception('Error with timer')


    def onLampTimerButton(self):
        try:
            if self.timerRunning:
                self.mainFrame.after_cancel(self.timerAfter) # pylint: disable=access-member-before-definition
                self.mainFrame.after(1000,self.timerEndShutterClose)
                logging.info('stopped lamp timer early')

            else:
                self.timerRunning = True
                delay = int(1000*float(self.entry_lamptimer.get()))

                logging.info('started lamp timer: '+str(delay/1000)+' s')   
                if not self.lamp.shutterOpen:
                    self.lamp.shutterOpen = self.comm.toggleShutter(self.lamp.shutterOpen)
                
                self.lamptimerCountDown(delay)
                self.disableButtons([self.btn_lamptimer])
        except:
            logging.exception('Error with lamp timer')


    def lamptimerCountDown(self,delay,iteration=0):

        timeLeft = delay-1000*iteration
        timeStr = str(round(timeLeft/1000))
        self.entry_lamptimer.delete(0,'end')
        self.entry_lamptimer.insert(0,timeStr)

        if timeLeft>0:
            self.timerAfter = self.mainFrame.after(1000,self.lamptimerCountDown,delay,iteration+1)
        else:
            timeStr = str(round(delay/1000))
            self.entry_lamptimer.delete(0,'end')
            self.entry_lamptimer.insert(0,timeStr)
            self.timerEndLampShutdown()

    def timerCountDown(self,delay,iteration=0):

        timeLeft = delay-1000*iteration

        timeStr = str(round(timeLeft/1000))
        self.entry_timer.delete(0,'end')
        self.entry_timer.insert(0,timeStr)

        if timeLeft>0:
            self.timerAfter = self.mainFrame.after(1000,self.timerCountDown,delay,iteration+1)
        else:
            timeStr = str(round(delay/1000))
            self.entry_timer.delete(0,'end')
            self.entry_timer.insert(0,timeStr)
            self.timerEndShutterClose()

    def onChopButton(self):
        try:
            if self.chopping:
                self.chopping = False
                self.mainFrame.after_cancel(self.chopAfter)
                if self.lamp.shutterOpen:
                    self.mainFrame.after(1000,self.chopEndShutterClose)
                self.enableButtons()
                logging.info('stopped chopping')

            else:
                self.chopping = True

                self.choppingOnTime = int(1000*float(self.entry_chop_on.get()))
                self.choppingOffTime = int(1000*float(self.entry_chop_off.get()))
                if self.choppingOnTime < 1000:
                    self.choppingOnTime = 1000
                    self.entry_chop_on.delete(0,'end')
                    self.entry_chop_on.insert(0,'1')

                if self.choppingOffTime < 1000:
                    self.choppingOffTime = 1000
                    self.entry_chop_off.delete(0,'end')
                    self.entry_chop_off.insert(0,'1')


                logging.info('started chopping: on time: '+str(self.choppingOnTime/1000)+' off time: '+str(self.choppingOffTime/1000))
                

                self.comm.closeShutter()
                self.mainFrame.after(self.choppingOffTime,self.chopOpen)
                self.disableButtons([self.btn_chop])  
        except:
            logging.exception('Error chopping')


    def chopOpen(self):
        tic = time.perf_counter()
        self.comm.openShutter()
        self.lamp.shutterOpen = True
        toc = time.perf_counter()

        delay = int(round(max([0, self.choppingOnTime-1000*(toc-tic)])))
        self.chopAfter = self.mainFrame.after(delay,self.chopClose)

    def chopClose(self):
        tic = time.perf_counter()
        self.comm.closeShutter()
        self.lamp.shutterOpen = False
        toc = time.perf_counter()

        delay = int(round(max([0, self.choppingOffTime-1000*(toc-tic)])))
        self.chopAfter = self.mainFrame.after(delay,self.chopOpen)


    def onPortSelect(self,*args):
        try:       
            port = self.commOption.get()
            logging.info('port '+port + ' selected')
            self.comm = serialComm.serialComm(port)
            self.lamp = self.comm.getLampState()
            self.lamp.window = self
                
            logging.info('Initial lamp state'+self.lamp.__repr__())


            if self.lamp.lampOn:
                self.btn_power.configure(bg ='green')
            else:
                self.btn_power.configure(bg ='red')

            if self.lamp.shutterOpen:
                self.btn_shutter.configure(bg ='green')
            else:
                self.btn_shutter.configure(bg ='red')
            self.entry_intensity.delete(0,'end')
            self.entry_intensity.insert(0,str(self.lamp.intensity))
            self.entry_timer.delete(0,'end')
            self.entry_timer.insert(0,str(self.lamp.timer))

            self.lbl_conn_status.configure(text = 'Connection OK\n Life '+str(self.lamp.life)+' h')
            self.enableButtons()

        except:
            self.lbl_conn_status.configure(text = 'Connection failed')
            logging.exception('Lamp connection failed')

    def onWindowClose(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.comm.closeShutter()
                self.comm.endRemote()
            except:
                logging.info('Unable to close communication')
            currentTime = time.strftime('%Y-%m-%d %H:%M',time.localtime())
            logging.info('Remote operation ended at '+currentTime)
            tkRoot.destroy()

    def handleExceptions(self,exception,value,trace):
        print(exception)
        logging.exception("Error")
        try:
            self.comm.closeShutter()
            self.comm.endRemote()
        except:
            logging.info('Unable to close communication')
        tk.messagebox.showerror('Exception',exception)
        self.master.destroy()


    def disableButtons(self,enabled):
        for widget in self.getAllChildren(self.mainFrame):
            if isinstance(widget, tk.Button) and widget not in enabled:
                widget.configure(state='disabled')


    def enableButtons(self):
        for widget in self.getAllChildren(self.mainFrame):
            if isinstance(widget, tk.Button):
                widget.configure(state='normal')


    def chopEndShutterClose(self):
        self.comm.closeShutter()
        self.lamp.shutterOpen = False

    def timerEndShutterClose(self):
        self.timerRunning = False
        self.comm.closeShutter()
        self.lamp.shutterOpen = False
        self.enableButtons()


    def timerEndLampShutdown(self):
        self.timerRunning = False
        self.comm.closeShutter()
        self.lamp.shutterOpen = False
        time.sleep(1)
        self.comm.closePower()
        self.lamp.lampOn = False

        self.enableButtons()

    def getAllChildren(self,widget,childList=[]):  
        for item in widget.winfo_children():
            childList.append(item)
            self.getAllChildren(item,childList)
        return childList


if __name__ == '__main__':
    logging.basicConfig(
        filename='AsahiLamp.log',
        level=logging.INFO,
        filemode='a')

    currentTime = time.strftime('%Y-%m-%d %H:%M',time.localtime())
    logging.info('\n\nStarted at '+currentTime)
    tkRoot = tk.Tk()

    mainWindow(tkRoot)
    tkRoot.mainloop()