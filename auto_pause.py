#!/usr/bin/env python

import cv2
import numpy
import subprocess as sp

cap = cv2.VideoCapture(0)

app_name = 'firefox'
app_paused = False

notPresentCount = 0

def pauseApp():
    global app_paused
    global notPresentCount

    print('Pause App called, count={}, state={}'.format(notPresentCount, app_paused))


    if app_paused :
        return

    notPresentCount = notPresentCount+1

    if notPresentCount > 5:
        print('Pausing App')
        sp.getoutput('kill -STOP $(pidof {})'.format(app_name))
        app_paused = True


def resumeApp():
    global app_paused
    global notPresentCount

    print('Resume App called, count={}, state={}'.format(notPresentCount, app_paused))

    if not app_paused:
        return

    notPresentCount = 0


    print('Resuming App')
    sp.getoutput('kill -CONT $(pidof {})'.format(app_name))
    app_paused = False

def main() :
    if sp.getoutput('pidof {}'.format(app_name)) == '':
        print('App Not Running!')
        return

    while True:
        res, photo = cap.read()
        photo = cv2.resize(photo,(240,180))

        face_model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        coords_list = face_model.detectMultiScale(photo)


        print('There are {} face(s) in this picture'.format(len(coords_list)))

        for coords in coords_list:
            x1 = coords[0]
            y1 = coords[1]
            x2 = coords[2] + x1 # width + x1
            y2 = coords[3] + y1 # height + y1
            photo = cv2.rectangle(photo, (x1, y1), (x2, y2), (255,0,0), 2)

        if len(coords_list) >= 1:
            resumeApp()

        else:
            pauseApp()

        cv2.imshow('hi', photo)
        if cv2.waitKey(1) == 13:
            break

    cv2.destroyAllWindows()
    cap.release()


main()
