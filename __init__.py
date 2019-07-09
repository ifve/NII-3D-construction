import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import tkinter as Tk
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib import cbook  

import os
import numpy as np
import nibabel as nib
from nibabel.testing import data_path
import vtki

import nibabel as nib
import numpy as np
import vtk
import vtkplotter
from vtkplotter import *
import PySimpleGUI as sg

import re
import string 



def img2D(points):
    #三角形片面重建模型 
    sg.Popup('渲染正在进行中，请您耐心等候一段时间~~~',button_color=('white','blue'),background_color='white',keep_on_top=True)
    gif(gifpath2)
    
    cloud = vtki.PolyData(points)
#     bcloud = vtki.PolyData(blist)
#     roicloud = vtki.PolyData(roilist)
    surf = cloud.delaunay_2d(tol = 1e-08,alpha = 1,offset = 100.0,bound = False,inplace =False ) 
#     surf1 = bcloud.delaunay_2d(tol = 1e-08,alpha = 0.3,offset = 100.0,bound = False,inplace =False )
#     surf2 = roicloud.delaunay_2d(tol = 1e-08,alpha = 0.1,offset = 100.0,bound = False,inplace =False )
    print(type(surf))
    plotter = vtki.BackgroundPlotter()
    plotter.add_mesh(surf)
#     plotter.add_mesh(surf1)
#     plotter.add_mesh(surf2)
    plotter.show()

#     surf.plot(salar = np.arange(100),show_edges=True) 
#     surf1.plot(surf2,salar = np.arange(100))
#     surf2.plot(surf1,salar = np.arange(100))
    
#     class MainWindow(Qt.QMainWindow):

#         def __init__(self, parent=None, show=True):
#             Qt.QMainWindow.__init__(self, parent)

#             # create the frame
#             self.frame = Qt.QFrame()
#             vlayout = Qt.QVBoxLayout()

#             # add the pyvista interactor object
#             self.vtk_widget =vtki.QtInteractor(self.frame)
#             vlayout.addWidget(self.vtk_widget)

#             self.frame.setLayout(vlayout)
#             self.setCentralWidget(self.frame)

#             # simple menu to demo functions
#             mainMenu = self.menuBar()
#             fileMenu = mainMenu.addMenu('File')
#             exitButton = Qt.QAction('Exit', self)
#             exitButton.setShortcut('Ctrl+Q')
#             exitButton.triggered.connect(self.close)
#             fileMenu.addAction(exitButton)

#             # allow adding a sphere
#             meshMenu = mainMenu.addMenu('重建显示')
#             self.add_p_action = Qt.QAction('显示激活区对象', self)
#             self.add_p_action.triggered.connect(self.add_p)
#             meshMenu.addAction(self.add_p_action)

#             self.add_roi_action = Qt.QAction('显示目标区域对象', self)
#             self.add_roi_action.triggered.connect(self.add_roi)
#             meshMenu.addAction(self.add_roi_action)

#             self.add_brain_action = Qt.QAction('显示脑模板对象', self)
#             self.add_brain_action.triggered.connect(self.add_brain)
#             meshMenu.addAction(self.add_brain_action)

#             if show:

#                 self.show()

#         def add_p(self):
#             """ add to the pyqt frame """

#             self.vtk_widget.add_mesh(surf)
#             #self.vtk_widget.reset_camera()

#         def add_roi(self):
#             """ add to the pyqt frame """

#             self.vtk_widget.add_mesh(surf2)
#             #self.vtk_widget.reset_camera()

#         def add_brain(self):
#             """ add to the pyqt frame """

#             self.vtk_widget.add_mesh(surf1)
#             #self.vtk_widget.reset_camera()


#     if __name__ == '__main__':
#         app = Qt.QApplication(sys.argv)
#         window = MainWindow()
#         sys.exit(app.exec_())
    
    

    
    

