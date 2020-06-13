

####
#
# TODO: deal with keyboard and video ourput at the same time, maybe use pygame for both, would need to itergrate pygame into this
#
###




import pygame
import random
import keyboard
import time

class chip:
    keyboard = [0]*16#store a list with 16 different key states
    display_buffer = [0]*64*32# a list with 32 lists of 64 0's
    memory = [0]*4096
    gpio = [0]*16#16 8 bit registers, last one vf used only for flags

    sound_timer = 0#will decrement to zero and waste a clock_cycle every clock_cycle
    delay_timer = 0#^^^^^^
    index_register = 0#16 bit
    program_counter = 0x200#16 bit, points to the current opcode that needs processing
    stack = []#a list at add or remove stack pointers
    opcode = 0# the operation code currently used
    #instruction functions
    draw = False

    curr_key = ""

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

    key_map = {1:"1",2:"2",3:"3",0xc:"4",
                    4:"q",5:"w",6:"e",0xd:"r",
                    7:"a",8:"s",9:"d",0xe:"f",
                    0xa:"z",0:"x",0xb:"c",0xf:"v"}

    def __init__(self):
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
                            0x7000: self._7xxx,
                            0x8000: self._8xxx,
                            0x8ff0: self._8xx0,
                            0x8ff1: self._8xx1,
                            0x8ff2: self._8xx2,
                            0x8ff3: self._8xx3,
                            0x8ff4: self._8xx4,
                            0x8ff5: self._8xx5,
                            0x8ff6: self._8xx6,
                            0x8ff7: self._8xx7,
                            0x8ffe: self._8xxe,
                            0x9000: self._9xxx,
                            0xa000: self.axxx,
                            0xb000: self.bxxx,
                            0xc000: self.cxnn,
                            0xd000: self.dxyn,
                            0xe000: self.e000,
                            0xe00e: self.ex9e,
                            0xe001: self.exa1,
                            0xf000: self.fxxx,
                            0xf007: self.fx07,
                            0xf00a: self.fx0a,
                            0xf015: self.fx15,
                            0xf018: self.fx18,
                            0xf029: self.fx29,
                            0xf033: self.fx33,
                            0xf055: self.fx55,
                            0xf065: self.fx65



                            }




        self.reverse_keys = {v:k for k, v in self.key_map.items()}



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


    def clock_cycle(self, key):
        self.curr_key = key
        #self.opcode = self.memory[self.program_counter]
        self.opcode = (self.memory[self.program_counter] << 8) | self.memory[self.program_counter + 1]#makes the opcode, not my design
        #^^ gives us the decimal equivalent of the hex code for the next 2 bytes

        #here we extract nibbles from the opcode
        self.vx = (self.opcode & 0x0f00) >> 8#left inner nibble, register x
        self.vy = (self.opcode & 0x00f0) >> 4#right inner nibble, register y



        self.program_counter += 2 #move ahead 2 bytes, given that each instruction is 16 bits

        extracted_op = self.opcode & 0xf000#gives us the starter to lookup the function, first 4 bit hex number, of 16



        # try:
        self.function_map[extracted_op]() # call the associated method
        # except:
        #     print ("Unknown initial instruction: %X" % self.opcode)

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


        self.display_buffer = [0]*64*32 # 64*32


    def oxxe(self):

        self.program_counter = self.stack.pop()

    def ixxx(self):

        self.program_counter = self.opcode & 0x0fff#extract the ladt three nibbles, a 12 bit hex number, thats why it only has 4096 bytes of memoory because the maximum value that can be stored by 3 hex numbers is 4095(0 indexed)



    def _2xxx(self):#calls a subroutine, ie just fucks the stack in the ass
        self.stack.append(self.program_counter)
        self.program_counter = self.opcode & 0x0fff

    def _3xxx(self):#Skips the next instruction if VX equals NN. (Usually the next instruction is a jump to skip a code block)
        if self.gpio[self.vx] == (self.opcode & 0x00ff):
            self.program_counter += 2

    def _4xnn(self):

        if self.gpio[self.vx] != (self.opcode & 0x00ff):
            self.program_counter += 2

    def _5xy0(self):

        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.program_counter += 2


    def _6xxx(self):
        self.gpio[self.vx] = (self.opcode & 0x00ff)


    def _7xxx(self):
        self.gpio[self.vx] += (self.opcode & 0x00ff)


    def _8xxx(self):#add another level of extraction, and intersection
        extracted_op = self.opcode & 0xf00f
        extracted_op += 0x0ff0#set max value so we can lookup with last number, a very useful techniquw when you have a lot of codes starting with the same hex digit

        try:
            self.function_map[extracted_op]()
        except:
            print ("Unknown instruction: %X" % self.opcode)

    def _8xx0(self):
        self.gpio[self.vx] = self.gpio[self.vy]
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff

    def _8xx1(self):
        self.gpio[self.vx] = self.gpio[self.vx] | self.gpio[self.vy]
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff

    def _8xx2(self):
        self.gpio[self.vx] = self.gpio[self.vx] & self.gpio[self.vy]
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff

    def _8xx3(self):
        self.gpio[self.vx] = self.gpio[self.vx] ^ self.gpio[self.vy]#XOR
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff



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
        self.gpio[0xf] = self.gpio[self.vx] & 0x0001#0x0001
        self.gpio[self.vx] = self.gpio[self.vx] >> 1


    def _8xx7(self):#If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
        if self.gpio[self.vy] > self.gpio[self.vx]: self.gpio[0xf] = 0
        else: self.gpio[0xf] = 1
        self.gpio[self.vx] = self.gpio[self.vy] - self.gpio[self.vx]
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff


    def _8xxe(self):#If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
        #1, set vf to vx msb
        #2, times vx by 2
        self.gpio[0xf] = (self.gpio[self.vx] & 0x00f0) >> 7 #would nedd a & 0xff if we had more bytes put into it initially
        self.gpio[self.vx] = self.gpio[self.vx] << 1
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff

    def _9xxx(self):
        if self.gpio[self.vx] != self.gpio[self.vy]: self.program_counter += 2


    def axxx(self):
        self.index_register = self.opcode & 0x0fff

    def bxxx(self):
        self.program_counter = (self.opcode & 0x0fff) + self.gpio[0x0]

    def cxnn(self):
        self.gpio[self.vx] = random.randint(0,255) & (self.opcode & 0x00ff)
        self.gpio[self.vx] = self.gpio[self.vx] & 0xff



    def dxyn(self):#Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N pixels. Each row of 8 pixels is read as bit-coded starting from memory location I;
    # I value doesn’t change after the execution of this instruction. As described above, VF is set to 1 if any screen pixels are flipped from set to unset when the sprite is drawn, and to 0 if that doesn’t happen

    #not my method, too slow

    #--- NEED TO REDO -- #
    #--- MAKE PYTHONIC --#

        self.gpio[0xf] = 0#make register vf default
        x = self.gpio[self.vx]#make an x and y
        y = self.gpio[self.vy]

        height = self.opcode & 0x000f#number of bytes

        row = 0#used for iterating
        while row < height:#loop for each byte ie row

            current_row = self.memory[row+self.index_register]#memory location, will increse per byte by 1

            pixel_offset = 0#varuable used to calculate bit offset


            while pixel_offset < 8:
                loc = x + pixel_offset + ((y + row) * 64)#create
                pixel_offset += 1
                if (y + row) >= 32 or (x + pixel_offset - 1) >= 64:continue#if the pixel is outside the screen ignore it, NORMALLY WRAPS AROUND NEEDS CHANGING
                mask = 1 << 8-pixel_offset#create a mask for getting the bit we want later, very clever , dont have to use bin() or fuck with slow strings
                current_pixel = (current_row & mask) >> (8-pixel_offset)#the address, make a mask to get the bit we want

                self.display_buffer[loc] = self.display_buffer[loc] ^ current_pixel#xor the current pixel into the buffer, 1=0,0=1

                #VF IS SET TO 1 ONLY IS A PIXEL IS ERASED
                if self.display_buffer[loc] == 0:
                    self.gpio[0xf] = 1
                else:
                    self.gpio[0xf] = 0

            row+=1
        self.draw = True



    def e000(self):
        extracted_op = self.opcode & 0xf00f


        # try:
        self.function_map[extracted_op]() # call the associated method
        # except:
        #     print ("Unknown instruction: %X" % self.opcode)

            #keypress stuff nedds porting
    def ex9e(self):
        if self.curr_key ==  self.key_map[self.gpio[self.vx]]:
            self.program_counter += 2


    def exa1(self):#Skips the next instruction if the key stored in VX isn't pressed. (Usually the next instruction is a jump to skip a code block)
        if self.curr_key == "":self.program_counter += 2
        elif self.gpio[self.vx] != self.reverse_keys[self.curr_key]:
            self.program_counter += 2
        #else: pass


    def fxxx(self):

        extracted_op = self.opcode & 0xf0ff

        try:
            self.function_map[extracted_op]()
        except:
            print ("Unknown instruction: %X" % self.opcode)

    def fx07(self):
        self.gpio[self.vx] = self.delay_timer

    def fx0a(self):

        h = input("program blocked until a vlid key is pressed...")
        if h in self.key_map.values():

            key_list = list(self.key_map.keys())
            val_list = list(self.key_map.values())
            self.gpio[self.vx] = key_list[val_list.index(h)]


        else:
            self.program_counter -= 2


    def fx15(self):
        self.delay_timer = self.gpio[self.vx]

    def fx18(self):
        self.sound_timer = self.gpio[self.vx]

    def fx1e(self):
        # n = self.index_register + self.gpio[self.vx]
        # if n > 0xfff:
        #     self.index_register = 0xfff
        #     self.gpio[0xf] = 1
        #
        # else:
        #     self.index_register = n
        self.index += self.gpio[self.vx]
        if self.index > 0xfff:
            self.gpio[0xf] = 1
            self.index &= 0xfff
        else:
            self.gpio[0xf] = 0

    def fx29(self):#Sets I to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented by a 4x5 font.

        self.index_register = (5*(self.gpio[self.vx])) & 0xfff##########################################################################################################################################################################changed to make run not to fix , needs attention
       #self.index_register = 5*(self.gpio[self.vx])

        self.draw = True


    def fx33(self):# take the decimal representation of VX, place the hundreds digit in memory at location in I, the tens digit at location I+1, and the ones digit at location I+2.
        self.memory[self.index_register]   = int(self.gpio[self.vx] / 100)
        self.memory[self.index_register+1] = int((self.gpio[self.vx] % 100) / 10)
        self.memory[self.index_register+2] = int(self.gpio[self.vx] % 10)
        print(self.gpio[self.vx])
        print(self.gpio[self.vx] / 100,(self.gpio[self.vx] % 100) / 10,self.gpio[self.vx] % 10)
        print(int(self.gpio[self.vx] / 100),int((self.gpio[self.vx] % 100) / 10),int(self.gpio[self.vx] % 10))

    def fx55(self):
        # for j in range(16):
        #     self.memory[self.index_register+j] = self.gpio[j]
        i = 0
        while i <= self.vx:
            self.memory[self.index_register + i] = self.gpio[i]
            i += 1
        self.index_register += (self.vx) + 1


    def fx65(self):#Fills V0 to VX (including VX) with values from memory starting at address I. The offset from I is increased by 1 for each value written, but I itself is left unmodified.[d]
        # for j in range(16):
        #     self.gpio[j] = int(self.memory[self.index_register+j])
        i = 0
        while i <= self.vx:
            self.gpio[i] = self.memory[self.index_register + i]
            i += 1
        self.index_register += (self.vx) + 1
