### 圓心定位
```
#均勻度
%matplotlib notebook
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib import gridspec
from scipy import ndimage
from skimage import measure
import skimage



img = mpimg.imread('HiGary_OriginImage.png')       # float32
pp= skimage.img_as_float(img)                      # 轉 float64 ,(720, 1280, 4) ;  signal range:0~1
#pp= skimage.img_as_ubyte(pp)                      # 轉u8-bit int ;   signal range: 0~255

# 分兩個，0~255的為計算用
img1= (pp)
img1= img1*255
lum_img = img1[:,:,0]  

# 0~1 的為 找邊界用
img2= ((pp)*5.5/3)**22
img2= ndimage.gaussian_filter(img2,10)
img2[0:200,:,:]=0             
img2[520:720,:,:]=0           
lum_img2 = img2[:,:,0]      

#plt.imshow(lum_img,'gray')

#  sobel 參數設定
mod= 'mirror'               
sx = ndimage.sobel(lum_img2, axis=0, mode=mod)
sy = ndimage.sobel(lum_img2, axis=1, mode=mod)
sob = np.hypot(sx, sy)
plt.figure(figsize=(8,6))
plt.imshow(sob,cmap='gray')
plt.show()

# find countour
contours = measure.find_contours(sob, 100)  
x_axis_data=[]
y_axis_data=[]

# 將找到輪廓的x,y座標存起來，裡面的每個array代表該輪廓的所有位置，x表示x所有位置，y表示y所有位置
for n, contour in enumerate(contours):    
    plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
    x_axis_data= x_axis_data+ [contour[:, 1]]
    y_axis_data= y_axis_data+ [contour[:, 0]]

# 設定輪廓大小，假定x輪廓位置總數>500 才列入要找的輪廓,也才接近正圓，因為目前專案圓周大小約2*3.14*60 
x_wanted =[]    
for i in range(len(x_axis_data)):
    if len(x_axis_data[i])>500 and len(x_axis_data[i])<1000:
        x_wanted= x_wanted+[x_axis_data[i]]

y_wanted =[]
for i in range(len(y_axis_data)):
    if len(y_axis_data[i])>500 and len(x_axis_data[i])<1000:
        y_wanted= y_wanted+[y_axis_data[i]]


# 將找到的正圓輪廓找到圓心
x_center=[]
for i,label in enumerate(x_wanted):
    tempx= np.mean(x_wanted[i])
    x_center= x_center +[tempx]

y_center=[]
for i,label in enumerate(y_wanted):
    tempy= np.mean(y_wanted[i])
    y_center= y_center +[tempy]
xc,yc=[],[]
xj,xi=[],[]
# 因為找到的正圓輪廓可能大於三個，所以圓心也大於三個，於是要篩選：  
if len(x_center)>3:

    for i in range(len(x_center)-1):
        for j in range(-i+len(x_center)):
                # 如果圓心的x距離相差<50 且抽取的兩個樣本不同：
                if abs(x_center[j+i]-x_center[i])<50 and x_center[j+i]!=x_center[i]:
                    xcc= (x_center[j+i]+x_center[i])/2
                    xj= xj+[x_center[j+i]]
                    xj=sorted(xj)
                    xi= xi+[x_center[i]]
                    xi=sorted(xi)
                    xc= xc+[xcc]
                    xc=sorted(xc)
     # 依照x找到的位置去找對應的y的位置

    for i in range(len(xj)):
        ycc=(y_center[x_center.index(xj[i])]+y_center[x_center.index(xi[i])])/2
        yc= yc+[ycc]

#畫圓心
    plt.figure(figsize=(8,6))
    plt.imshow(img)
    for gg in range(len(xj)):
        plt.scatter(xc[gg],yc[gg],marker= '*',c='r',s= 20)  
# 若沒到三個輪廓 或剛好，依樣顯示出來，不過有可能會沒定位到，可以先看圖再修正 曝光參數或輪廓邊界參數
else:
    xc= x_center
    xc= sorted(xc)
    for i in range(len(xc)):
        ycc=y_center[x_center.index(x_center[i])]
        yc= yc+[ycc]
        yc=sorted(yc)
    plt.figure(figsize=(8,6))
    plt.imshow(img)
    for gg in range(len(x_center)):
        plt.scatter(x_center[gg],y_center[gg],marker= '*',c='r',s= 20)   




# 計算均勻度           
x, y = np.meshgrid(np.arange(0, 1280, 1), np.arange(0, 720, 1))
contor_all=[]
for ij in range(len(xc)):
    contor = np.sqrt((x-xc[ij]) ** 2 + (y-yc[ij] )** 2)
    for j in range(720):
            for i in range(1280): 
                    if contor[j][i]<30 :
                            contor[j][i] =1.0
                    else:
                            contor[j][i]=0.0
    contor_all= contor_all+[contor]      

A= ((lum_img*contor_all[0]).sum())/(contor_all[0].sum())   
B= ((lum_img*contor_all[1]).sum())/(contor_all[1].sum())
C= ((lum_img*contor_all[2]).sum())/(contor_all[2].sum())
if C>B:
    ratio1= A/B
    ratio2= A/C
    ratio3= B/C
else:
    ratio1= A/B
    ratio2= A/C
    ratio3= C/B

# 畫掃描圖
fig = plt.figure(figsize=(8, 6)) 
gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1.5]) # 因為圖片比例 與 畫圖 比例不對 必須重新設定比例
#plt.subplot(211)
plt.subplot(gs[0])
plt.imshow(lum_img,cmap='jet')
plt.plot( np.linspace(0,(img.shape[1])-10,num=(img.shape[1])-10,dtype=int) ,
         [360]*(img.shape[1]-10),lw=1,c='r')

upper = [360 + 30]*(img.shape[1]-10)
lower = [360 - 30]*(img.shape[1]-10)
plt.fill_between(np.linspace(0,(img.shape[1])-10,num=(img.shape[1])-10,dtype=int) , 
                 lower, upper, color='#888888', alpha=0.4)

#plt.subplot(212)
plt.subplot(gs[1])

ybox=[]
for cc in range(lum_img.shape[1]-10):
    box= np.mean(lum_img[360-30:360+30,cc]) #算平均
    ybox=ybox+[box]
plt.plot(np.linspace(0,(img.shape[1])-10,num=(img.shape[1])-10,dtype=int) ,
        ybox,lw=2 ,c='g',alpha=0.1)  # image 是三維矩陣查看方式:  image[直,橫,rgb]
plt.grid()
plt.fill_between(np.linspace(0,(img.shape[1])-10,num=(img.shape[1])-10,dtype=int) ,
        ybox,lw=2 ,color='g',alpha=0.2)
plt.show()


print 'HDL/TG:{}'.format(ratio1),'  HDL/TC:{}'.format(ratio2),'  TG/TC:{}'.format(ratio3)
```




![GitHub Logo](https://github.com/ekils/Uniformity_algorithm/blob/master/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7%202017-04-04%20%E4%B8%8A%E5%8D%8811.03.06.png)<br>

![GitHub Logo](https://github.com/ekils/Uniformity_algorithm/blob/master/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7%202017-04-04%20%E4%B8%8A%E5%8D%8811.03.18.png)<br>

![GitHub Logo](https://github.com/ekils/Uniformity_algorithm/blob/master/%E8%9E%A2%E5%B9%95%E5%BF%AB%E7%85%A7%202017-04-04%20%E4%B8%8A%E5%8D%8811.03.28.png)<br>


