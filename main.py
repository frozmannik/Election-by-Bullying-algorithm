from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image


class MyApp(App):
    def build(self):
        self.buttons = {}
        self.logo = Image(source = 'pic.jpg', allow_stretch = True, keep_ratio = False)
        b1 = BoxLayout(orientation='vertical')
        b1.add_widget(self.logo)

        b2 = BoxLayout(orientation='horizontal', size_hint = (.9, .1))
        b2.add_widget(Label(text = "Node id:"))
        self.id = TextInput(multiline=False)
        b2.add_widget(self.id)
        b2.add_widget(Button(text = "Add node", on_press = self.add_node))

        self.g1 = GridLayout(cols = 3, padding = [30], spacing = 3, size_hint = (1, 1) ) # padding is space between corners
                                                                                        # spacing is space betwenn buttons
        b1.add_widget(b2)
        b1.add_widget(self.g1)
        return b1

    def add_node(self, btn):
        if (self.id.text).isdigit(): # check input should be int
            if int(self.id.text) in self.buttons.keys(): #check if value not in list
                print("item already exist")
            else:
                self.buttons[int(self.id.text)] = [Button(text = "Node id : "+self.id.text + "\n Leader is :",
                                              font_size = 30,
                                              on_press = self.btn_disable,
                                              background_color = [0, 1, 0, 1],  # background_color [r,g,b,a]
                                              background_normal = '',
                                              size_hint = (.5, .25),  # size of button according to windows size
                                              pos = (0,0)), 'enable' ]

                self.g1.add_widget(self.buttons[int(self.id.text)][0])
                print(self.buttons[int(self.id.text)])
                self.election()

    def btn_disable(self, instance): # change state
        if instance.text[-8:] == "disabled": # if node is disabled
            id = instance.text[6:instance.text.index('di')] # id of node
            instance.text = "Node id : "+str(id) + "\n Leader is :"
            instance.background_color = [0, 1, 0, 1]
            self.buttons[int(id)][1] = 'enable'
        else: # node enable
            if instance.text[:6] == 'Leader': # if node is a Leader
                id = int(instance.text[19:])
            else:
                id = int(instance.text[9:instance.text.index('\n')])
            self.buttons[int(id)][1] = 'disable'
            instance.text = "Node: " + str(id) + " disabled"
            instance.background_color = [1,0,0,1]
        self.election()

    def election(self):  # should runs when any changes apear( runs election )
        sorted = []
        for key in self.buttons.keys():
            sorted.append(key)
        sorted.sort()

        for k in reversed(sorted):
            if self.buttons[k][1] == 'enable':  # from highest id we search back nodes with 'enable' status
                print("Found acceptable leader {} {}".format(k, self.buttons[k][1]))
                for node in self.buttons:
                    if self.buttons[node][1] == 'enable':
                        self.buttons[node][0].text = "Node id : {} \n Leader is : {}".format(node,k)
                        self.buttons[node][0].background_color = [0,1,0,1]
                self.buttons[k][0].text = "Leader \n Node id : {}".format(k)
                self.buttons[k][0].background_color = [1,1,0,1]
                break
        else:
            print("leader is not suitable")


if __name__ == "__main__":
    MyApp().run()
