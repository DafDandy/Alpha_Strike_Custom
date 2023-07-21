import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Alpha Strike Custom Card Generator')
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()