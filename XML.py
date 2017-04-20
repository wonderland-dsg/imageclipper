#coding=utf-8
from xml.dom.minidom import Document

class XML:
    def __init__(self):
        None

    def __creat_node(self,name,text):
        node=self.doc.createElement(name)
        node_text=self.doc.createTextNode(text)
        node.appendChild(node_text)
        return node

    def creat_tree(self,folder,image_name,msize):
        self.image_name=image_name
        self.doc=Document()
        self.annotation=self.doc.createElement('annotation')
        #annotation.setAttribute('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")#设置命名空间
        #annotation.setAttribute('xsi:noNamespaceSchemaLocation','bookstore.xsd')#引用本地XML Schema
        self.doc.appendChild(self.annotation)

        folder=self.__creat_node('folder',folder)
        self.annotation.appendChild(folder)

        filename=self.__creat_node('filename',image_name)
        self.annotation.appendChild(filename)

        size=self.doc.createElement('size')

        size_width=self.__creat_node('width',str(msize[1]))
        size.appendChild(size_width)
        size_height=self.__creat_node('height',str(msize[0]))
        size.appendChild(size_height)
        size_depth=self.__creat_node('depth',str(msize[2]))
        size.appendChild(size_depth)

        self.annotation.appendChild(size)

    def insert_object(self,name,bndbox):
        object=self.doc.createElement('object')
        object_name=self.__creat_node('name',name)
        object_bndbox=self.doc.createElement('bndbox')
        object_bndbox_xmin=self.__creat_node('xmin',str(bndbox[0]))
        object_bndbox_ymin=self.__creat_node('ymin',str(bndbox[1]))
        object_bndbox_xmax=self.__creat_node('xmax',str(bndbox[2]))
        object_bndbox_ymax=self.__creat_node('ymax',str(bndbox[3]))
        object_bndbox.appendChild(object_bndbox_xmin)
        object_bndbox.appendChild(object_bndbox_ymin)
        object_bndbox.appendChild(object_bndbox_xmax)
        object_bndbox.appendChild(object_bndbox_ymax)
        object.appendChild(object_name)
        object.appendChild(object_bndbox)
        self.annotation.appendChild(object)

    def close(self,folder):
        f = open(folder+self.image_name+'.xml','w')
        f.write(self.doc.toprettyxml(indent = ''))
        f.close()

if __name__=='__main__':

    xml=XML()
    xml.creat_tree("test","test",[1,1,1])
    xml.insert_object("dog",[1,1,1,1])
    xml.insert_object("dog",[1,1,1,1])
    xml.insert_object("dog",[1,1,1,1])
    xml.insert_object("dog",[1,1,1,1])
    xml.insert_object("dog",[1,1,1,1])
    xml.close("test")