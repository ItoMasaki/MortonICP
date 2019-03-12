from sample_func import *

from numpy import array
from numpy import argmin, power, sqrt, append
from numpy import int32, int64

import tkinter

class ICP():
    def __init__(self):

        # 線形探索 : (最小)
        self.MinArray       = array([])

        # 描画コンストラクタ
        self.lx, self.ly = 4, 4
        self.root = tkinter.Tk()
        self.root.geometry("{0}x{1}".format(self.lx, self.ly))
        self.Canvas = tkinter.Canvas(self.root, bg="black", width=self.lx, height=self.ly)
        self.Canvas.pack()


    # モートン関連
    def BitSeparate(self, n: int64):
        #######################
        #
        # 1bitごとに分割します.
        # ex. 011 -> 00|01|01
        #
        # 計算量 O(1)
        #
        ########################

        n = (n | n << 8) & 0x00ff00ff
        n = (n | n << 4) & 0x0f0f0f0f
        n = (n | n << 2) & 0x33333333
        return (n | n << 1) & 0x55555555

    def XY2Morton(self, x: int64, y: int64):
        #######################################################
        #
        # 2次元座標系を1次元座標系へと変換します.
        # ex. Xはビットセパレートを行います.
        #     X : 00|01|01
        #     Yはビットセパレート後に1ビット左シフトを行います.
        #     Y : 01|00|01 -> 10|00|10
        # これにOR演算を行うことで
        #     XY: 10|01|11
        #
        # 計算量 O(1)
        #
        ########################################################

        return self.BitSeparate(x)|self.BitSeparate(y)<<1

    def MortonOrder(self, Points, DevideLevel):
        ############################################################################
        #
        # モートンオーダーを扱う上では全ての点はR^2空間の部分空間出なくてはならない.
        # Z^2空間では負の値も含むので安定的な動作は保証されない.
        #
        # 点群に対するモートンオーダー : 計算量 O(n)
        #
        #############################################################################

        MortonArray = list()

        # 与えられた点をX,Yに分解
        X = (Points[:, 0:1]).reshape(1, len(Points))[0]
        Y = (Points[:, 1:2]).reshape(1, len(Points))[0]

        # 最小点と最大点の相対距離を求める
        minX = X.min()
        minY = Y.min()

        print( "min-X:{0} min-Y:{1}".format(round(minX, 5), round(minY, 5)) )

        maxX = X.max()
        maxY = Y.max()

        print( "max-X:{0} max-Y:{1}".format(round(maxX, 5), round(maxY, 5)) )

        relateX = maxX + minX
        relateY = maxY + minY

        print( "relata-X:{0} relate-Y:{1}".format(round(relateX, 5), round(relateY, 5)) )

        UX =  relateX / 2**DevideLevel
        UY =  relateY / 2**DevideLevel

        print( "DevideX:{0} DevideY:{1}".format(round(UX, 5), round(UY, 5)) )

        X = (Points[:, 0:1]//UX).reshape(1, len(Points))[0].astype(int64)
        Y = (Points[:, 1:2]//UY).reshape(1, len(Points))[0].astype(int64)

        length = len(X)

        for n in range(0, length):
            #MortonArray.append( self.XY2Morton(X[n], Y[n]) )

            MortonArray.append( format(self.XY2Morton(X[n], Y[n]), 'b').zfill(2*DevideLevel) )
            #MortonArray.append( format(self.XY2Morton(X[n], Y[n]), 'b') )

        return array(MortonArray)


    def SpacePosition(self, MortonOrder, width, height):
        #########################################################################
        #
        # あるモートンオーダーに対して、空間を描画する為の四角形の座標を返します。
        # さらに、所属する空間分だけの座標を返します。
        #
        # 計算量 O(n)
        #
        #########################################################################

        position       = list()
        length         = len(MortonOrder)
        start_x, end_y = 0, 0

        for i in range(0, length, 2):
            width /= 2
            height /= 2

            start_x += width*( int(MortonOrder[i+1]) )
            end_y += height*( int(MortonOrder[i]))

            start_y = end_y + height
            end_x = start_x + width

            position.append( (start_x, start_y, end_x, end_y) )

        return tuple(position)


    def LinearCorrespond(self, BasePoints, FragmentPoints):
        # 線形探索
        # 計算量O(n^2)

        for FragmentPoint in FragmentPoints:
            min_dist = 10**3
            for BasePoint in BasePoints:
                x = power(BasePoint[0] - FragmentPoint[0], 2)
                y = power(BasePoint[1] - FragmentPoint[1], 2)

                dist = sqrt(x + y)

                if min_dist > dist:
                    min_dist = dist

            self.MinArray = append(self.MinArray, min_dist)

        print(len(self.MinArray))
        print(argmin(self.MinArray))


    def Display(self):

        r = 50
        px, py = self.FragmentPoints[:, 0:1], self.FragmentPoints[:, 1:2]
        length = len(px)
        for i in range(length):
            self.Canvas.create_oval(px[i][0], self.ly-py[i][0], py[i][0]+r, self.ly-py[i][0]-r, fill="white", tags="{0}".format(i))

        self.root.mainloop()


if __name__ == "__main__":
    # sample data
    x, y = exp_array(0.1, 3.6)
    y = add_noise(y)
    #x = x*10

    # get data
    u = y + 1
    u = add_noise(u)

    points = []
    pointCloud = zip(x, y)
    pointCloud_1 = array(list(pointCloud))

    # 0~360
    x = x[260:360]
    y = y[260:360]
    pointCloud = zip(x, u)
    pointCloud_2 = array(list(pointCloud))

    icp = ICP()
    points = icp.MortonOrder(pointCloud_1, 1)
    space = list()
    for point in points:
        space.append( icp.SpacePosition(point, 2, 2) )
    print( tuple(set(space)) )

    #icp.Display()
