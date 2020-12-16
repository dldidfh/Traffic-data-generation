import cv2
import numpy as np

isDragging = False
draggingCount = 0
x0, y0, w0, h0 = -1, -1, -1, -1
line_list = []
blue, red = (255,0,0), (0,0,255)

def onMouse(event, x, y, flags, param):
    global isDragging, x0, y0, draggingCount
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        isDragging = True
        x0 = x
        y0 = y
    elif event == cv2.EVENT_MOUSEMOVE:
        if isDragging:
            img_draw = img.copy()
            # for i in range(len(line_list)):
            #         cv2.line(img_draw,(line_list[i][0]), (line_list[i][1]), blue, 2)
            cv2.line(img_draw, (x0,y0), (x,y), red, 2)
            cv2.imshow('img', img_draw)
    elif event == cv2.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            draggingCount += 1
            w0 = x - x0
            h0 = y - y0 
            line_list.append([(x0,y0),(x,y)])
            print("x:%d, y:%d, w:%d, h:%d, Lx:%d, Ly:%d" % (x0,y0,w0,h0,x,y))
            print('라인 리스트 : \n',line_list)
            # if w0 > 0 and h0 < 0:
            img_draw = img.copy()
            for i in range(len(line_list)):
                cv2.line(img_draw,(line_list[i][0]), (line_list[i][1]), blue, 2)
            # cv2.line(img_draw, (x0,y0), (x,y), blue,2)
            cv2.imshow('img', img_draw)
                # roi = img[y0:y0+h0, x0:x0+w0]
                # cv2.imshow('cropped', roi)
                # cv2.moveWindow('cropped', 0, 0)
                # cv2.imwrite('./cropped.jpg', roi)
                # print('croped.')
        else:
            cv2.imshow('img', img)
            print('좌측상단에서 우측 하단으로')
        # return line_list

def draw_line(frame):
    # global line_list
    # img = cv2.imread('test.jpg')       
    cv2.imshow('img',frame)
    cv2.setMouseCallback('img', onMouse, frame)
    cv2.waitKey()
    cv2.destroyAllWindows()
    # for i in range(len(line_list)):
    #     cv2.line(img,(line_list[i][0]), (line_list[i][1]), blue, 2)
    # cv2.imshow('img', img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return line_list

