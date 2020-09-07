from font import Font

class dispMatrix(object):
    def __init__(self,matrix=1,rotation=0):
        self.matrix_width = 8
        self.matrix_height = 8
        self.matrix_count = matrix
        self.message_string = ''
        self.message_matrix_buffer =[[],[],[],[],[],[],[],[]]
        self.display_matrix = []
        self.rotation = rotation
        self.fnt = Font()
        self.gen_matrix()
        self.frame_index = 0
        self.frame_count = 0
        self.generate_message(' ')
        #self.dip_matrix_default = [range(0,8),range(15,7,-1),range(16,24),range(31,23,-1),range(32,40),range(47,39,-1),range(48,56),range(63,55,-1)

    def _gen_matrix(self,initial_width_count=0):
        temp_display_matrix=[]
        width_counter=initial_width_count * 64
        direction = 1
        for _ in range(0,self.matrix_height):
            if direction == 1:
                jj = list(range(width_counter,self.matrix_width+width_counter,direction))
                temp_display_matrix.append(jj)
                width_counter = width_counter + self.matrix_width
                direction = -1
            else:
                jj = list(range(self.matrix_width+width_counter-1,width_counter-1,direction))
                temp_display_matrix.append(jj)
                width_counter = width_counter + self.matrix_width
                direction = 1

        return temp_display_matrix

    def gen_matrix(self):
        #self.matrix_count = mat_len
        self.display_matrix = [[],[],[],[],[],[],[],[]]
        for ct in range(0,self.matrix_count):
            mat = self._gen_matrix(ct)
            self.display_matrix[0].extend(mat[0])
            self.display_matrix[1].extend(mat[1])
            self.display_matrix[2].extend(mat[2])
            self.display_matrix[3].extend(mat[3])
            self.display_matrix[4].extend(mat[4])
            self.display_matrix[5].extend(mat[5])
            self.display_matrix[6].extend(mat[6])
            self.display_matrix[7].extend(mat[7])


    def binr(self,number):
        res = "{0:08b}".format(int(number, 16)) 
        res = res.replace('0',' ').replace('1','@')
        data = [ x for x in res]
        #data = [ int(x) for x in res]
        return(self.matrix_reverse(data))


    def matrix_reverse(self,mat):
        new_mat = []
        for x in range(7,-1,-1):
            new_mat.append(mat[x])
        return new_mat

    def character_render_8(self,char_d):
        arr_d = []
        d = ord(char_d)
        for x in self.fnt.font8[d]:
            dr = self.binr(x)
            arr_d.append(dr)
        return arr_d

    def character_render_6(self,char_d):
        arr_d = []
        d = ord(char_d)
        for x in self.fnt.font6[d]:
            dr = self.binr(x)
            arr_d.append(dr)
        arr_tmp=[[],[],[],[],[],[],[],[]]
        for x in range(0,6):
            arr_tmp[0].append(arr_d[x][0])
            arr_tmp[1].append(arr_d[x][1])
            arr_tmp[2].append(arr_d[x][2])
            arr_tmp[3].append(arr_d[x][3])
            arr_tmp[4].append(arr_d[x][4])
            arr_tmp[5].append(arr_d[x][5])
            arr_tmp[6].append(arr_d[x][6])
            arr_tmp[7].append(arr_d[x][7])
        return arr_tmp
        
        return arr_d

    def generate_message(self,message,size=6):
        self.message_string = " " * self.matrix_count + message + "  " * self.matrix_count
        self.message_matrix_buffer = [[],[],[],[],[],[],[],[]]
        for x in self.message_string:
            if size == 6:
                data = self.character_render_6(x)
            else:
                data = self.character_render_8(x)
            self.message_matrix_buffer[0].extend(data[0])
            self.message_matrix_buffer[1].extend(data[1])
            self.message_matrix_buffer[2].extend(data[2])
            self.message_matrix_buffer[3].extend(data[3])
            self.message_matrix_buffer[4].extend(data[4])
            self.message_matrix_buffer[5].extend(data[5])
            try:
                self.message_matrix_buffer[6].extend(data[6])
                self.message_matrix_buffer[7].extend(data[7])
            except:
                self.message_matrix_buffer[6].extend([0,0,0,0,0,0,0,0])
                self.message_matrix_buffer[7].extend([0,0,0,0,0,0,0,0])

        self.frame_count = len(self.message_matrix_buffer[0])

    def matrix_rotate(self,data = [],rotation = 0):
        matrix = [[],[],[],[],[],[],[],[]]
        if rotation == 0:
            return data
        elif rotation == 2:
            for x in data:
                t = 0
                for y in self.matrix_reverse(x):
                    matrix[t].append(y)
                    t = t + 1
            return matrix
        
        elif rotation == 1:
            for x in self.matrix_reverse(data):
                t = 0
                for y in x:
                    matrix[t].append(y)
                    t = t + 1
            return matrix

        elif rotation == 3:
            for x in self.matrix_reverse(data):
                t = 0
                for y in self.matrix_reverse(x):
                    matrix[t].append(y)
                    t = t + 1
            return matrix

    def matrix_to_pixels(self,data):
        pixels=[]
        for x in range(0,self.matrix_width * self.matrix_count):
            for y in range(0,self.matrix_height):
                if data[x][y] == "@" or data[x][y] == "1" or data[x][y] == 1:
                    pixels.append(self.display_matrix[x][y])
        return pixels


    def frame(self,frame_id = -1):
        if frame_id == -1:
            self.frame_index = self.frame_index + 1
        else:
            self.frame_index = frame_id

        if self.frame_index > self.frame_count - (self.matrix_width * self.matrix_count) - 1:
            self.frame_index = 0
        #print(self.message_matrix_buffer[0][self.frame_index:self.frame_index+8])
        data_frame = [
            self.message_matrix_buffer[0][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)],
            self.message_matrix_buffer[1][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)],
            self.message_matrix_buffer[2][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)],
            self.message_matrix_buffer[3][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)],
            self.message_matrix_buffer[4][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)],
            self.message_matrix_buffer[5][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)],
            self.message_matrix_buffer[6][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)],
            self.message_matrix_buffer[7][self.frame_index:self.frame_index+(self.matrix_width * self.matrix_count)] ]

        obtained_matrix = self.matrix_rotate( data_frame, self.rotation)
        return self.matrix_to_pixels(obtained_matrix)
        

