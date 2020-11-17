from tkinter import Tk,Label,LabelFrame,Entry,Spinbox,Frame,Canvas,StringVar,Button,Text,Scrollbar
from convert import Number_system

# unicode reps for subscript
subscript = ["\u2080","\u2081","\u2082","\u2083","\u2084","\u2085","\u2086","\u2087","\u2088","\u2089"]

NEWLINE = "\n"

class gui (Number_system):

    """
        Graphical User Interface for number systrm calculator
        The user interface is divided into 3 secions(operand, operation, and result_board )
        certain restriction has been made on the widgets so as to reduce extra exception handling
        within the system
    """
    operation = []
    operand  = []
    result = 0

    def __init__(self, master):
        """"    User interface is built on tkinter   """
        Number_system.__init__(self)
        self.entry_value = StringVar()
        self.entry_base = StringVar() 
        self.output_base = StringVar()

        master = master
        master.title("Numerical System")
        master.minsize(width= 400, height=400)
        master.resizable(width=0, height=0)
        font = ("verdanna", 8, "bold")

        # Canvas 
        canvas = Canvas(master, bg="blue")
        canvas.pack(fill="both")


        # Frames
        top_frame = Frame(canvas,)
        top_frame.pack()

        bottom_frame = Frame(canvas, )
        bottom_frame.pack()


        # operand widget( Entry , Scrollbar )
        operand_label = LabelFrame(top_frame, text=" Operand ", font= font,bg="bisque", fg="blue", borderwidth=3,padx=5)
        operand_label.pack(side="left",fill="y")

        Label(operand_label, text="Value: ", width=8,bg="bisque", font=font ).grid(row=0, sticky="W")

        self.entry = Entry(operand_label, width=19,font= font, borderwidth=3, textvariable=self.entry_value)
        self.entry.grid(row=0, column=1)
        self.entry.focus_set()
        self.entry.bind("<KeyRelease>", self.min_base_value)

        Label(operand_label, text= " V_base: ", width=9, height=2,bg="bisque", font=font,).grid(row=1)

        value_base = Spinbox(operand_label, from_=2, to=36, width=7,state="readonly", textvariable=self.entry_base)
        value_base.grid(row=1,column=1,sticky="W")

        Label(operand_label, text= " O_base: ", width=9,bg="bisque", font=font,).grid(row=2)

        output_base = Spinbox(operand_label, from_=2, to=36, width=7,state="readonly", textvariable = self.output_base)
        output_base.grid(row=2,column=1,sticky="W")


        # Operations widget( Buttons )
        operation_label = LabelFrame(top_frame, text=" Operation ", fg="blue",bg="bisque", font = font, borderwidth=3,padx = 5,pady=4)
        operation_label.pack(side="left",fill="x")

        add_btn = Button(operation_label, text=" + ", width=8, font = font,)
        add_btn.bind("<Button-1>",self.board_operation)
        add_btn.grid(row=0)
    
        sub_btn = Button(operation_label, text=" - ", width=8, font = font,)
        sub_btn.bind("<Button-1>",self.board_operation)
        sub_btn.grid(row=0, column=1)

        mul_btn = Button(operation_label, text=" x ", width=8, font = font,)
        mul_btn.bind("<Button-1>",self.board_operation)
        mul_btn.grid(row=1, column=0)

        div_btn = Button(operation_label, text=" / ", width=8, font = font,)
        div_btn.bind("<Button-1>",self.board_operation)
        div_btn.grid(row=1, column=1)

        submit_btn = Button(operation_label, text="convert / submit", fg="green",bg="bisque", width=18,font=font)
        submit_btn.config(command=self.submit)
        submit_btn.grid(row=2, columnspan=2, sticky="W")

        clear_btn = Button(operation_label, text="clear",bg="bisque", fg="red", font=font,height=5, width=8,command= self.erase_board)
        clear_btn.grid(row=0,column=2, rowspan=3)


        # Result widget ( Text Entry )
        result_label = LabelFrame(bottom_frame, text=" Result ", fg="blue",bg="bisque", font = font, borderwidth=1,)
        result_label.pack()

        scroll = Scrollbar(result_label)
        scroll.pack(side="right",fill="y")

        self.board = Text(result_label, bg="black", fg="white", width=50,font= ("dubai", 11,), height=20, wrap='word',insertborderwidth=2)
        self.board.config(state="disable", yscrollcommand=scroll.set)
        self.board.pack(side="left")
        scroll.config(command=self.board.yview)

        master.mainloop()

    def to_equiv_base(self):
        """"
            perform necessary operation with operands in base10
            and return value in output base
        """
        base_10 = str(self.baseX_to_base10( self.entry_value.get(), self.entry_base.get() ) )
        gui.operand.append(self.baseX_to_base10(  self.entry_value.get(),self.entry_base.get() ))
        if any(gui.operand):
            gui.result = gui.operand[0]
            for index,operation in enumerate(gui.operation):
                if operation == " + ":
                    gui.result += gui.operand[index+1]
                if operation == " - ":
                    gui.result -= gui.operand[index+1]
                if operation == " x ":
                    gui.result *= gui.operand[index+1]
                if operation == " / ":
                    gui.result /= gui.operand[index+1]
                    
            return self.base10_to_baseX(gui.result, self.output_base.get()) 

        return self.base10_to_baseX(base_10, self.output_base.get()) 

    def submit(self):
        """
            Basically prints the result to the board
        """
        if data := self.entry_value.get():
            if not data.isalnum():
                return False
            self.display(data  + self.subscript(self.entry_base.get()) + " = " + self.to_equiv_base() + self.subscript(self.output_base.get()) + NEWLINE )
            # resets all the variable after every calculation
            self.entry_value.set("")
            self.entry_base.set(2)
            gui.result = 0
            gui.operand.clear()
            gui.operation.clear()

    def min_base_value(self, event):
        ''''
            configure the base of the value inputed to minimun 
            and capitalise value (if it contains alphabet)
        '''
        if  data := self.entry_value.get():
            self.entry.config(bg="red") if not data.isalnum() else self.entry.config(bg="white")
            self.entry_value.set(self.entry_value.get().upper())
            min_base = self.legal_base_36.rfind(max(self.entry_value.get()))
            self.entry_base.set(min_base+1) if min_base > 0 else self.entry_base.set(2)

    def display(self,*response):
        '''
            Manipulating the configuration of the Text widget
        '''
        self.board.config(state="normal")
        self.board.insert("end",*response)
        self.board.see("end")
        self.board.config(state="disable")

    def board_operation(self, event):
        '''
            Displays equation on the Text widget(board)
        '''
        if data := self.entry_value.get():
            if data.isalnum():
                self.display(data  + self.subscript(self.entry_base.get()) + event.widget.cget("text") )
                gui.operand.append(self.baseX_to_base10(data,self.entry_base.get()))
                gui.operation.append(event.widget.cget("text"))
                self.entry_base.set(2)
                self.entry_value.set("")

    def subscript(self, base, data=""):
        '''
            converts value_base to subscript
        '''
        sub = list(base)
        for i in sub:
            data += subscript[int(i)]
        return data

    def erase_board(self):
        """
            Delete all characters on the board
        """
        self.board.config(state="normal")
        self.board.delete(0.0,"end")
        self.board.config(state="disable")



if __name__ == '__main__':
    gui(Tk())
