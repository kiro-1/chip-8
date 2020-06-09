#import pygame


class chip:
    keyboard = [0]*16#store a list with 16 different key states
    display_buffer = [[0]*64]*32# a list with 32 lists of 64 0's
    memory = [0]*4096
    gpio = [0]*16#16 8 bit registers, last one vf used only for flags
    sound_timer = 0#will decrement to zero and waste a clock_cycle every clock_cycle
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

    def __init__(self,width,height):
        for i in range(80): self.memory[i] = self.fonts[i]#load in the fonts from 0x0 to 0x50
        self.function_map = {0x0000: self.oxxx,
                            0x00e0: self.oxxo,
                            0x00ee: self.oxxe,
                            0x1000: self.ixxx,
                            0x2000: self._2xxx,
                            0x3000: self._3xxx,
                            0x4000: self._4xnn,
                            0x5000: self._5xy0,
                            0x6000: self._6xxx,
                            0x8000: self._8xxx,
                            0x8ff0: self._8xx0,
                            0x8ff1: self._8xx1,
                            0x8ff2: self._8xx2,
                            0x8ff3: self._8xx3,

                            0x8ff4: self._8xx4,
                            0x8ff5: self._8xx5,

                            }
        # pygame.init()#should probably make this class inherit from the pygame class
        # screen = pygame.display.set_mode((width, height))
        # pygame.display.set_caption("CHIP-8 Emulator by Bailey Padovan")
        #
        # pygame.display.set_icon(pygame.image.load('icon.png'))


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


    def clock_cycle(self):
        #self.opcode = self.memory[self.program_counter]
        self.opcode = (self.memory[self.program_counter] << 8) | self.memory[self.program_counter + 1]#makes the opcode, not my design
        #^^ gives us the decimal equivalent of the hex code for the next 2 bytes

        #here we extract nibbles from the opcode
        self.vx = (self.opcode & 0x0f00) >> 8#left inner nibble, register x
        self.vy = (self.opcode & 0x00f0) >> 4#right inner nibble, register y
        print(self.opcode,self.vx,self.vy)


        self.program_counter += 2 #move ahead 2 bytes, given that each instruction is 16 bits

        extracted_op = self.opcode & 0xf000#gives us the starter to lookup the function, first 4 bit hex number, of 16
        print(extracted_op)


        try:
            self.function_map[extracted_op]() # call the associated method
        except:
            print ("Unknown initial instruction: %X" % self.opcode)

        #timer stuff
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
        #     if self.sound_timer == 0:
        #   Play a sound here with pygame

    def oxxx(self):

        extracted_op = self.opcode & 0xf0ff#look at the first alnd last 2, second will always be 0

        try:
            self.function_map[extracted_op]()
        except:
            print ("Unknown instruction: %X" % self.opcode)


    def oxxo(self):


        self.display_buffer = [[0]*64]*32 # 64*32


    def oxxe(self):

        self.program_counter = self.stack.pop()

    def ixxx(self):

        self.program_counter = self.opcode & 0x0fff#extract the ladt three nibbles, a 12 bit hex number, thats why it only has 4096 bytes of memoory because the maximum value that can be stored by 3 hex numbers is 4095(0 indexed)



    def _2xxx(self):#calls a subroutine, ie just fucks the stack in the ass
        self.stack.append(self.program_counter)
        self.program_counter = self.opcode & 0x0fff

    def _3xxx(self):#Skips the next instruction if VX equals NN. (Usually the next instruction is a jump to skip a code block)
        if self.gpio[self.vx] == self.opcode & 0x00ff:
            self.program_counter += 2

    def _4xnn(self):

        if self.gpio[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2

    def _5xy0(self):

        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc += 2


    def _6xxx(self):
        self.gpio[self.vx] == self.opcode & 0x00ff


    def _7xxx(self):
        eslf.gpio[self.vx] += self.opcode & 0x00ff


    def _8xxx(self):#add another level of extraction, and intersection
        extracted_op = self.opcode & 0xf00f
        extracted_op = extracted_op & 0x0ff0#set max value so we can lookup with last number, a very useful techniquw when you have a lot of codes starting with the same hex digit

        try:
            self.function_map[extracted_op]()
        except:
            print ("Unknown instruction: %X" % self.opcode)

    def _8xx0(self):
        self.gpio[self.vx] = self.gpio[self.vy]

    def _8xx1(self):
        self.gpio[self.vx] = self.gpio[self.vx] | self.gpio[self.vy]

    def _8xx2(self):
        self.gpio[self.vx] = self.gpio[self.vx] & self.gpio[self.vy]

    def _8xx3(self):
        self.gpio[self.vx] = self.gpio[self.vx] ^ self.gpio[self.vy]#XOR


    def _8xx4(self):#PROBLEM COMPUTES TOO MANY OPERATIONS FOR 1:1 EFFICENCY, bad for nes or snes @>1mhz

        #set the carry flag
        if self.gpio[self.vx] + self.gpio[self.vy] > 0xff:#there is probably a more legible way of doing this
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] = 0
        #add the register Vy into Vx
        self.gpio[self.vx] += self.gpio[self.vy]
        #keep the lowest 8 bits, ie wrap back to 0 if it exceeds 255
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff#should just be self.gpio[self.vx] = 0xff

    def _8xx5(self):

        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xf] = 0
        else:
            self.gpio[0xf] = 1
        self.gpio[self.vx] = self.gpio[self.vx] - self.gpio[self.vy]
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff

#lsb = the bit with the least value in the current byte, ie 000000>1<. haha lsd

    def _8xx6(self):#Stores the least significant bit of VX in VF and then shifts VX to the right by 1.[b]



















    #drawing
    def _fx29(self):#Sets I to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented by a 4x5 font.
        index_register = self.vx * 5






c = chip(640,320)

c.load_program("demo.ch8")
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()
print()
c.clock_cycle()

c.print_memory()
print(c.display_buffer)
