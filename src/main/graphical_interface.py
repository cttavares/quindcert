import wx

import datetime
import logging



import sys
import os
import threading
import time
import wx.lib.agw.pybusyinfo as PBI

from photonic_indistinguishability_measures.variance import InterfaceHelperDevice
from quandela.circuit_helpers import generate_identity, generate_random_circuit
from tomography.process_tomography_quandela import characterize_device
from tomography.estimating_overlaps import find_overlaps, random_preparation


import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.figure import Figure
from matplotlib.pyplot import text



from main.matrix_control import MatrixControl
from fractions import Fraction

class Data:
    def __init__ (self):
        self.number_of_modes = 4 
        self.user_key = ""
        self.qpu_device = "Naive"

        print ("Identity: ", generate_identity (self.number_of_modes).compute_unitary ())

        self.original_matrix = generate_identity (self.number_of_modes).compute_unitary()
        self.rebuilt_matrix = generate_identity (self.number_of_modes).compute_unitary()
        
        self.trace = 1
        self.gram_matrix = generate_identity (self.number_of_modes).compute_unitary()
        
        # For the moment let's keep
        # 
        #processor = Device.create_local_processor ('Naive')
        #self.qpu_device = "sim:ascella"
        #self.user_key = "_T_eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTc4LCJleHAiOjE3MTcyNTM1NDR9.pltdoPfsKfGcFqQl0kJ3N3o6qGdDqnvGDmYNauldWbOEvVFBXpYGTv_Ot-iuh-54QIeFua-CB_DNFtmWQOKpHQ"

