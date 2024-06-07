import wx
import wx.grid as gridlib

class MatrixControl(wx.Panel):
    def __init__(self, parent, matrix):
        super(MatrixControl, self).__init__(parent)
        self.matrix = matrix
        
        self.grid = gridlib.Grid(self)
        self.grid.CreateGrid(len(self.matrix), len(self.matrix [0]))
        
        # Hide row and column labels
        self.grid.SetRowLabelSize(0)
        self.grid.SetColLabelSize(0)

        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                self.grid.SetCellValue(i, j, str(value))
        
        self.grid.AutoSizeColumns()
        self.grid.AutoSizeRows()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(sizer)

    def update_matrix (self, matrix):
        self.matrix = matrix

        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                self.grid.SetCellValue(i, j, str(value))