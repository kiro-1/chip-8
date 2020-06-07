
class chip:
    keyboard = [0]*16#store a list with 16 different key states
    display_buffer = [0]*64*32
    memory = [0]*4096
    gpio = [0]*16#16 8 but registers, last one vf used only for flags
    sound_timer = 0#will decrement to zero and waste a cycle every cycle
    delay_timer = 0#^^^^^^
    index_register = 0#16 bit
    program_counter = 0x200#16 bit, points to the current opcode that needs processing
    stack = []#a list at add or remove stack pointers
    opcode = 0# the operation code currently used
    #instruction functions

    vx = 0
    vy = 0

    fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0,#0
       0x20, 0x60, 0x20, 0x20, 0x70, # 1
       0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
       0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
       0x90, 0x90, 0xF0, 0x10, 0x10, # 4
       0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
       0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
       0xF0, 0x10, 0x20, 0x40, 0x40, # 7
       0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
       0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
       0xF0, 0x90, 0xF0, 0x90, 0x90, # A
       0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
       0xF0, 0x80, 0x80, 0x80, 0xF0, # C
       0xE0, 0x90, 0x90, 0x90, 0xE0, # D
       0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
       0xF0, 0x80, 0xF0, 0x80, 0x80  # F
       ]

    def __init__(self):
        for i in range(80): self.memory[i] = self.fonts[i]#load in the fonts from 0x0 to 0x50
        self.function_map = {0x0000: self.oxxx,
                            0x00e0: self.oxxo,
                            0x00ee: self.oxxe,}


    def load_program(self, path):
        b = open(path, "rb").read()
        for i in range(len(b)):
            self.memory[i+0x200] = b[i]#load it in after the 512 byte



    def print_memory(self):
        nm = []
        for i in self.memory: nm.append(hex(i).replace("0x",""))
        x = 0
        for i in range(len(nm)):
            if len(nm[i])==1:print("0"+nm[i]+" ",end='')
            else: print(nm[i]+" ",end="")
            x+=1
            if x ==32: x=0;print()


    def cycle(self):
        #self.opcode = self.memory[self.program_counter]
        self.opcode = (self.memory[self.program_counter] << 8) | self.memory[self.program_counter + 1]#makes the opcode, not my design
        #^^ gives us the decimal equivalent of the hex code for the next 2 bytes

        #here we extract nibbles from the opcode
        self.vx = (self.opcode & 0x0f00) >> 8#left inner nibble
        self.vy = (self.opcode & 0x00f0) >> 4#right inner nibble
        print(self.opcode,self.vx,self.vy)


        self.program_counter += 2 #move ahead 2 bytes, given that each instruction is 16 bits

        extracted_op = self.opcode & 0xf000#gives us the starter to lookup the function
        try:
            self.funcmap[extracted_op]() # call the associated method
        except:
            print ("Unknown instruction: %X" % self.opcode)

        #timer stuff
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
        #     if self.sound_timer == 0:
        #   Play a sound here with pyglet!

    def oxxx(self):
        """does another extraction if the starting hex is 00"""
        extracted_op = self.opcode & 0xf0ff#look at the second hexidecimal number(n.2 of 4)

        try:
            self.function_map[extracted_op]()
        except:
            print ("Unknown instruction: %X" % self.opcode)

    def oxxo(self):
        """Clears the screen"""
        self.display_buffer = [0]*64*32 # 64*32


    def oxxe(self):
        """Returns from subroutine"""
        self.program_counter = self.stack.pop()


c = chip()

c.load_program("IBMLogo.ch8")
c.cycle()
c.cycle()
c.cycle()
c.cycle()
c.cycle()
c.cycle()
c.print_memory()