class WorkerThread(threading.Thread):
    def __init__(self, data, frame, parent):
        super(WorkerThread, self).__init__()
        self.parent = parent
        self.data = data
        self.frame = frame
        
    def run(self):
        # 
        (original, matrix, trace) = characterize_device(self.data.number_of_modes, self.data.qpu_device, self.data.user_key) # After work is done, destroy the PyBusyInfo dialog
        
        self.data.original_matrix = original
        self.data.rebuilt_matrix = matrix
        self.data.trace = trace

        self.frame.update ()


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Optical device characterization', size = (400,300))
        
        self.data = Data()
        self.panel = wx.Panel(self)
        
        # Create a notebook (tabbed interface)
        notebook = wx.Notebook(self.panel)

        # Create the first tab
        self.tab1 = self.create_tab1_(notebook)
    
        # Create the first tab
        self.create_tab_2(notebook)
        
        self.create_tab3(notebook)
         # Add the notebook to the panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        
        self.Maximize ()
        self.Center ()
        self.Show(True)
        self.hide_components (self.quandela_configuration_sizer, self.quandela_configuration)


    def round_to_fraction (self, number):
        f = Fraction (number)
        return f.limit_denominator (10)

    def on_click_button_page_2_make_experiments (self, event):
        checked = self.checkbox_list.GetCheckedItems ()
        device = InterfaceHelperDevice (self.data.number_of_modes, self.data.qpu_device, self.data.user_key)

        if 0 in checked:
            fb_ind = device.do_the_experiments_for_full_bunching_indistinguishable_case (self.data.number_of_modes)
            fb_dis = device.do_the_experiments_for_full_buncing_distinguishable_case (self.data.number_of_modes)
            
            index = self.prob_full_bunching_distinguishable.LabelText.find (":")
            self.prob_full_bunching_distinguishable.LabelText = self.prob_full_bunching_distinguishable.LabelText [:index] + ": " + str (fb_dis) + "(" + str (self.round_to_fraction (fb_dis)) + ")" 
            
            index = self.prob_full_bunching_normal.LabelText.find(":") 
            self.prob_full_bunching_normal.LabelText = self.prob_full_bunching_normal.LabelText [:index] + ": " + str (fb_ind) + "(" + str (self.round_to_fraction (fb_ind)) + ")"
        
        if 1 in checked:
            var = device.do_the_experiments_for_variance_indistinguishable_case (self.data.number_of_modes)
            index_1 = self.expected_variance.LabelText.find (":") 
            self.expected_variance.LabelText = self.expected_variance.LabelText [:index_1] + ": " + str (var) + "(" + str (self.round_to_fraction (var)) + ")"

            var_d = device.do_the_experiments_for_variance_distinguishable_case (self.data.number_of_modes)
            average_bound = device.calculate_bound_average_n_modes (var, var_d, self.data.number_of_modes)
            index_2 = self.sigma_average.LabelText.find (">")
            self.sigma_average.LabelText = self.sigma_average.LabelText [:index_2] + " >= " + str (average_bound) + "("+ str (self.round_to_fraction (average_bound)) +")"

            if self.data.number_of_modes == 3:
                min_average_bound = device.calculate_minimum_three_modes (var)
                index_3 = self.sigma_min.LabelText.find (":")
                self.sigma_min.LabelText = self.sigma_min.LabelText [:index_3] + ":" + str (min_average_bound) + "("+ str (self.round_to_fraction (min_average_bound)) +")"
        
            self.render_function (self.canvas_panel, self.fill_points_to_show (var, var_d))


    def create_tab_2(self, notebook):
        tab2 = wx.Panel(notebook)
        notebook.AddPage(tab2, "Gram matrix estimation (expected variance)")
        
        vbox = wx.BoxSizer (wx.VERTICAL)
        
        experiments_box = wx.StaticBox (tab2, label = "Experiments")
        experiments_box_sizer = wx.StaticBoxSizer(experiments_box, wx.HORIZONTAL)
        items = ["Probability of Full Bunching", "Expected Variance"]
        self.checkbox_list = wx.CheckListBox(tab2, choices=items)
        my_btn = wx.Button(tab2, label='Make experiments', pos=(5, 55))
        my_btn.Bind (wx.EVT_BUTTON, self.on_click_button_page_2_make_experiments)
        
        experiments_box_sizer.Add (self.checkbox_list,0, wx.ALL, 5)
        experiments_box_sizer.Add (my_btn, 0, wx.ALL, 5)

        vbox.Add (experiments_box_sizer) 


        hbox = wx.BoxSizer(wx.HORIZONTAL)

        expected_variance_box = wx.StaticBox (tab2, label = "Expected Variance")
        expected_variance_box_sizer = wx.StaticBoxSizer(expected_variance_box, wx.VERTICAL)
        
        self.sigma_min = wx.StaticText (tab2, label = "\Sigma_min")
        self.sigma_average = wx.StaticText (tab2, label = "\Sigma_average")
        self.expected_variance = wx.StaticText (tab2, label = "Expected Variance (sigma)")
        
        expected_variance_box_sizer.Add (self.expected_variance, 0, wx.ALL, 5)

        self.canvas_panel = wx.Panel (tab2)
        expected_variance_box_sizer.Add (self.canvas_panel, 1, wx.EXPAND| wx.ALL, 5)
        
        expected_variance_box_sizer.Add (self.sigma_min, 0, wx.ALL, 5)
        expected_variance_box_sizer.Add (self.sigma_average, 0, wx.ALL, 5)
            
        full_bunching_box = wx.StaticBox (tab2, label = "Full Bunching")
        full_bunching_box_sizer = wx.StaticBoxSizer (full_bunching_box, wx.VERTICAL)

        self.prob_full_bunching_normal = wx.StaticText (tab2, label = "Probability of Full Bunching:")
        self.prob_full_bunching_distinguishable = wx.StaticText (tab2, label = "Probability of Full Bunching (distinguishable scenario):")

        full_bunching_box_sizer.Add (self.prob_full_bunching_normal, 0, wx.ALL, 5)
        full_bunching_box_sizer.Add (self.prob_full_bunching_distinguishable, 0, wx.ALL, 5)

        hbox.Add (expected_variance_box_sizer)
        hbox.Add (full_bunching_box_sizer)
        
        vbox.Add (hbox)
        tab2.SetSizer(vbox)

        # Set up the matplotlib figure and canvas
        self.render_function(self.canvas_panel)

    def fill_points_to_show (self, var, var_dis):
        device = InterfaceHelperDevice (self.data.number_of_modes, self.data.qpu_device, self.data.user_key)

        points_x = []
        points_x.append (device.calculate_max_expected_variance (self.data.number_of_modes))
        points_x.append (device.calculate_min_expected_variance (self.data.number_of_modes))

        points_x.append (var_dis)
        points_x.append (var)

        points_y = []
        for _ in range (4):
            points_y.append (3)
        
        return (points_x, points_y)

    def render_function(self, canvas_panel, points_pair = ()):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        
        if len (points_pair) == 2:
            print ("Points pairs: ", points_pair)
            (points_x, points_y) = points_pair 
            self.axes.plot (points_x, points_y)
        
        self.canvas = FigureCanvas(canvas_panel, -1, self.figure)
        self.canvas.draw ()
    
    def on_button_click(self, event):
        
        busy = PBI.PyBusyInfo("Task in progress...", parent=self)
        worker_thread = WorkerThread(self.data, self, busy)
        worker_thread.start()
    
    def on_dropbox1_select(self, event):
        selected_item = self.dropdown.GetItems () [self.dropdown.GetSelection()]
        print ("Event activated!", selected_item) 
        
        # If a specific item is selected, create and display the second dropbox
        if selected_item == "Quandela v2":
            self.show_components (self.quandela_configuration_sizer, self.quandela_configuration)
        else:
            self.hide_components (self.quandela_configuration_sizer, self.quandela_configuration)
        
    def on_dropbox2_select(self, event):
        selected_index = self.dropbox2.GetSelection()
        if selected_index == 0:
            self.data.qpu_device = "Naive"
        elif selected_index == 1:
            self.data.qpu_device = "sim:ascella"
        elif selected_index == 2:
            self.data.qpu_device = "qpu:ascella"

        print ("Changed to: ", self.data.qpu_device)

    def on_dropbox3_select(self, event):
        selected_index = self.dropdown3.GetSelection()
        self.data.number_of_modes = selected_index

    def on_text_changed (self, event):
        self.data.user_key = self.quandela_text_input.GetValue()
        print ("Text changed to: ", self.data.user_key)

    def hide_components (self, sizer, box):
    
        for item in sizer.GetChildren ():
            window = item.GetWindow ()
            window.Hide ()
        
        box.Hide()
        
    def show_components (self, sizer, box):
        for item in sizer.GetChildren ():
            item.GetWindow ().Show ()
        box.Show ()

    def build_quandela_config(self, tab):
        self.quandela_configuration = wx.StaticBox (tab, label = "Quandela configuration")
        self.quandela_configuration_sizer = wx.StaticBoxSizer (self.quandela_configuration, wx.HORIZONTAL)
            
        additional_choices = ["Naive", "(Cloud simulator) sim:ascella", "(Actual QPU) qpu:ascella"]
        self.dropbox2 = wx.Choice (tab, choices=additional_choices)
        self.quandela_configuration_sizer.Add (self.dropbox2, 0, wx.EXPAND|wx.ALL, 5)
        self.dropbox2.Bind(wx.EVT_CHOICE, self.on_dropbox2_select)

        key_label = wx.StaticText(tab, label="Key:")
        self.quandela_configuration_sizer.Add (key_label, 0, wx.EXPAND|wx.ALL, 5)

        self.quandela_text_input = wx.TextCtrl (tab)
        self.quandela_text_input.Bind (wx.EVT_TEXT, self.on_text_changed)
        self.quandela_configuration_sizer.Add (self.quandela_text_input, 0, wx.EXPAND|wx.ALL, 5)
        self.hbox_configuration.Add (self.quandela_configuration_sizer, wx.EXPAND|wx.ALL, 5)
        
    def create_tab1_(self, notebook):
        tab1 = wx.Panel(notebook)
        notebook.AddPage(tab1, "Device characterization")
        
        vbox = wx.BoxSizer (wx.VERTICAL)
        self.hbox_configuration = wx.BoxSizer (wx.HORIZONTAL)
        
        device_configuration = wx.StaticBox (tab1, label = "Device confguration")
        self.device_configuration_sizer = wx.StaticBoxSizer (device_configuration, wx.HORIZONTAL)
        
        device_label = wx.StaticText(tab1, label="Device type: ")
        self.device_configuration_sizer.Add (device_label,  0, wx.EXPAND|wx.ALL, 5)
        choices = ['Quandela v2', 'Penny Lane', 'Custom']
        self.dropdown = wx.Choice(tab1, choices=choices)
        self.dropdown.Bind(wx.EVT_CHOICE, self.on_dropbox1_select)
        self.device_configuration_sizer.Add (self.dropdown,  0, wx.EXPAND|wx.ALL, 5) 
        
        modes_label = wx.StaticText(tab1, label="Number of modes")
        self.device_configuration_sizer.Add (modes_label,  0, wx.EXPAND|wx.ALL, 5)
        modes = [str (i) for i in range (0, 8)]
        self.dropdown3 = wx.Choice(tab1, choices=modes)
        self.dropdown3.Bind(wx.EVT_CHOICE, self.on_dropbox3_select)
        self.device_configuration_sizer.Add (self.dropdown3,  0, wx.EXPAND|wx.ALL, 5)

        self.hbox_configuration.Add (self.device_configuration_sizer) 
        
        self.build_quandela_config(tab1)
        self.hbox_configuration.Add (self.quandela_configuration_sizer)
        
        
        vbox.Add (self.hbox_configuration)
        
        device_characterization = wx.StaticBox (tab1, label = "Device characterization")
        device_characterization_sizer = wx.StaticBoxSizer (device_characterization, wx.VERTICAL)
        device_characterization_button = wx.Button(tab1, label='Characterize device', pos=(5, 55))
        device_characterization_button.Bind (wx.EVT_BUTTON, self.on_button_click)
        device_characterization_sizer.Add (device_characterization_button)

        vbox.Add (device_characterization_sizer)

        hbox_matrices = wx.BoxSizer (wx.HORIZONTAL)

        show_original_matrix_box = wx.StaticBox (tab1, label = "Original matrix")
        show_original_matrix_sizer = wx.StaticBoxSizer (show_original_matrix_box, wx.HORIZONTAL)
        
        edit_input_matrix_button = wx.Button(tab1, label='Edit input matrix', pos=(5, 55))
        
        self.canvas_original = self.render_matrix (tab1, self.data.original_matrix)
       
        show_original_matrix_sizer.Add (edit_input_matrix_button,0, wx.ALL, 5)
        show_original_matrix_sizer.Add (self.canvas_original, 1, wx.EXPAND|wx.ALL, 10)
        
        show_obtained_matrix_box = wx.StaticBox (tab1, label = "Matrix obtained")
        show_obtained_matrix_sizer = wx.StaticBoxSizer (show_obtained_matrix_box, wx.HORIZONTAL)
        
        self.canvas_obtained = self.render_matrix(tab1, self.data.rebuilt_matrix)
        show_obtained_matrix_sizer.Add (self.canvas_obtained, 1, wx.EXPAND|wx.ALL, 10)

        hbox_matrices.Add (show_original_matrix_sizer)
        hbox_matrices.Add (show_obtained_matrix_sizer)
        
        vbox.Add (hbox_matrices)
        
        trace_box = wx.StaticBox (tab1, label = "Trace box")
        trace_box_sizer = wx.StaticBoxSizer (trace_box, wx.HORIZONTAL)
        
        self.canvas_trace = self.render_text(tab1, self.data.trace)
        
        trace_box_sizer.Add (self.canvas_trace)
        vbox.Add (trace_box_sizer)
        
        tab1.SetSizer(vbox)
        return tab1
    

    def render_text(self, tab1, text):
        trace_figure = Figure(figsize=(4, 3))
        ax = trace_figure.add_subplot(111)
        ax.axis ('off')
        # Render LaTeX expression
        ax.text(0.5, 0.5, text, fontsize=20, ha='center')
        canvas_trace = FigureCanvas (tab1, -1, trace_figure)
        return canvas_trace

    def matrix_to_latex(self, matrix):
        num_rows = len(matrix)
        num_cols = len(matrix[0])
    
        latex_code = r'\[\begin{bmatrix}'
    
        for i in range(num_rows):
            for j in range(num_cols):
                if j != 0:
                    latex_code += ' & '
                latex_code += str(matrix[i][j])
            latex_code += r' \\'
    
        latex_code += r'\end{bmatrix}\]'
    
        return latex_code    
    
    def render_matrix_(self, panel, matrix):
        fig_obtained = Figure(figsize=(4, 3))
        ax = fig_obtained.add_subplot(111)
        
        # Enable LaTeX rendering in Matplotlib
        ax.axis ('off')
        ax.text(0.5, 0.5, self.matrix_to_latex (matrix), fontsize=20, ha='center', va='center')
      
        canvas_obtained = FigureCanvas (panel, -1, fig_obtained)
        return canvas_obtained

    def render_matrix (self, panel, matrix):
        return MatrixControl (panel, matrix)

    def create_tab3(self, notebook):
        tab3 = wx.Panel(notebook)
        notebook.AddPage(tab3, "Calculate Gram matrix")
        
        gram_matrix_box = wx.StaticBox (tab3, label = "Gram matrix")
        
        gram_matrix_box_sizer = wx.StaticBoxSizer (gram_matrix_box, wx.HORIZONTAL)
        generate_gram_matrix_button = wx.Button(tab3, label='Generate', pos=(5, 55))
        generate_gram_matrix_button.Bind (wx.EVT_BUTTON, self.on_button_generate_gram_matrix)
        gram_matrix_box_sizer.Add (generate_gram_matrix_button)

        self.canvas_gram_matrix = self.render_matrix (tab3, self.data.gram_matrix)
        gram_matrix_box_sizer.Add (self.canvas_gram_matrix)

        tab3.SetSizer(gram_matrix_box_sizer)

    def make_experiments_expected_variance (self, circuit):
        device = InterfaceHelperDevice (self.data.number_of_modes, self.data.qpu_device, self.data.user_key)
        return device.do_the_experiments_for_the_variance (self.data.number_of_modes, self.data.qpu_device, self.data.user_key, circuit)
    
    def on_button_generate_gram_matrix (self, event):
        number_of_preparations = ((self.data.number_of_modes * self.data.number_of_modes) - self.data.number_of_modes)//2  
        print ("Number of necessary preparations: ", number_of_preparations)

        matrices = []
        for i in range (number_of_preparations):
            matrices.append (generate_random_circuit (self.data.number_of_modes))
        
        characterized_matrices = []
        for i in matrices:
            characterized_matrices.append (characterize_device (self.data.number_of_modes, self.data.qpu_device, self.data.user_key, i) [1])

        expected_variances_pairs = []
        for j in characterized_matrices:
            expected_variances_pairs.append ((j, self.make_experiments_expected_variance (j)))

        X = find_overlaps (expected_variances_pairs, number_of_preparations)
        self.data.gram_matrix = X
        self.update ()


    def update (self):
        print ("Gram matrix to update: ", self.data.gram_matrix)
        self.canvas_gram_matrix.update_matrix (self.data.gram_matrix)
        
        print ("Rebuilt matrix to update: ", self.data.rebuilt_matrix)
        self.canvas_obtained.update_matrix (self.data.rebuilt_matrix)
        
        print ("Original matrix to update: ", self.data.original_matrix)
        self.canvas_original.update_matrix (self.data.original_matrix)
        

if __name__ == '__main__':
    if not os.path.exists('.\logs'):
        os.makedirs('.\logs')

    dateTag = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M-%S")
    logging.basicConfig(filename=".\\logs\\running_%s.log" % dateTag, encoding='utf-8', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
    
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()