def imgpro(points,roilist,blist):
    rx = roilist[:,0]
    ry = roilist[:,1]
    rz = roilist[:,2]
    
    brx = blist[:,0]
    bry = blist[:,1]
    brz = blist[:,2]
    #去除模板外的激活点区域
    bmaxx = np.amax(brx)
    bmaxy = np.amax(bry)
    bmaxz = np.amax(brz)
    bminx = np.amin(brx)
    bminy = np.amin(bry)
    bminz = np.amin(brz)


    roimaxx = np.amax(rx)
    roimaxy = np.amax(rx)
    roimaxz = np.amax(rx)
    roiminx = np.amin(rx)
    roiminy = np.amin(ry)
    roiminz = np.amin(rz)

    sg.Print('bmax',bmaxx,bmaxy,bmaxz,'min',bminx,bminz,bminz)
    sg.Print('roimax',roimaxx,roimaxy,roimaxz,'roimin',roiminx,roiminz,roiminz)
    sg.Print('删除前的激活区维度：',points.shape)
    flag = 1
    if flag ==1:
        for i in range(points.shape[0]):
            if points[i,0]>bmaxx or points[i,0]<bminx or points[i,1]>bmaxy or points[i,1]<bminy or points[i,2]>bmaxz or points[i,2]<bminz:
                print('删除的点：',points[i])
                np.delete(points,points[i],0)
        sg.Print('删除后的激活区维度：background',points.shape)
    if flag == 2:
        for i in range(points.shape[0]):
            if points[i,0]>roimaxx or points[i,0]<roiminx or points[i,1]>roibmaxy or points[i,1]<roibminy or points[i,2]>roimaxz or points[i,2]<roiminz:
                print('删除的点：',points[i])
                np.delete(points,points[i],0)
        sg.Print('删除后的激活区维度：roi',points.shape)
        sg.Popup('激活区数据已筛选完毕~~~',button_color=('white','blue'),background_color='white',keep_on_top=True)
    
    return points

def dataprocess(file,roi,model):
   
    example_file = os.path.join(file)
    #载入示例图片
    img = nib.load(example_file)
    #img1 = img.slicer[0,:,:]

    img2 = img.get_fdata()
    #img1 = np.flatnonzero(img2.astype(np.float16))#得到数组中非0 值的索引

    #sg.Print(img2.ravel()[img1])
    #原数据切片显示
    # import matplotlib.pyplot as plt
    # for i in range(img2.shape[2]):
    #     print("i:",i)
    #     plt.figure(i)
    #     print(img2[:,:,i])
    #     plt.imshow(img2[:,:,i])
    #     plt.show()
    #img2 = img2.astype(np.float32)

    x = []
    y = []
    z = []
    v = []
    counts = np.array([0,0,0])
    #sg.Print("counts",type(counts))
    for xi in range(img2.shape[0]):
           for yi in range(img2.shape[1]):
                for zi in range(img2.shape[2]):
                    #print('img2:',img2[yi,xi,zi])
                    counts = np.add(counts.reshape(1,3), np.array([xi,yi,zi]).reshape(1,3))
                    if(img2[xi,yi,zi]>0):
                        x.append(xi)
                        y.append(yi)
                        z.append(zi)
                        v.append(img2[xi,yi,zi])
                        #print('counts',counts.shape,'[xi,yi,zi]:shaep:',np.array([xi,yi,zi]).shape)

    #sg.Print(np.array([xi,yi,zi]),'counts:',counts)



    #grid = vtki.StructuredGrid()

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    v = np.array(v)
    v = v**3*50
    
    # for i in range(v.shape[0]):
    #     print(i,v[i])
    counts = counts/x.shape[0]
    #点云重现
   
    points = np.c_[x, y, z]
    sg.Print('激活区的数据维度：',points.shape)
    # simply pass the numpy points to the PolyData constructor


    b = nib.load(model)#脑部区域显示
    bimg = b.get_fdata()
    #print (roimg)
    # roimg = roimg.astype(np.uint8)
    sg.Print('脑模板区域的数据维度：',bimg.shape)
    #roimg = list(roimg)
    brx = []
    bry = []
    brz = []
    brv = []
    countb = np.array([0,0,0])
    cnt = 0
    for i in range(bimg.shape[0]):
        for j in range(bimg.shape[1]):
            for k in range(bimg.shape[2]):
                countb = np.add(countb , np.array([i,j,k]))
                cnt += 1
                if bimg[i][j][k]>0.7 :
    #                 print('counts:',counts)
                    brx .append(i)
                    bry.append(j)
                    brz.append(k)
                    brv.append(bimg[i][j][k])

    brx = np.array(brx)
    bry = np.array(bry)
    brz = np.array(brz)
    brv = np.array(brv)
    sg.Print('删选后脑模板的维度：',brx.shape,bry.shape,brz.shape)
    blist = np.c_[brx.reshape(-1),brz.reshape(-1),bry.reshape(-1)]
    countb = countb/brx.shape[0]

    rois = nib.load(roi)#目标区域显示
    roimg = rois.get_fdata()
    #print (roimg)
    # roimg = roimg.astype(np.uint8)
    sg.Print('目标区域的数据维度：',roimg.shape)
    #roimg = list(roimg)
    rx = []
    ry = []
    rz = []
    rv = []
    countroi =np.array([0,0,0])
    for i in range(roimg.shape[0]):
        for j in range(roimg.shape[1]):
            for k in range(roimg.shape[2]):
                countroi = np.add(countroi , np.array([i,j,k]))
                if roimg[i][j][k]>0.7:
    #                 print('counts:',counts)
                    rx .append(i)
                    ry.append(j)
                    rz.append(k)
                    rv.append(roimg[i][j][k]) 

    rx = np.array(rx)
    ry = np.array(ry)
    rz = np.array(rz)
    rv = np.array(rv)

    roilist = np.c_[rx.reshape(-1),rz.reshape(-1),ry.reshape(-1)]
    countroi = countroi/rx.shape[0]
    #计算模板和目标区域的中心坐标
    sg.Print('中心坐标：',counts,countb,countroi)

    #模板与目标区域的空间大小标准化匹配
    posk = np.array(img2.shape)
    bk = np.array(bimg.shape)
    roik = np.array(roimg.shape)

    alpha1 = bk/posk
    alpha2 = bk/roik
    sg.Print('激活区与脑模板的比例测算：''alpha1:',alpha1,'alpha2:',alpha2)

    bks = np.array([bimg.shape[0]/2,bimg.shape[1]/2-15,bimg.shape[2]/2])
    posks = np.array([img2.shape[0]/2,img2.shape[1]/2,img2.shape[2]/2])
    roiks = np.array([roimg.shape[0]/2,roimg.shape[1]/2-15,roimg.shape[2]/2])


    #点云数据与模板匹配
    for i in range(points.shape[0]):
        points[i] = points[i]*alpha1- posks + bks
    for i in range(roilist.shape[0]):
        roilist[i] = roilist[i]*alpha2 #- roiks + bks
    #print('return value.shape:',points.shape ,roilist.shape,blist.shape)
    return points ,roilist,blist,img2,roimg,bimg
        
