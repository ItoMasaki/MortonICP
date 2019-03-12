def pos(b, width, height):
    # 計算量 O(n)

    position = list()

    length = len(b)

    start_x, end_y = 0, 0

    for i in range(0, length, 2):

        width /= 2
        height /= 2

        start_x += width*( int(b[i+1]) )
        end_y += height*( int(b[i]))

        start_y = end_y + height
        end_x = start_x + width

        position.append( ((start_x, start_y), (end_x, end_y)) )

    print(position)

if __name__ == "__main__":
    pos("1010", 10, 5)
