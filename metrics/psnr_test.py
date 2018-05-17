import cv2
import numpy
from WSPsnrCalc import WSPsnrCalc

game_TR = cv2.VideoCapture("./user01/game_output_1.mp4")
game_CR = cv2.VideoCapture("./user01/game_output_1_CR.mp4")

retT, frameT = game_TR.read()
retC, frameC = game_CR.read()
print("Start Evaluating WS-PSNR...")
val = WSPsnrCalc(frameC, frameT)
print(val)