# dataprocess(model,roi,file)

#界面动画


#三维重建

def construction3d(points,blist,roilist,mm,shape3D,color3D,flag):
    sg.Popup('3D重建过程正在进行中，请您耐心等候一段时间~~~',button_color=('white','blue'),background_color='white',keep_on_top=True)
    gif(gifpath2)
    #颜色值转换格式
    

    def toRgb(tmp):
        opt = re.findall(r'(.{2})',tmp) #将字符串两两分割
        v = []#用以存放最后结果
        for i in range (0, len(opt)):#for循环，遍历分割后的字符串列表
            v.append(int(opt[i], 16)) #将结果拼接成12，12，12格式
        print("转换后的RGB数值为：")
        v = tuple(v)
        print(type(v),v)#输出最后结果，末尾的","不打印
        return v  
    color3D[0] = toRgb(color3D[0])
    color3D[1] = toRgb(color3D[1])
    color3D[2] = toRgb(color3D[2])
        
    
    
    #polydata数据类型转换
    cloud = vtki.PolyData(points)
    bcloud = vtki.PolyData(blist)
    roicloud = vtki.PolyData(roilist)
    #print(rx.shape,ry.shape,rz.shape)
    # colors.getColor([10,100])

    #制作绘图对象
    plotter = Plotter()
    sg.Print('绘图纸准备完毕')
    roivtk = vtkplotter.Actor(roicloud,c =color3D[1])
    bvtk = vtkplotter.Actor(bcloud,c=color3D[2])
    posvtk = vtkplotter.Actor(cloud,c=color3D[0])
    #posvtk.addPointScalars(v,name='value')
    sg.Print('对象转换完毕')


    sg.Print('VTK对象加载完毕')

    #制作点状标记区域
    # for i in range(len(points)):
    #     sp = shapes.Cube(points[i],c=v[i])
    #     plotter.add(sp)
    sp = shapes.Points(points,c=color3D[0])
    bp = shapes.Points(blist,c=color3D[2])
    roip = shapes.Points(roilist,c=color3D[1])

    sg.Print('激活区对象加载完毕')
    sg.Popup('3D重建过程已完成大半部分，不要着急马上就好啦~~~',button_color=('white','blue'),background_color='white',keep_on_top=True)

    #添加截面
    planez = shapes.Plane(pos=tuple(mm), normal=(0,0,1), sx=100, sy=100, c=(50,125,255),alpha=1, texture=None)   
    planey = shapes.Plane(pos=tuple(mm), normal=(0,1,0), sx=100, sy=100, c=(100,255,100), alpha=1, texture=None)    
    planex = shapes.Plane(pos=tuple(mm), normal=(1,0,0), sx=100, sy=100, c=(255,125,50), alpha=1, texture=None)    


    
    sg.Print('截面加载完毕')

    #点云重建过程
    mp = analysis.recoSurface(points, bins=256)
    mroi = analysis.recoSurface(roilist, bins=256)




    #绘图显示
    if shape3D[2] == 0:
        plotter.add(bvtk)#点云对象添加
    if shape3D[1] == 0:
        plotter.add(roivtk)
    if shape3D[0] == 0:
        plotter.add(posvtk)
    if shape3D[0] == 1:
        plotter.add(sp)#点云点模型对象添加
    if shape3D[2] == 1:
        plotter.add(bp)
    if shape3D[1] == 1:
        plotter.add(roip)
    if shape3D[1] == 2:
        plotter.add(mroi)#点云重建对象添加
    if shape3D[0] == 2:
        plotter.add(mp)
    if flag == 1:
        plotter.add(planez)#截面标识对象添加
        plotter.add(planey)
        plotter.add(planex)
    #添加插件
    def slider1(widget, event):
        value = widget.GetRepresentation().GetValue()
        sp.alpha(value)
        posvtk.alpha(value)
        mp.alpha(value)


    def slider2(widget, event):
        value = widget.GetRepresentation().GetValue()
        bp.alpha(value)
        bvtk.alpha(value)
        

    def slider3(widget, event):
        value = widget.GetRepresentation().GetValue()
        mroi.alpha(value)    
        roivtk.alpha(value)
        roip.alpha(value)

    Np = sp.N()
    scals = np.linspace(0, 1, Np)  # coloring by index nr of vertex

    #sp.addPointScalars(scals, "mypointscalars")  # add a vtkArray to actor


    addonc = 'white'

    def buttonfunc():
        bp.alpha(1 - bp.alpha())  # toggle mesh transparency
        bu.switch()                 # change to next status
        printc(bu.status(), box="_", dim=True)


    bu = plotter.addButton(buttonfunc,pos=(350, 20),states=["press to hide", "press to show"],c=["w", "w"],bc=["dg", "dv"],font="courier",size=18,bold=True,italic=False)
    plotter.addSlider2D(slider1, 0,1, value=5, pos=12, c=addonc,title="激活区显示颜色")
    plotter.addSlider2D(slider2, 0,1, value=1, pos=13, c=addonc,title="目标区域的透明度")
    plotter.addSlider2D(slider3, xmin=0, xmax=1, value=0.5, pos=14, c=addonc, title="脑部模板区域的透明度")
    sg.Popup('模型已经渲染完毕，点击确定即可显示结果~~~',button_color=('white','blue'),background_color='white',keep_on_top=True)
    plotter.show()




#截面GUI


def drawplane(posplane,img2,roimg,bimg,alpha):
    sg.Popup('截面渲染正在进行中，请您耐心等候一段时间~~~',button_color=('white','blue'),background_color='white',keep_on_top=True)
    gif(gifpath2)
    def draw_figure(canvas, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas
        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
        canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        return photo

    #--------------------------------三视图代码 -----------------------------------------
    img2c = np.pad(img2,((6,6),(7,7),(6,6)),'minimum')#与模板大小匹配
    pimg = []
    for i in range(img2c.shape[0]):
        for j in  range(img2c.shape[1]):
            for k in range(img2c.shape[2]):
                if img2c[i,j,k]==img2c[i,j,k]:
                    pimg.append(np.float64(img2c[i,j,k])+1)
                else:
                    pimg.append(0)

    pimg = np.array(pimg)
    for i in range(pimg.shape[0]):
        pimg[i] = np.array(pimg[i])
    pimg = pimg.reshape(roimg.shape)


    def addlight(plotter,img,cmap,a,j):
        ls = LightSource(azdeg=1000, altdeg=60)
        rgb = ls.shade(img_rotate, cmap= cmap, vert_exag=1, blend_mode='overlay')
        plotter.imshow(rgb,alpha =a[j] )
        plotter.set_axis_off()
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                        wspace=0.35)


    def datachoose(pimg,bimg,roimg,i):#选择背景数据或者激活区数据或者目标区数据
        if i == 0:
            data = pimg
            return data
        elif i == 1:
            data = bimg
            return data
        elif i == 2:
            data = roimg
            return data



    
    #原图像生成截面图

    ax = plt.figure(figsize=(5,5))
    mm = posplane
    a =alpha

    #截面显示
    mm = np.array(mm)
    mm  =  mm.astype(np.uint32)
    for i in range(1,len(mm)+1):#三种视图
        if i == 1:
            sg.Print('正在绘制俯视图')
            plots = plt.subplot(2,2,i)
            for j in range(3):
                img = datachoose(bimg,roimg,pimg,j)
                sg.Print('是截面的问题吗？',mm[i-1])
                sg.Print("选中的截面数据为：",img[:,:,int(mm[i-1])])
                if np.any(img[:,:,mm[i-1]]) == True:
                    img_rotate = img[:,:,mm[i-1]]
                    addlight(plots,img_rotate,plt.cm.copper,a,j)
                elif i==1 and j ==0 :
                    sg.Popup('该截面没有激活点,截面位置为侧截面%d处'%mm[i-1])             
        if i == 2:
            sg.Print('正在绘制侧视图')
            plots = plt.subplot(2,2,i)
            for j in range(3):
                img = datachoose(bimg,roimg,pimg,j)
                sg.Print("选中的截面数据为：",img[int(mm[i-1]),:,:])
                if np.any(img[mm[i-1],:,:]) == True:
                    img_rotate = np.fliplr(img[mm[i-1],:,:])
                    addlight(plots,img_rotate,plt.cm.copper,a,j)
                elif i==1 and j ==0 :
                    sg.Popup('该截面没有激活点，截面位置为侧截面%d处'%mm[i-1])  
        if i == 3 :
            sg.Print('正在绘制正视图')
            plots = plt.subplot(2,2,i)
            for j in range(3):
                img = datachoose(bimg,roimg,pimg,j)
                sg.Print("选中的截面数据为：",img[:,int(mm[i-1]),:])
                if np.any(img[:,mm[i-1],:]) == True:
                    img_rotate = np.fliplr(img[:,mm[i-1],:])
                    addlight(plots,img_rotate,plt.cm.copper,a,j)
                elif i==1 and j ==0 :
                    sg.Popup('该截面没有激活点，截面位置为侧截面%d处'%mm[i-1])
    figure_x, figure_y, figure_w, figure_h = ax.bbox.bounds                                
    #ax.show() 

    #------------------------------- Beginning of GUI CODE -------------------------------

    # define the window layout
    layout = [[sg.Text('截面图显示', font='Any 18',auto_size_text=25)],
              [sg.Canvas(size=(figure_w, figure_h), key='canvas')],
#               [sg.Slider(range=(1,99), default_value=0.1, size=(20,15), orientation='horizontal', font=('Helvetica', 12),key='_a1_')],
#               [sg.Slider(range=(1,99), default_value=0.3, size=(20,15), orientation='horizontal', font=('Helvetica', 12),key='_a2_')],
#               [sg.Slider(range=(1,99), default_value=0.8, size=(20,15), orientation='horizontal', font=('Helvetica', 12),key='_a3_')],
              [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]

    # create the form and show it without the plot
    planewindow = sg.Window('#########截面显示>>>>>>>>>>>>', force_toplevel=True).Layout(layout).Finalize()
    # window.Element('canvas').Update(values['_a1_'])
    # a[1] = values['_a1_']/100
    # add the plot to the window
    sg.Popup('截面渲染已经完成，点击确定即可显示~~~',button_color=('white','blue'),background_color='white',keep_on_top=True)
    fig_photo = draw_figure(planewindow.FindElement('canvas').TKCanvas, ax)

    # show it all again and get buttons
    
    
    event, values = planewindow.Read()

    #window.Element('canvas').Update(values['input'])
    if event == None or event == 'OK':
        planewindow.Close()
        

def gif(gifpath2):
    for i in range(400000):   
        sg.PopupAnimated(gifpath2, background_color='white', time_between_frames=100,message='数据处理时间准备过程时间较长，请您耐心等待一段时间。。。')
    sg.PopupAnimated(None)
    
    
file = 'C://Users//ifve//Desktop//DICOM//newdata//pa1//data//6//mat/figner.nii'
model = 'D:/download/package/spm12/spm12/canonical/avg152PD.nii'
roi = 'D:/download/package/spm12/spm12/canonical/avg152T2.nii'    
alpha = [0.1,0.4,0.8]#三个对象透明度设置
planepos = [45,50,50]#三个截面位置  
shape3D = [0,0,0]
color3D = ['00ff00','ff0000','0000ff']
# color3D = np.array(color3D)
gifpath2 =  'C://Users//ifve//Desktop//3dcon//img/loadgif2.gif'

    


#gif(gifpath2)
#points ,roilist,blist,img2,roimg,bimg = dataprocess(file,roi,model)
#img2D(points,blist,roilist)
#imgpro(points,roilist,blist)
#construction3d(points,blist,roilist,planepos,shape3D,color3D,1)
#drawplane(posplane,imgp,imgroi,imgb,alpha)