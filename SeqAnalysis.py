
import sys
import os
import ctypes
import threading
import shutil
import base64
import time
import urllib.parse
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter, OrderedDict
import concurrent.futures
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QPushButton, QLineEdit, QFileDialog, 
                             QMessageBox, QCheckBox, QGroupBox, QGridLayout, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QUrl
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QFontDatabase, QDesktopServices, QPixmap, QPainter, QPainterPath

# --- ASSETS ---
FONT_DATA = "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gAD/AAaqrIGPSaX//85VVqb//96qqqf//96qq6f//+9VVf8AJFVUi/8ALKqsCIv/ADCqrP8AE4AA/wAoKqyy/wAfqqiy/wAfqqj/ADLVVv8AD9VY/wA+qqqL/wBpVTCL/wBTVVT//9WqqP8APVV8//+rVVgIk4vNvouTBW//AClVWP//2oAA/wAiqqhcp1yn///MKqz/ABFVWP//x1VU/wAGqqgI9ywx+yoH//+tVVb///iqqP//vNVU///j1Vj//8xVVlr//8xVVVr//+Yqq///wtVUi///tqqsi///21XE/wAGqqr//99VVP8ADVVW///jVOj/AA1VVf//41VU/wAUgABy/wAbqqv//+qqrP8AG6qr///qqqz/ABoqq///7tVU/wAYqqp+/wAYqqp+q///8YAA/wAnVVZ7CP8ACVVWh/8AEYAA///41VT/ABmqqv//9aqs/wAZqnD///WqrP8AEaqq///41VT/AAmq5of/AAmqqof/AA+qqoT/ABWqrIH/ABWqrIH/AA+AAIP/AAlVVIX/AAlVVIX/AAyqrP//99VUm///9aqsm///9aqs/wALgAD///ZVVJKCCJKC/wAHqqz///WAAP8ACFVUf/8ACFUAf/8ABdVU///zVVb/AANVrP//8qqq/wADVVT///Kq4v8AAaqs///xqqqL///wqnSL///Gqqr//+gqrP//0dVW///QVVRo///QVVRo///CgAD//+6AAP//tKqsi0mLUZlZpwhZp2OxbbsIgotKWIuCBf8AJKqr///MqrL/AC6AAGH/ADhVVf//31VO/wA4VVb//99VVf8AP4AA///sqqv/AEaqqoUI+zDl9zAH5f8AB1VR/wBJqqz/ABzVVf8AOVVU/wAyVVr/ADlVVP8AMlVW/wAcqqz/AEDVVIv/AE9VVggO+FX4BfjgFf8AVVVW/wABVVT/AET//v8AI6qs/wA0qqzR/wA0qqzR/wAaVVTni/cGi/8Ac1VY///lqqzo///LVVT/AEaqqP//y1Vk/wBGqqhG/wAjVVj//6qqnIv//6tVVov//7tVVf//3Kqo///LVVX//7lVWP//y1VV//+5VVj//+Wqqy6L//+MqqgIi///jVVU/wAaVVX//6OAAP8ANKqr//+5qqz/ADSqq///uaqs/wBEqqv//9zVVP8AVKqqiwj7MvzgFeuL+pAcBSeJlyuL/pAc+tkF9zT5KhX//8VVVov//9Eqqv8AGyqsaP8ANlVUaP8ANlUg///ugAD/AEfVVIv/AFlVjIvl/wARgAD/AEhVWK7/ADaqqK7/ADaqqP8ALtVW/wAbVVj/ADqqqov/ADqqqou6///kqqj/ACNVVv//yVVY/wAjVVT//8lVWP8AEaqs//+3qqiLMQiL//+mqqz//+5VVP//uCqo///cqqz//8mqrP//3Kqq///Jqqxc///k1VT//8VVVosI+bv9TxXfi/8ARFVY/wAjVVX/ADSqqP8ARqqr/wA0qqj/AEaqqf8AGlVY/wBcVVWL/wByAAKL/wBz//L//+XVWP8AXSqq///Lqqj/AEZVZP//y6qo/wBGVVT//7uAAP8AIyqs//+rVViL//+qqqiL//+61VT//9zVVP//ywAE//+5qqxW//+5qqz//+WAAP//otVUi/sICIv7Bv8AGoAA//+jqqrA//+5VVbA//+5VVb/AEUqqP//3Kqq/wBVVViLCOEE///FVVj/////////0NVQ/wAbKqv//9xVWP8ANlVW///cVVT/ADZVVf//7iqs/wBH1VWL/wBZVVaL5f8AEdVU/wBIVVT/ACOqrP8ANqqs/wAjqmj/ADaqrP8ALyqo/wAbVVT/ADqq8IvFi/8ALoAA///kqqyu///JVVSu///JVWT/ABGAAP//t6qqi///pf/yCIv//6aqqv//7oAA//+4Kqto///Jqqto///Jqqv//9GAAP//5NVVUYsIDuccBG3TFYKRBXuB///uVViG///sqqiLeYv//+5VWJH//+6qqJf//+6qrJd3n///6VVUp/8ARKqo/wBSqqr/ACJVWOiL/wBnVVaL/wBtVVRm/wBjqqxB5QiDiz1Wi4IF/wAZVVT//+NVVKD//9wqrP8AEKqsYP8AEKqsYP8ACFVU///UKqqL///TVVaL//+5VVb//+xVVEz//9iqrP//yKqqCPvk+GMF///eqqz/AC9VVP//51VU/wAjqqx7o3ujeP8AHqqsdf8AJVVUdf8AJVTg///wVVb/ACFVVP//9qqq/wAdVcz///aqqv8AHVVQ///7VVani/8AGqqwi/8AOVVY/wAUVVb/AC0qqP8AKKqqrP8AKKqqrP8AM1VW/wARKqjJ/wABVVgI/wBYqqyL1v//16qo/wA9VVT//69VWAiTi83Ei5MF//+vVVTv//+bqqy9+wyL//+iqqqLPv//5tVY///DVVb//82qqP//w1VW///Nqqj//+Gqqv//vNVYizeL///XVViT///XKqibYpti/wAYqqr//9AqrP8AIVVW///JVVT//7lVVv//3qqs///C/////8uqqP//zKqr//+4qqwI///Mqqv//7iqrP//5lVV//+tVVSLLYv//6yqsv8AFNVV//+1Kqv/ACmqq///vaqj/wApqqv//72qqv8AONVV///MqqvT///bqqvT///bqqvb///t1VXji/cOi/X/ACGqquX/AENVVv8APKqs//+8qqv/ADyqqP//3lVV/wA8qqyLCP8AHKmYi/8AGqqokv8AGKvAmQiNkQX+SPguFYv/AEtVVv8AE6qr/wBB1Vb/ACdVVf8AOFVU/wAnVVb/ADhVVP8AMVVU/wApKqz/ADtVVqUIyi/39Px5Bf//tVVUU///qqqsbyuL//+Wqrj/////////qKqq/wAfqqv//7qqnv8AP1VW//+6qrH/AD9VVf//3VVV/wBRqqv/////+u8IDv1r9y756hUgCg78t/dn+NEVi/cy/wAaVVX/AJpVVP8ANKqr/wCWqqz/ADSqqv8Alqpg1/8AiKqo/wBjVVb/AHqq+Aj7CQb//59VVv//fqqo//+1qqr//3RVWFf7Klf7KnH//2iqrIv//2dVVIv//2dVWqX//2jVVr///2pVUP8AM/////9qVVX/AEpVVf//dIAA/wBgqqz//36qqwj3CQb//5yqqv8AeqqqP/8AiIAA///LVVb/AJZVVv//y1VV/wCWVVD//+Wqq/8Amiqqi/8AngAGCA78t6ocBaYV/wBjVVb//4VVWP8AS/////93VVD/ADSqq///aVVY/wA0qqr//2lVVP8AGlVW//9lqqyL+zKL+zL//+Wqqv//ZdVU///LVVb//2mqrP//y1VY//9pqqs///93f////5yqqP//hVVWCPcIBv8AYVVW9xb/AEqqqv8Ai6qrv/8AlVVVv/8AlVVUpfcri/8AmKqsi/8AmKqscf8AlyqoV/8AlaqsV/8Alaqo//+1VVX/AIvVWP//nqqr9xYIDvtA+DgcBVwVi/u9+5b3KGBD95b7J/uW+yq2Q/eW9yqL+7/di4v3v/eW+yq20/uW9yr3lvcnYNUF+5b7Kov3vQUOlfqU+SUV/D74KjH8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/8+qrMz//78qqP8AMCqs//+uqqz/AB9VVAj8cfemFYv/AESqIP8AGVVW/wA4Kqj/ADKqqv8AK6s4/wAyqqr/ACuqqMv/ABXVWP8ATVVWi9mL/wBAVVT//+oqqP8AMqqs///UVVj/ADKqrP//1FVY/wAZVVT//8fVUIv//7tVWIv//7tVVP//5oAA///HqqxYX1hf//+/1VR1//+yqqyLCP//sqqqi0v/ABXVVP//zVVW/wArqqz//81VVv8AK6qs///mqqr/ADiAAIv/AEVVVAj3oP5SFSH/////////p9VW/wAdqqv//7mqqv8AO1VW//+5qrH/ADtVUv//3NVV1//////6/wBcqq7/////+uf/ACNVVdf/AEaqscf/AEaqqsfjqf8AaVVWi/WL/wBYVVT//+HVVP8ARqqs///Dqqz/AEaqrP//w6qs/wAjVVT//7Qqqov//6SqqgiL//+iqq7//9zVVP//s9VV//+5qqz//8T//f//uaqsUP//p4AA///igAD//5VVVIsIDpP6gvofFYv/AISqaF//AGuqqDP/AFKq8DP/AFKqqPsG/wApVVj7IIv//3dVVIv//49VVv//1aqo//+nVVb//6tVWP//p1VW//+rVVj//9OqqiGL//+AqqiL+xT/ACwqqv//laqs/wBYVVb//6tVVP8AWFVW//+rVVb/AHAqqv//1aqq9xyLCP8Ac1VUi/8AZqqs/wApqqrl/wBTVVYv//9Iqqz//3KqrP//Qqqp//9BVVT//zyqqwiLg8pYk4sF9zj/AKqqq/cU/wCoKqnn/wClqqzn/wClqqz/AC2qrP8Akyqo////VVT/AICqrAj8bvvyFf//kVVWi///p1VU/wAhVVT//71VVv8AQqqs//+9VVb/AEKqrP//3qqq34v/AGVVVP/////77/8AIVVV/wBTgAD/AEKqsM7/AEKqqM7/AFiqqv8AIYAA/wBuqq6L9wSL/wBZgAD//96AAM5Izkj/ACGAAP//rIAAiycIi///mqqs///eKqw3//+8VVT//71VVP//vFWA//+9VVT//6bVVP//3qqs//+RVSyLCA79APeA+eIV/wAaqpqL/wAWqqr/AAlVVP8AEqq8/wASqqz/ABKqqv8AEqqs/wAJVVahi/8AGVVUi/8AGqqs///2qqr/ABaqqP//7VVW/wASqqz//+1VVv8AEqqo///pVVT/AAlVWP//5VVWi///5qqri///6dVV///2qqh4///tVVh4///tVdD///aAAP//6VVUi///5VTcCIv//+aqrP8ACYAAdZ7//+1VVJ7//+1VVP8AFiqr///2qqz/ABlVVYsI/f0E/wAaqpqL/wAWqqr/AAmAAP8AEqq8nv8AEqqqnv8ACVVW/wAWKqqL/wAZVVaL/wAaqqj///aqqv8AFqqq///tVVb/ABKqrv//7VVW/wASqqv//+lVVP8ACVVV///lVVaL///mqquL///p1VX///aqq3j//+1VVXj//+1VVv//9oAA///pVVSL///lVVYIi///5qqq/wAJgAD//+nVVp54nnj/ABYqq///9oAA/wAZVVWLCA780feg+eoV/wAaqqqL/wAW1Vb/AAlVVJ7/ABKqrJ7/ABKqrP8ACYAA/wAWqqiL/wAaqqyL/wAaqqz///aAAP8AFtVUeJ54nv//6Sqq/wAJgAD//+VVVov//+VVZIv//+lVVf//9oAA///tVUd4///tVVV4///2qqv//+kqrIv//+VVVAiL///lVcj/AAlVVf//6VVU/wASqqv//+1U5P8AEqqr///tVVT/ABaqqv//9qqs/wAaqquLCPsZ/t4Vi4W+YpaLBf8AcKqq/wCTVVXC/wB3qqv///1VVuf///6qqv8AHKqq///2gAD/ABfVVv//7lVWnv//7lVWnv//6YAA/wAJgAD//+Sqqov//+Sqq4v//+kqqv//9qqr///tqqv//+1VVf//7aqr///tVVb///bVVf//6VVUi///5VVWi///61VW/wAFqqv//+1VVP8AC1VV///vVVYI/wALVUn//+9VVf8AD1VV///0qqv/ABNVYoX///6qq///61VW///21VX//99//3r//9Oqq3r//9Oqq///6IAA///VKqpt///WqqsIDiX3TvknFfku/B+Rg4s1g4X9p/hji8z5p/hjk4WLNYWDBQ73Ifcn+gkVNfpD4Qf+Q/xbFTX6Q+EHDiX5ufknFf0w+CCHk4vhk5H5pfxji0r9pfxjg5GL4Y+TBQ4t+HUcBUwV//+YqrCL//+lqqr//+BVWP//sqqm///Aqqj//7KqrP//wKqo///OVVb//7JVWP//6f/+LwiNg+J2k40F/wATVVXV/wAnKqvJxr3Gvf8AQ9VWpP8ATKqqi/8AXqqsi/8ATlVUcclXyVeqSos9i///5qqs///8gAD//+eAAIT//+hVVIT//+hVxP//+IAA///r1VSD///vVOgIg///71VU///y1VR4///tqqz//+qqrP//7aqs///qqqz///HVVP//8FVUgYGBgXp7c3Vzdf//8FVU///xVVT///iqrP//+Kqs///Oqqxd///b1VT//9KAAHRedF7///SAAP//ydVWi///wKqqCDfv4QeL/wAvVVb/AAjVVP8AKSqq/wARqqyu/wARqqyu/wAeKqj/ACWAAP8AKqqss/8AB1VU/wAGqqz/AA8qrP8ADiqoov8AFaqsov8AFaqs/wAQgAD/AA/VVJWVlZX/AA6qrP8AD4AA/wATVVSg/wATVISg/wAOVVT/ABKAAP8ACVYomwj/AAlVVJv/AAqAAP8AEyqs/wALqqz/ABZVVP8AC6qs/wAWVOj/AAgqqP8AFtVU/wAEqqz/ABdVxP8ABKqs/wAXVGj/AAJVVP8AGFVUi/8AGVZEi/8Aaqqo///Xqqz/AFfVWP//r1VU0P//r1Vs0P//mFVU/wAigAD//4FVQIsInhz7XBX//+aqqot1///2qqv//+1VVv//7VVV///tVVb//+1VVv//9qqq///pVVSL///lVVaL///lVVb/AAlVVv//6Sqq/wASqqp4/wASqqp4of//9oAA/wAZVVaL/wAaqqyL/wAWqqj/AAmAAP8AEqqsnv8AEqqsnv8ACVVU/wAW1VWL/wAaqqsIi/8AGqqp///2qqz/ABaqq///7VVU/wASqqz//+1V3P8AEqqr///pVVT/AAlVVf//5VTQiwgO+SH59PuMFd2L2f8AC9VV1f8AF6qr1f8AF6qryf8AHyqqvf8AJqqrCIuTXsmDiwX//5NVWEH//4ZVVGb//3lVVIv7Eov//43VVP8AHFVV//+Zqqz/ADiqq///maqq/wA4qqv//6+qqv8AT3/////Fqqz/AGZVVv//xaqr/wBmVVb//+LVVf8ActVUi/8Af1VWi/8Afqqs/wAc1VX/AHKqqP8AOaqr/wBmqqz/ADmqqP8AZqqs/wBRKqr/AFD//P8AaKqu/wA7VVgI/wBoqqz/ADtVWPcK/wAdqqj/AINVVIv/AHyqrIv/AHB//P//5dVY/wBkVVj//8uqqP8AZFVY///Lqqja//+2Kqz/ADmqqP//oKqs/wA5qqj//6CqrP8AHNVY//+UVVSL+wyL//+XVVZ2//+tgABh///Dqqph///DqqtX///h1VVNiwhhi2qac6lzqX//ACxVVov/ADqqqgj4jDv7Kwf//79VWP8AZ1VU//+eVVT/ADOqrP//fVVUi///kVVUi///poAAZ///u6qsQ///u6qqQ///3dVW//+lqqyL//+TVVSL//+Uqqr/ACIqqv//piqq/wBEVVb//7eqrP8ARFUs//+3qrD/AFjVVP//29VV/wBtVYD/////+8+L/wA8qqz/AA6qq/8ANVVU/wAdVVUI/wA1VVj/AB1VVf8AKaqo/wAoVVWp/wAzVVaT///Kqqr/ABWqqP//1aqr/wAjVVj//+Cqq/8AI1VY///gqqv/AC6qqP//8FVVxYv/AFiqqP/////+/wBKVVj/ACPVVcf/AEeqrcf/AEeqqqn/AGYqqov/AISqrIv/AGSqrP//7Sqo/wBegAD//9pVWP8AWFVUCP//2lVY/wBYVRj//8wqqP8AS9VUSf8AP1WUSf8AP1VY//+wVVj/ADHVUP//oqqo/wAkVVj//6KqqP8AJFVY//+bVVT/ABIqqP//lAAEi///kKqsi///l4AA///sgAD//55VVGT//55VVmT//6zVVP//yqqo//+7VVb//7xVWP//u1VW//+8VZD//8nVVf//r1VU///YVVX//6JVHAj//9hVWP//olVU///sKqv//5wqrP/////9IYs1mP//raqqpf//sVVWpf//sVVW/wAk1VX//7nVVf8AL6qr///CVVX/AC+qqv//wlVV/wA3VVb//8pVVsr//9JVVf8APv/y///SVVX/AEYqqmj/AE1VZP//56qr/wBNVVT//+eqq9v///PVVf8AUqqsiwhc+G0V//+qqqyL//+61VT/AB1VVVb/ADqqq1b/ADqqqv//5YAA/wBIVVaL4Yvh/wAagAD/AEiAAMDGwMb/AEUqrP8AHYAA/wBVVVSL/wBTVVSL0P//46qs/wA2qqz//8dVVP8ANqqo///HVYD/ABtVWP//tlVUi///pVUsCIv//6VVVv//5IAA//+2gABU///HqqpU///Hqqv//7sqrP//49VV//+tVVSLCA73sRwFPeEVg40F///yqqj///VVVnr///qqqv//61VYi///6VVYi///7dVQ/wAHqqr///JVWP8AD1VW///yVVj/AA9VVv//8YAA/wAaVVX///CqqP8AJVVVCPx+HASFSov80Bz6zfcBi/cb99P5XYvX+0oFpU3/ABpVWP//1lVV/wAaqqj//+qqq/8AH1VY///nVVX/ACJVUP//86qr/wAlVViL/wAlVViL/wAeqqj/AAmqq6P/ABNVVQiPkwX+lvgmFffR+X/3zv1/BQ73PPoT+UwV/wA6qqyl/wAvKqj/ACYqrP8AI6qs/wAyVVT/ACOqqP8AMlUg/wAR1Vj/ADrVVIv/AENVjIv/AGlVWP//3Kqo/wBTqqj//7lVWMn//7lVVMkhqv//cqqsiwj8ZRz6zfiJBv8Akqqsi/8Ab4AA/wAhVVb/AExVVP8AQqqq/wBMVVj/AEKqp/8AJiqo/wBYVVWL/wBuAASL/wBRVVb//+fVWP8ARSqq///PqqjE///PqujE///C1VT/ACkqrP//tf/E/wAZVVQI+234sRX/AF6qrIv/AEqAAHX/ADZVVF//ADZVVF//ABsqrE2LO4v//7FVjP//5dVU///CVVT//8uqrP//01Ug///Lqqz//9NVVP//t9VU///pqqwviwj8E/iMBvg6HPuJFfw6+Lv4Lgb/AGKqrIv/AE+AAHL/ADxVVFn/ADxVVFn/AB4qrEiLN4v//61VVm7//71//1H//82qq1H//82qq///s1VU///m1VX//6CqrIsIDvfS92P5LhWL//+RVVT/ABmqq///m1VW/wAzVVX//6VVVv8AM1VW//+lVVb/AEaAAP//uP///wBZqqr//8yqq/8AWaqs///Mqqv/AGMqqP//5lVV/wBsqqyL6//////+/wBYqqz/ABOqqv8AUVVU/wAnVVj/AFFVWP8AJ1VVzv8ANqqr/wA0qqjRCJOL0lSLggX//8CqqP//r1VW//+w1Vj//8DVVSz//9JVVSz//9JVVf//mSqs///pKqv//5FVVIv//59VYIv//6TVVP8AEdVV//+qVUz/ACOqq///qlVW/wAjqqv//7aAAP8AMFVV///CqqrI///Cqqv/ADz/////z4AA/wBJVVX//9xVVf8AVaqs///cVVj/AFWqqv//7iqr/wBa1Vb//////esIi+v/ABHVVf8AWqqs/wAjqqv/AFVVVP8AI6qr/wBVVVT/ADCAAP8ASVVU/wA9VVX/AD1VWP8APVVW/wA9VVj/AEmAAP8AMFVQ/wBVqqr/ACNVWP8AVaqs/wAjVVj/AFsqqP8AEaqo/wBgqqyL/wBuqqyL/wBm1VT//+kqqOr//9JVWOr//9JVWP8ATyqo///A1VD/AD9VWP//r1VYCIuDRFODiwX//8tVWNFI/wA2qqj//66qqP8AJ1VY//+uqqz/ACdVWP//p1VU/wATqqgri///k1VUiyj//+aqqP//pqqs///NVVj//6aqqv//zVVY//+5gAD//7lVUP//zFVW//+lVVj//8xVVf//pVVU///mKqsmi///kKqsCA74C/k8HAUzFfxzHPrN+HMG/wDRVVSL/wCmqqzI9xD3DvcQ/wB5//7J/wChqqqL/wDJVViL/wDHVVT//8HVWP8AoFVU//+Dqqj/AHlVWP//g6rI/wB5VVj//1mAAP8APKqo//8vVTiLCBz7KwT8CxwEd/gLBv8AsVVUi/8AjIAA///MKqj/AGeqrP//mFVY/wBnqqj//5hVVP8AM9VY//91gACL//9SqqyL//9SqqxX//91VVQjIyMj//9zqqxX//9PVVSLCA6u+qQcBNUV6f3bHPrN+dvp/XP4qfjY5/zY+JoHDkj6axwE1RXp/aIc+s3z+Qf4ref8rfiaBw74TxwFvPlEFYOV/SmLiy34x4sF///+rAD//59VVv//5aqoMv//zKlY//+uqqr//8yqqP//rqqu//+61Vj//7/VVTT//9D//TRc//+hKqz//+iAAP//mVVUi/sA//////7//51VVP8AGaqq//+mqqz/ADNVWP//pqq2/wAzVVL//7mqqtL//8yqoP8AWqqu///Mqqv/AFqqqv//5lVV/wBkqqqL/wBuqqwIi/8Ab1VU/wAZ1VXw/wAzqqv/AFqqrP8AM6qq/wBaqiD/AEaAAP8ARqqo/wBZVVb/ADKrOP8AWVVU/wAyqqju/wAZVVj/AGyqrIvri/8AWKqs///sVVj/AFFVVP//2Kqo/wBRVVj//9iqqM7//8lVWP8ANKqoRQiTi9LHi5MFTdv//7GqqP8APlVY//+hVVj/ACyqqP//oVVU/wAsqqgk/wAWVVj//5CqrIv//59VVIv//6SqrP//7lVYNf//3KqoNf//3KtI//+2Kqr//8+qqP//wlVW///CqhD//8JVXP//wqqo///PVVX//7aqrP//3FVP//+qqqz//9xVWP//qqqs///uKqv//6VVVP/////9KwiLK/8AEdVV//+lKqr/ACOqq///qlVW/wAjqqv//6pVVv8AMIAA//+2qqr/AD1VVU7/AD1VVk7/AElVVP//z6qq/wBVVVb//9xVVv8AVVVU///cVVX/AFqqrP//7iqr64v/AH9VVIv/AHOqrP8AHaqr8/8AO1VV8/8AO1VV/wBRVVj/AFBVVf8AOqqo/wBlVVYI/wA6qqj/AGVVVv8AHVVY/wBvVVaL/wB5VVSL/wAUqqz///9VWP8AEFVU///+qqiXCA74ExwEkxwFMxX8+P32+PgjHPrN8/kH+fb9B/QcBTMHDvzg910cBTMVHPrN8xwFMwcOPfemHAUzFS34Wf30B4svcP//ttVVVf//yaqrVf//yaqrR///5NVVOYv//4Kqrv/////+//+bqqv/ADlVVv//tKqn/wByqqwIg4tDT4uDBf8AV//9+xr/AH+qq0j/AKdVWIv/AG1VMIv/AFvVVP8AIyqq/wBKVXz/AEZVVv8ASlVU/wBGVVb/ACUqrP8AYNVUi/8Ae1VWCPpUBw72HASi4RWDjQX//+6qqP//9VVWd///+qqq///pVViL///pVViL///oqqj/AAgqqnP/ABBVVnP/ABBVVv//46qs/wAbKqr//99VVLEI/FH4nPjq+QWFk/sRi/08/VqL+Voji4sc+s3zi4v4dfch9yb4PPyEBf8AWqqsI/8AUKqsV/8ARqqoi7GLq/8ACaqrpf8AE1VVCI+TBQ4z+lvpFf0qHATVIxz6zfmSBg75AfcXFvclHAUzzYv4dxz7bfh4HASTzIv3D/7uBf8ABqqo///IqquU///Z////AAtVWP//61VW/wALVVj//+tVVv8AD6qo///1qqqfi/8AFKqoi5z/AAVVVv8ADVVY/wAKqqoIk4moQYWDBXP//+yqq23///ZVVWeL//+iqqj//////1X/AEOqq///8VVY/wCHVVYIKfob/FH+zUqL/FH6yfsL/skFDvghHASkHAUzFYv+/P4u+vxKi4sc+s3xi4v6/Pou/vzMi4scBTMFDviQ+bVyFf8AYqqsi/8AXNVU/wAR1VXi/wAjqqvi/wAjqqv/AEqAAP8AMFVVycjJ/wA8////ADDVWP8ASVVV/wAjqqj/AFWqrP8AI6qo/wBVqqr/ABHVWP8AWtVWi+uL6///7iqo/wBaqqz//9xVWP8AVVVU///cVVj/AFVVVP//zyqo/wBJVVRN/wA9VVgITf8APVVY//+1gAD/ADBVUDT/ACNVWDT/ACNVWP//oyqs/wARqqj//51VVIv//3yqrIv//4iAAP//4dVY//+UVVT//8OqqP//lFVW///Dq0D//6uqqv//rSqoTv//lqoYTv//lqqs///hgAD7CYv//39VVIsrnf//pSqqr///qlVWCK///6pVVrz//7aqqslOyU7/AEqAAP//z6qq4v//3FVW4v//3FVV/wBc1VT//+4qq/8AYqqsiwjuBPsE//////7//5qAAP8AGaqqMP8AM1VYMP8AM1VV//+4qqr/AEbVVf//zFVW/wBaVVb//8xVVf8AWlVW///mKqv/AGTVVov/AG9VVIv/AG9VPP8AGdVV/wBk1VT/ADOqq/8AWlVw/wAzqqr/AFpVWP8AR1VW/wBGqqjmvua+/wBlgAD/ABmAAPcEiwj3BIv/AGWAAP//5oAA5ljmWP8AR1VY//+5VVj/ADOqqP//paqo/wAzqqj//6WqrP8AGdVY//+bKqiL//+QqqyL//+Qqqz//+YqqP//myqq///MVVj//6Wqqv//zFVY//+lqqr//7iqqP//uSqrMP//zKqrMP//zKqr//+agAD//+ZVVfsEiwgO2/kuHAUzFfxlHPrN8/i19/0G/wCMqqyL/wBs1VT/ACLVVNj/AEWqrNj/AEWqrP8AJoAA/wBgKqiL/wB6qqyL9w7//9lVWOv//7KqqNH//7KqrNH//5NVVK77IIsIof1MFfwT+O74Ewbri/8ATCqsb/8AOFVUU/8AOFVUU/8AHCqs//+3qqiL//+nVViL//+nVVT//+PVVP//t6qs///HqqxT///HqqxT//+z1VRvK4sIDviQHAWF+0YV///hVVj//+dVVf//3VVQ///zqqv//9lVWIv///dVWIv///eAAP8AAIAA///3qqiM///3qqiM///3VVj/AAJVVYL/AAOqq4L/AAOqq///+FVY/wAC1VX///mqqI3///mqqI3///fVWP8ABFVVgf8ABqqrgf8ABqqr///41Vj/AASAAP//+6qo/wACVVUI///7r0j/AAJVVf//+Cqo/wAFqqv///SmEJT///SzqJT///kqqP8ABYAA///9obCN///9ryCN///4qqj/AAZVVf//86Y4/wAKqqv///OvAP8ACqq4///5Kqj/AAWqqv///qZY/wAAqp7//9NVWP8AJVVU///WVVT/ACCqq///2VVU/wAcAAH3MK//AH6qqP8AT4AA/wBhVVj3Dwj/AGFVWPcP/wAwqqj/AI/VVIv/AKSqrIvr///uKqj/AFqqrP//3FVY/wBVVVT//9xVWP8AVVVU///PKqj/AElVVE3/AD1VWE3/AD1VWP//tYAA/wAwVVA0/wAjVVg0/wAjVVj//6MqrP8AEaqo//+dVVSL//98qqyL//+IgAD//+HVWP//lFVU///DqqgI//+UVVb//8OrQP//q6qq//+tKqhO//+WqhhO//+Wqqz//+GAAPsJi///f1VUiyud//+lKqqv//+qVVav//+qVVa8//+2qqrJTslO/wBKgAD//8+qquL//9xVVuL//9xVVf8AXNVU///uKqv/AGKqrIsI/wAOqqyL/wAPVVSIm4Wbhf8AEtVU///1VVX/ABWqrP//8Kqr/wAVqqz///Cqqv8AENVU///zgACX///2VVaX///2VVb/ABRVVP//7n///wAcqqz//+aqq/8AHKig///mqqv/ABKqqP//76qq/wAIrLj///iqq/8AJ1VY///fVVX/ACVVUP//5tVV/wAjVVj//+5VVgj/ACNVWP//7lVWsv//9yqq/wAqqqiL/wA9VViLv/8AEFVW/wAqqqj/ACCqqgiPk2TPBRz7QPnkFYv/AG9VPP8AGdVV/wBk1VT/ADOqq/8AWlVw/wAzqqr/AFpVWP8AR1VW/wBGqqjmvua+/wBlgAD/ABmAAPcEi/cEi/8AZYAA///mgADmWOZY/wBHVVj//7lVWP8AM6qo//+lqqj/ADOqqP//paqs/wAZ1Vj//5sqqIv//5CqrAiL//+Qqqz//+YqqP//myqq///MVVj//6Wqqv//zFVY//+lqqr//7iqqP//uSqrMP//zKqrMP//zKqr//+agAD//+ZVVfsEi/sE//////7//5qAAP8AGaqqMP8AM1VYMP8AM1VV//+4qqr/AEbVVf//zFVW/wBaVVb//8xVVf8AWlVW///mKqv/AGTVVov/AG9VVAgO9zQcBJzfFYCPBf//8VVY///1VVb//+uqqP//+qqqcYt3i3iQeZV5lf//8NVU/wALgAD///OqrJj///OqrJj///KqqP8AE6qr///xqqz/ABpVVf//8aqs/wAaVVX///SqqP8AFqqr///3qqye///3qqye///0gAD/ABsqqv//8VVU/wAjVVYI///Eqqz/AJCqrP//zVVU/wBUqqhh/wAYqqz/AHSqrP8ADKqs/wBZqqj/ACaAAP8APqqs/wBAVVT/AD6qqP8AQFVU/wAfVVj/AFWAAIv/AGqqrIv/AHdVWP//2aqo/wBcVVD//7NVWP8AQVVY//+zVVT/AEFVWPsB/wAgqqj//3KqrIsI/GUc+s3z+Nj3tQb/ADVVVIv/AD6qrP//q1VU0///Vqqs/wADU8z///dVVv8ABVVU///zVVT/AAdW4P//71VW/wATVIj//9Cqq/8ADVVUa/8AB1Yk///vVVX/AAdVVP//71VVmf//5aqr/wAUqqxn/wAUqqxn/wAS1VT//+bVVZz///Gqq5z///Gqq/8AFlVUff8AG6qs///yVVUI/wAbqaj///JVVf8AHiqo///5Kqr/ACCrsP8AAAAB/wAmqqiL/wAjVVj/AAmqq6v/ABNVVQiPkwX+F/koFfjJ+BMH/wBhVVSL/wBMgAD//+bVWP8AN6qs///Nqqj/ADeqrP//zaqo/wAb1VT//7uAAIv//6lVWIs1///kKqz//7sqrP//yFVU///MVVT//8hVVP//zFVU//+zgAD//+YqrP//nqqsiwgOf9f3XRWLk8rMk4sF/wBmqqn//3qqq/8AhVVV//+9VVX/AKQAAovti/8AT4AA/wAYVVXI/wAwqqvI/wAwqqv/AB6AAP8APaqri/8ASqqqi53///3VVP8AESqq///7qqz/ABBVVv//+6qs/wAQVVb///rVVP8ADqqqhZiFmIL/AA0qqn//AA1VVgh//wANVVb///TVVP8AC4AA///1qqz/AAmqqv//9aqs/wAJqqj///GAAP8ACoAA///tVVT/AAtVWP//7VVU/wALVVT///AqrP8ACSqsfpJ+kv//7dVU/wAI1VT//+iqrP8ACqqs///oqqz/AAqqrHj/AAhVVP//8VVUkf//8VVUkf//6yqs/wAIqqxw/wALVVQIcP8AC1VU///rKqr/AAiqrP//8VVWkWWb///gVVb/AA4qrP//5qqq/wAMVVT//+aqwP8ADFVU///jKqqc///fqpb/ABWqrP//36qr/wAVqqz//+ZVVaF4/wAWVVR4/wAWVVT//++qq/8AG6qs///yVVWs///yVVWs///5Kqv/ACPVVIv/ACaqrAiL/wBjVVix/wBR1VDX/wBAVVjX/wBAVVjt/wAgKqj3DIv3Nov3GUzz+xIIi4NKToKLBf//qKqs9f//k6qowP//fqqsi///qKqqi///uFVWdVNfU19v///HqqiL//+7VViLa/8ABoAAbphxmHH/ABQqqv//6FVU/wAbVVb//+qqrP8AG1VW///qqqyn///tqqj/AByqqv//8KqsCP8AHKqO///wqqz/ACSqqnr/ACyqyP//7VVUl///+1VU/wAV1VSC/wAfqqz///KqrP8AH6qs///yqqz/ABaAAP//9oAA/wANVVT///pVVP8ADVSs///6VVT/ABTVVP//9qqs/wAcVgB+/wAcVVR+oP//9VVU/wANqqz///eqrP8ADaqs///3qqz/ABIqqP//9IAA/wAWqqz///FVVAj/ABaqrP//8VVUnP//8oAA/wALVVT///OqrP8AC1VU///zqqz/AA0qrP//8NVUmnmaeZZ5knmSef8ABiqs///rqqr/AAVVVP//6VVW/wAFVVT//+lVVv8AAqqs///oVVSL///nVVaL//+VVVb//9eqrP//qSqq//+vVVRICP//r1WESP//mFVU///egAD//4FVKIv//56qqov//6TVVv8AFFVVNv8AKKqrNv8AKKqr//+8Kqr/ADb/////zVVW/wBFVVYIDmD40xwE1RUc+ysjHATV/FDp+nctBw734PdIHAUzFf2/B4v//1lVUrv//3uAAOv//52qrv8AX//y//+dqqr/AIGqqv//ztVW/wCjVWSL9ziL/wCBqqy8/wBfVVTt/wBfVVj/AGH///8AL6qo/wCEqquL/wCnVVYI+b8l/bsHi///dKqs///ZVVj//5HVVP//sqqoOv//sqqsOv//l1VU///XgAD7GIv//3tVVIv//5eAAP8AKFVW//+zqqz/AFCqqv//s6qq/wBQqqr//9nVVv8AblVWi/cgCPm7Bw73rRwFGRwFMxUii/x3HPt5/D76lAX//+iqqsH//+Yqq/8AKCqo///jqqv/ABpVWP//46qr/wAaVVj//9wqqv8ADSqo///UqquLZYv//+Cqqv//9lVY///nVVb//+yqqAiFg6hBk4kF/wALVVT/AAtVWJz/AAWqqP8AFqqsi/8AE//8i/8AESqr///4qqj/AA5VWf//8VVY/wAOVUv///FVWP8ADtVV///mVVD/AA9VYP//21VYCPiAHPt3zYv4xRwFKwUO+fT6WxwFMxXri/fwHPuD+BMcBH3zi5CD/F8c+tVJi/wAHASP/AEc+3FKi/woHASJBf//81VV/wAlVVh//wAZ1VD///Sqq/8ADlVY///0qqv/AA5VWP//71VV/wAHKqh1i///8Kqqi///7lVW///6VVh3///0qqgIg41w1Y+TBaf/ABNVWKz/AAmqqLGL24v/ADlVVf//yqqo/wAiqqv//5VVWAj35f6MBQ73RPUcBUwVtYv/ACWAAP//9CqorP//6FVYrP//6FVY/wAkgAD//9fVULP//8dVWAj3zfxU+Eb41/cHi4+D/IT9Jff1/IwFo///3Kqr/wAVVVj//+gqq/8AEqqo///zqqr/ABKqqP//86qq/wAUVVj///nVVqGL/wATVViL/wASVVD/AAVVVv8AEVVY/wAKqqoIlYmmQYeDBf//4qqo///sqqtq///2VVX//9tVWIv//9SqqIv//9pVWP8AC6qra/8AF1VVa/8AF1VVZ/8AKFVVY/8AOVVWCPvP+FX8RvzY+weLh5P4g/km+/T4iwX//+iqq/8AIqqo///q1VX/ABfVWHiYeJj//+uAAP8ABoAAdYv//+qqqov//+2qq///+lVY///wqqv///SqqAiDjW7Vj5MF/wAdVVX/ABNVWP8AIVVV/wAJqqj/ACVVVosIDvdvHATlHAUrFYeTJYv8X/1G/An4wwVl/wA3VVj//94qq/8AJ9VQ///iVVX/ABhVWP//4lVV/wAYVVj//9wqq/8ADCqoYYtpi23///ZVWHH//+yqqAiHg6hBk4kFmf8AC1VY/wARqqr/AAWqqP8AFVVWi/8AE1VWi/8AEf/////5gAD/ABCqq37/ABCqq37/ABRVVf//6Cqoo///3VVYCPg0/P6L/Lv1i4v4vQUOyfrm5xUv/rHNB/n5HASX/c6Li+X6W4uLSv32HPtqBQ78x/hlHAVUFeH7vxz5K/e/4ftbHAYpBw5B9yccBaIVMYuFgfnJHPn75IuTlgUO/MfNHAVUFfdaHPnX+1o1978cBtX7vwYO9PkRHAUzFUmL/IX9kpGD5YuVkfg8+R/4Mv0fk4Xni5GTBQ77GbT7ExU5+gPdBw78pPcsHAXBFYKLTj+Lg/f4+4aRi7K8i5MFDqz6vdsVg40F///zVVj///VVVnz///qqqv//7qqoiwj//9lVVP//7Kqs/wAfVVX/AD6qqx/4kAeLwf//96qs/wAw1VT//+9VVP8AK6qs///vVVT/ACuqrP//6aqs/wAkKqhv/wAcqqxv/wAcqqz//98qrKP//9pVVP8AE1VU///aVVT/ABNVVGT/AA3VVP//16qs/wAIVVj//9eqrP8ACFVY///WgAD/AAQqqP//1VVUi///YVVUi///eFVV///EVVT//49VV///iKqsCIuDylSTiwX/AGFVVv8AY1VU9wL/ADGqrP8Aeqqqi8WL/wA11VT///aAAP8AMaqseP8AMaqseP8AKdVU///gqqyt///UVVSt///UVVSc///LgACL///CqqwIIAf7AP8ALqqs//+RVVT/ABdVVP//jqqsi///rqqqi0L///SqrP//v1VW///pVVT//79VVv//6VVU///K/////9sqrP//1qqrWP//1qqrWP//61VV///CKqqL//+3VVaL//+Yqq3/ACWqqv//roAA/wBLVVb//8RVU/8AS1VW///EVVX/AF1VVP//4iqr/wBvVVaLCP8ATVVUi9T/AA8qq/8ARKqs/wAeVVX/AESqrP8AHlVW/wA2qqj/ACsqqv8AKKqswwh8B4tb/wAMKqz//9lVVf8AGFVU///iqqv/ABhVVP//4qqr/wAiKqz///FVVbeL/wAhVViL/wAcqqiUo50Ij5UF/OzDFf//q1VWi///uKqq/wAVVVVR/wAqqqtR/wAqqqtu/wA6VVWL1Yv/AE1VVv8AH9VVx/8AP6qr/wAqqqr/AD+qqP8AKqqs/wBSKqr/ABVVVP8AZKqui/8AcKqsi/8AbKqo///oqqz/AGiqrP//0VVUCCEHi1v///WAAP//1Cqqdv//2FVWdv//2FVVb///36qraHJocv//2NVU///sqqr//9SqrP//8lVW///Uqqz///JVVv//01VU///5KqpdiwgO91P5NvqtFf//qKqsi///sNVUeERlRGX//8XVVlf//9KqqkkIi/i9g5EveIsc+qDvi4v3UAX/AC1VVkn/ADoqqlfSZf8ARv/+Zf8ATyqqeP8AV1VYi/8AZVVUi/8AWoAAo/8AT6qsu/8AT6qou/8APVVY/wBAqqq2/wBRVVa2/wBRVVb/ABWAAP8AWlVUi/8AY1VWi/8AY1Us///q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//aqqP//7VVQ///tVVj//+1VXf//7VVY///2qqv//+lVUP/////4///lVVgIi///5VVY/wAJVVX//+lVUP8AEqqr///tVVj/ABKqq///7VVY/wAWqqr///aqqP8AGqqriwhYHPuHFfqU7/6UBw79MvdnHAR5Ff8AGqqri/8AFqqr/wAJVVj/ABKqqv8AEqqo/wASqqr/ABKpgP8ACVVW/wAWqqiL/wAaq9iL/wAaqpj///aqqv8AFqqo///tVVb/ABKqwP//7VVW/wASqqj//+lVVf8ACVVY///lVVWL///lVVuL///pVVX///aqqP//7VVQ///tVVj//+1VVv//7VVY///2qqr//+lVUIv//+VVWAiL///lVVj/AAlVVv//6VVQ/wASqqr//+1VWP8AEqqr///tVVj/ABaqqv//9qqo/wAaqquLCFr7DRX+fQeLS///9Cqr///NVVX//+hVVf//2qqr///oVVb//9qqq///3H/////fVVX//9Cqq28Ii4WyQZSLBf8AKqqr/wAYqqr/ACKAAP8AGYAA/wAaVVX/ABpVVv8AGlVV/wAaVVv/ABWqq/8AI1VVnP8ALFVQnP8ALFVV/wAIgAD/ADSAAIv/ADyqqwj6cwcORvqO2RWBjQX//+9WTP//9qqq///wVVT///tVVv//8VRgi///4Kqs/////////9uqqP8AF6qr///Wqqz/AC9VVgj7//hK+Ef4T4mR+weL/LX8wYv6MIORL3iLHPqe74uL9+r3NPc49+z8NAWp///bVVX/AB0qrP//46qr/wAcVVR3/wAcVVR3/wAgKqyBr4uxi/8AHKqs/wAIVVX/ABNVVP8AEKqrCI+TBQ79Ffc4HAViFeeek4WLHPsxBYv//8FVVv8AE1VW///gqqv/ACaqqv///////wARVVaLmv8ABVVW/wAMqqr/AAqqqgiTiaFHh4EFc3n//+KqqoL//91VVov//9NVVov//91VVf8ADqqr///nVVX/AB1VVf//51VV/wAdVVb///Oqq/8AJqqqi7sIDvnoHAV7+q0VMYv//7DVWHb//7uqqGH//7uqqGH//8zVWFJpQ2//AEiqrF3/ADkqqEv/ACmqrEv/ACmqqP//s6qs/wAU1Vj//6dVVIs7i///uIAA///vKqhM///eVVhM///eVcz//84qqv//0dVU///bVVb//8VU4AiuB4v/AC6qrP//89VW/wAlVVT//+eqqqf//+eqq6f//94qqpn//9Sqq4v//91VVov//+Kqq4L//+f//3kIh4GiR5OJBf8AD1VW/wAMqqya/wAGVVT/AA6qqosIsZ7//9+qrP//v1VUH/308vj8B4vvq/8AUaqsy/8AP1VU/wA///L/AD9VVP8AUqqq/wAfqqz/AGVVZIv/AGCqrIv/AEuqqP//4iqs/wA2qqz//8RVVP8ANqqs///EVVT/ABtVVP//r4AAi///mqqsCP0F8/j8B4v/AGNVVP8AICqo/wBRgAD/AEBVWP8AP6qs/wBAVVj/AD+qrP8AUtVQ/wAf1VT/AGVVWIv/AGCp8Iv/AEuqqP//4iqs/wA2q2j//8RVVP8ANqqo///EVVT/ABtVWP//r4AAi///mqqsCP0F8fkNB4v/AH1VVP//3IAA/wBkqqxE10TX//+fKqix//+FVViLCA73B/kb+q0VO4v//7iAAP//76qoTP//31VYTP//31VU///NgAD//9KqrGVRCKoHi/8ALqqs///z1Vb/ACVVVP//56qqp///56qrp///3iqqmf//1Kqri///3VVWi///4qqrgv//5///eQiHgaJHk4kF/wAPVVb/AAyqrJr/AAZVVP8ADqqqiwixnv//36qs//+/VVQf/fTy+PwHi+//ACAqqv8AUaqs/wBAVVb/AD9VVP8AQFVW/wA/VVT/AFPVVv8AH6qs/wBnVVSL/wBiqqyL2m3/ADtVVE//ADtVVE//AB2qrP//r6qsi///m1VUCP0F8fkNB4v/AHyqrGX/AGSAAD//AExVVD//AExVVP//m1VU/wAmKqz//4KqrIsIDvdA+Q36rRX//2VVVIv//37VVv//zIAA//+YVVYk//+YVVYk///MKqr//4CAAIv7LP/////++yz/ADPVVv//gIAA/wBnqqwk/wBnqqok/wCBKqr//8yAAP8Amqqsi/8Amqqsi/8AgSqo/wAzgAD/AGeqrPL/AGeqqPL/ADPVWP8Af4AAi/csCIv3LP//zCqo/wB/gAD//5hVWPL//5hVcPL//37VVP8AM4AA//9lVTyLCP5pBP//gVVWi///l1VU/wAqKqr//61VVv8AVFVW//+tVVb/AFRVVv//1qqq/wBp1VSL/wB/VVb/////+v8Af1VA/wApVVX/AGnVVP8AUqqx/wBUVWz/AFKqpP8AVFVU/wBoqqr/ACoqrP8Afqqyi/8Afqqsi/8AaKqo///V1VT/AFKqrP//q6qs/wBSqqj//6uqrP8AKVVY//+WKqiL//+AqqwIi///gKqw///Wqqj//5Yqqv//rVVY//+rqqb//61VcP//q6qq//+XVVT//9XVVv//gVU8iwgO92n5TPqtFTOL//+wKqz//+xVWP//uFVU///Yqqj//7hVVv//2Kqs///FgAD//8pVVP//0qqqRwjNB4v/AC9VVP//89VW/wAlgAD//+eqqv8AG6qs///nqqv/ABuqqP//3iqq/wAN1Vj//9Sqq4v//91VVov//+Kqq4L//+f//3kIh4GiR5OJBf8AD1VW/wAMqqz/AA+qqv8ABlVUm4sI/wAkqqv/ABJVVf//36qs//+/VVQfHPtt8PiDB/8ALVVWScVX/wBGqqpl/wBGqqxl2nj/AFdVVIv/AGVVVIv/AFqqrKPbu9u7/wA9gAD/AECqqrb/AFFVVrb/AFFVVv8AFYAA/wBaVVSL/wBjVVaL/wBjVSz//+qAAP8AWlVUYP8AUVWACGD/AFFVVP//woAA/wBAqqw7uzu7//+lVVSj//+aqqyLCP5pBP//hVVkiyb/AChVVv//sKqc/wBQqqr//7Cqqv8AUKqq///YVVb/AGuqqov/AIaqrIv/AIaqrP8AJ6qq/wBrqqj/AE9VVv8AUKqs/wBPVVb/AFCqrP8AZP/+/wAoVVT/AHqqrIv/AHlVVIv/AGOqrP//1Sqs2f//qlVU2f//qlVssv//ltVUi///g1VACIv7EmT//5aAAD02PTb//5xVVP//1YAA//+GqqyLCA73ZxwE4/qSFXOd///iqqiU///dVViL///UqqiL///eVVj///IqqHP//+RVWHP//+RVdH///9nVVIv//89VOAhNB///0qqs/wBCqqz//8UqqMD//7eqrP8AJ1VU//+3qqz/ACdVWP//sCqo/wATqqj//6iqrIv//5tVVov//6XVVHP//7BVVlv//7BVVlv//8J/////v1VU///Uqqv//66qrP//1Kqr//+uqqz//+pVVf//paqoi///nKqs//////3//5yqtv8AFaqr//+lqqr/ACtVWP//rqqgCP8AK1VS//+uqqz/AD2AAP//v1VW/wBPqq7//8///v8AT6qcW/8AWiqqc/8AZKq6i/8AVqqsi/8ATqqonv8ARqqssf8ARqqssf8AOqqov/8ALqqszQj8g+8cBJMH/wBAqqz/ABNVWP8AIFVU/wAmqqge/wAOqqiLmv//+aqs/wAPVVj///NVVAiTjaHPBf0Z/kQV//+GqqqL//+cgAD/ACqAAP//slVW4P//slVW4P//2Sqq/wBpgACL9xKL/wBRVVT/ABFVVf8ASoAA/wAiqqv/AEOqrP8AIqqY/wBDqqz/ADEqqv8ANaqo/wA/qr7/ACeqrP8AP6qq/wAnqqz/AEfVVv8AE9VU24v/AHqqrIvw///Xqqz/AE9VVP//r1VUCP8AT1VU//+vVWz/ACeqrP//lFVUi///eVVAi///eVVU///YVVT//5RVVv//sKqs//+vVVb//7CqrP//r1VWJv//16qq//+FVVSLCA78E/lS+pAVZf8AE1VYYP8ACaqoW4v//8Cquov//8cqqv//8FVY///Nqpz//+CqqP//zaqq///gqqz//9eAAF///+FVVv//x1VUCKQHi/8AL1VU///z1Vb/ACWAAP//56qq/wAbqqz//+eqq/8AG6qo///eKqr/AA3VWP//1Kqri///3VVWi///4qqrgv//5///eQiHgaJHk4kF/wAPVVb/AAyqrP8AD6qq/wAGVVSbiwj/ACSqq/8AElVV///fqqz//79VVB/99PD4+AeL8/8AGiqq/wBTVVT/ADRVVv8APqqs/wA0VVb/AD6qrP8AQSqq/wAfVVTZi/8ALKqsi67///iqrP8AGVVU///xVVQIk42u1wUO+2/4RPqtFf8ARKqqi/8APyqq///xqqj/ADmqrP//41VY/wA5qqz//+NVVP8ALCqo///Zqqz/AB6qrFsIi4NLV4OLBW//ACdVVP//3FVU/wAeqqz//9SqrKH//9SqrKH//8+qqpb//8qqqov//8FVVov//82AAP//8FVU///Zqqr//+CqrP//2aqr///gqqz//+zVVf//16qoi///zqqsi///01VU/wAQKqtn/wAgVVX//+SqrP8AIFVW///kqqz/ADGAAP//5Kqo/wBCqqr//+SqrAiT///8qqz/AAxVVv//+1VU/wAQqqqFr33/ACBVVP//8tVU/wAcqqz///OqrP8AHKqs///zqqyp///wgAD/AB9VVP//7VVU/wAfVVT//+1VVv8AGiqs///sKqqgdqB2/wARVVRx/wANqqxs/wANqqxs/wAG1VT//93VVov//9qqqgiL//+pVVb//97VVP//uyqq//+9qqxY//+9qqxY//+sKqj//+aAAP//mqqsizuL//+31Vb/ABCAAP//v6qqrP//v6qurP//y4AA/wAt1VX//9dVUv8AOqqrCIuVyr6ViwX/AByqq///0Kqr/wAnqqr//9pVVf8AMqqrb/8AMqqgb/8AOqqqff8AQqq2i/8AS1VWi/8APSqq/wARVVW6/wAiqqu6/wAiqqv/ABeAAP8ALVVVi8OL/wARVVb///1VVP8AEFVU///6qqz/AA9VVv//+qqs/wAPVVaF/wANgAD///lVVP8AC6qqCP//+VVU/wALqqqAl///8Kqs/wAMVVb///CqrP8ADFVW///zKqj/AAnVVP//9aqs/wAHVVb///WqrP8AB1VW///vgAD/AAkqqv//6VVUlv//6VWUlv//7qqqk///8//CkH+Q///sKqr/AAhVVv//5FVW/wALqqr//+RVVv8AC6ou///sgAD/AAgqqv//9Kqq/wAEqygI///ZVVb/AA9U0Gv/AA5VVP//5qqq/wANVdz//+aqq/8ADVVU///l1VX/ABEqrHCgcKD//+uqq6T///JVVaj///JVVqj///kqqv8AINVUi/8AJKqsi/8ATqqs/wAdgAD/AECAAMb/ADJVVMb/ADJVVP8AS4AA/wAZKqzniwgO/Cn5BecVgI8Fb///7VVW///fVVT///aqqv//2qqsi0v/////////zoAA/wAWKqto/wAsVVZo/wAsVVX//+6AAP8AP9VVi/8AU1VWCPj49+Dh++D32geDkS94i/vN+0aLizX3RouL/PgFi///kqqq/wAa1VX//6oqq/8ANaqr///Bqqv/ADWqqv//waqr/wBHgAD//+DVVf8AWVVWi8WL/wAvqqyY/wAlVVSlCI+UBQ7n+uzbFYONBf//9VVY///1VVZ8///6qqr//+yqqIsI///bVVT//+2qrP8AH1VV/wA+qqsf+fQk/PwHi///nVVWa///rqqqS0tLSztrK4v//56qqov//7KAAP8AHFVV///GVVb/ADiqq///xlVW/wA4qqv//+Mqqv8ATf//i/8AY1VWCPkRJv0ZB4v//4SqqrD//53VVdX//7cAAdVC/wBiVVb//9uAAP8Aeqqqi/8AS1Usi/8ARFVU/wAQgAD/AD1VgKz/AD1VVP8AIP///wAxqqz/AC0qq7H/ADlVVghwB4tb/wAL1VT//9mqqv8AF6qs///jVVb/ABeqrP//41VV/wAh1VT///Gqq7eL/wAiqqiL/wAdVViUo50IkJUFDnfx+q0VZ4ttgnN5CIeBokeTiQX/ABCqqv8ADKqs/wARqqr/AAZVVP8AEqqsi/8AEqqqiZuB/wANVVZ5/wANVVV5m2z/ABKqq18I9/P92sqL+D76jImTK4v7+/32+8P5fQV3u///6Sqr/wAkVVT//+ZVVf8AGKqs///mVVX/ABiqqP//34AA/wAMVVj//9iqq4sIDvhz7/qtFf//31VWi22C///kqqp5CIeBokeViQX/AA6qq/8ADKqs/wARqqv/AAZVVP8AFKqqi5uJ/wAOVVb///aAAP8ADKqqev8ADKqrev8ADlVV///h1VSb///UqqwI98X93sGL97D5/Pex/fzAi/gF+oyJkyaL+7b90fuf+dEti/ue/dH7jPlYBf//7qqr/wAwqqz//+qqqv8AJIAA///mqqv/ABhVVP//5qqr/wAYVVhr/wAMKqj//9lVVYsIDnn3AfqtFf//2qqri///4aqrgv//6KqqeQiHgaJHk4kF/wAQqqr/AAyqrJz/AAZVVP8AEVVWi/8AEqqni/8AEoAAhP8AElVZff8AElVKff8AFdVV///nVVT/ABlVYf//3KqsCPeS+/b8FfyMj4Pvi/fq+Ff3fvvgBf8AJKqsV/8AIFVUZqd1p3X/ACKqrID/AClVVIuvi6mUo50Ij5V0z4ONBf//81VU///1VVZ6///6qqr//+qqrIv//+1VVIv//+2AAP8ABoAA///tqqyY///tqqz/AAz//v//6iqo/wAYKqv//+aqrP8AI1VXCPuS9/b4FfiMh5Mni/vq/FX7fvfeBWe////gVVWw///kqquh///kqquhaJb//9VVVYsIDqL6yfqUFSeL/A/95Pva+WsF///qqqv/ADFVVP//6NVV/wAkqqxyo3Kj///fKquX///XVVWL///dVVSL///iqquC///oAAF5CIeBokeTiQX/AA6qq/8ADKqs/wARqqv/AAZVVP8AFKqqi52J/wAPVVX///ZVVP8ADKqr///uqqz/AAyqq///7qqsm///4Kqo/wATVVX//9KqrAj39f2nT/sVBf//6VVW///NVVH//+cqqv//29VVcP//6lVacP//6lVV///g1Vb///Uqq///3Kqqi///4Kqqi23/AAmqq///41VW/wATVVUIg4ZqRo+FBf8AI1VV///nVVb/ACuqq///86qqv4vFi73/AA+AALWq/wAp//6q/wAlqqr/ADQqqv8AIVVY/wBJVVYI+If69AUO+zz3Tt8V+R75+IvT/XaLizf4+Yv9Hv32i0H5v4uL3wUO/JT3XfjsFamL/wAWKqv/ABSqrP8ADlVV/wApVVT/AA5VVv8AKVUo/wAHKqr/AENVVIv/AF1VhAj3hgeL/wBmqhD/AA1VVv8ARKqo/wAaqqr/ACKrSP8AGqqo/wAiqqj/ADSqqv8AEVVY/wBOqq6LCLLhYgb//5Cqtov//7KqqnL//9SqoFn//9Sqq1n//+pVVf//plVYi///fqqoCPuzB4v//+dVVP///9VV///tqqz///+qq3////+qq3////8qqv//8Sqs///+qqv//+5VVP///qqr///uVVT///3VVX6I///3qqyI///3qqz///vVVf//9qqo///6qqv///WqrP//+qqr///1qqz///lVVf//+Kqog///+6qsg///+6qsgf///Cqof////KqsCH////yqrH3///5VVHuLCD4Hm4uZ///+VVSX///8qqyX///8qqyV///8KqiT///7qqyT///7qqz/AAaqq///+Kqq/wAFVVX///Wqqv8ABVVV///1qyT/AAQqq///9qqqjv//96oyjv//96qq/wACKqt+/wABVVX//+5VVv8AAVPg///uVVb/AADVVf//8Sqq/wAAVst/CP8AAFVVf/8AACqr///tqqqL///nVVYI+7MHi///fqqr/wAVqqv//6ZVVf8AK1VVWf8AK1VWWf8ATVVUcv8Ab1VWiwi04WQG//+xVVaL///LVVT/ABFVVf//5VVW/wAiqqv//+VVVv8AIqqr///yqqr/AESqq4v/AGaqqgj3hgeL/wBcqp7///jVVv8AQyqq///xqqr/ACmquP//8aqr/wApqqz//+nVVf8AFNVUbYsIDv029zr7vxXjHAbVMwYO/JT3ufn0FYv//6KqrP8AByqq//+8qqj/AA5VVv//1qqs/wAOVVb//9aqrP8AFiqq///rVVSpiwhaB22L///p1Vb//+sqrP//8aqq///WVVT///Gqqv//1lVW///41Vb//7zVVIv//6NVVgj7hgeL//+ZVVb///Kqqv//u1VV///lVVb//91VVf//5VVZ///dVVVW///uqqv//7Cqp4sIZDW0Bv8Ab1VWi/8ATVVUpP8AK1VWvf8AK1VWvf8AFaqq/wBZqquL/wCBVVUI97MHi6f/AAAqqv8AFSqq/wAAVVb/AA5VVv8AAFVW/wAOVVb/AAFVVP8AEIAA/wACVVb/ABKqqv8AAlVW/wASqqr/AAOAAP8ADdVW/wAEqqqU/wAEqp6U/wAGqqqU/wAIqriU/wAIqqqU/wAK1Vb/AAYqrJj/AANVVJj/AANVVP8AD9VW/wABqqz/ABKqqosI2Af//+1VVov///Aqqv8AAaqsfv8AA1VUfv8AA1VU///1Kqr/AAYqrP//91VWlP//91VWlP//+VVUlP//+1VWlP//+1VWlP///IAA/wAN1VT///2qqv8AEqqs///9rcD/ABKqrP///qqq/wAQgAD///+nlv8ADlVU////qqr/AA5VVP///9VW/wAVKqyLpwj3sweL/wCBVVj//+pVVv8AWaqo///Uqqq9///Uqq69//+yqquk//+QqqeLCGI1sgb/AE9VVov/ADT/////7qqo/wAaqqv//91VWP8AGqqq///dVVj/AA1VVv//u1VQi///mVVYCA7n+dr43BX/AB1VVIv/ABmqrP8AAlVUof8ABKqsof8ABKqs/wATKqz/AAeAAP8AEFVU/wAKVVT/ABBVVP8AClQc/wAMKqz/AAjVVJP/AAdWkP8AB/4E/wAHVVT/AApVVP8ACqqs/wAMrKiZCIuTWM+DiwX//+CqrFv//9BVVHNLi///z1WEi///sVVUl///k1Uoo///k1VWo///rVVUl///x1VWi///21VWi///34AAhv//46qqgf//46qrgXb///VVVP//8lVV///0qqz///JVVf//9Kqs///xgAD///FVVP//8KqreQiLhb5IkYsF/wANVVX/ABSqrP8AFIAAnP8AG6qr/wANVVT/ABuqqv8ADVVU/wAcgAD/AAaqrP8AHVVWi/8ANqqqi/8AUIAA///0Kqz/AGpVVv//6FVU/wBqVSj//+hVVP8AUNVU///0Kqz/ADdVhIsIDvzNDsv5EfrsFf8Ajqqsi/8AdVVU///JVVjn//+SqqgIk4vLvouUBf//1VVU/wA2qqj//8mAAP8ALNVY//+9qqyu//+9qqyu//+21VT/ABPVWDv/AASqqAj3Ki/7Kgf//3CqrP//9KtA//+Kf/7//8gqqP//pFVW//+bqhj//6RVVv//m6qs///SKqr//4XVVIv7JP/////++yT/AC3VVv//haqq/wBbqqz//5tVVv8AW6qo//+bVVb/AHWAAP//x////wCPVVj///Sqqwj7Muf3Mgf/AE9VVP8ABKqr1J//AEKqrP8AI1VV/wBCqqz/ACNVTv8ANqqouP8AKqqs/wA2qrIIi5VLvIOLBf//1qqsVf//zVVU///XKqpP///kVVZP///kVVX//76qrP//8iqr//+5VVSL//99VVyLIbX//66qpN///66qrv8AU//y///XVVX/AGmqqv/////9/wB/VWT//////f8AgKqs/wAo1VX/AGqAAP8AUaqu/wBUVVT/AFGqqv8AVFVY/wBogAD/ACoqqP8Af1VWiwgOifkJHATwFf8AcVUki/8AYlVU///Qqqj/AFNViP//oVVYCJOLyMWLkwX//5yqrPcE//+HVVTD+yKL//+MqqyL//+gf/7//91VWP//tFVW//+6qqj//7RVVv//uqs4///aKqr//6GqqIv//4iqIAj7iPsKL/cK/LH7Fy/6Eef9J/ix+Cnn/Cn3igeL/wBbVVj/ABvVVv8AR6qo/wA3qqq//wA3qoy//wBGgACl/wBVVXSLCA73JhwEoBwFLRWJkfsBi/xW/Tr8Vfk6+wmLh4X4kv2U+7WLiz33uYuL+0L7uYuLPfe5i4v7dwX093f3udn7ufdC97nZ+7UGDvv692McBHkV/wAaqquL/wAWqqv/AAlVWP8AEqqq/wASqqj/ABKqqv8AEqmA/wAJVVb/ABaqqIv/ABqr2Iv/ABqqmP//9qqq/wAWqqj//+1VVv8AEqrA///tVVb/ABKqqP//6VVV/wAJVVj//+VVVYv//+aqq4t1///2qqj//+1VVf//7VVY///tVVb//+1VWP//9qqq///pVVCL///lVVgIi///5VVY/wAJVVb//+lVUP8AEqqq///tVVj/ABKqq///7VVYof//9qqo/wAZVVWLCPfTFv8AGqqsi/8AFtVU/wAJVVie/wASqqie/wASqYD/AAmAAP8AFqqoi/8AGqvYi/8AGqqY///2gAD/ABaqqHj/ABKqwHj/ABKqqP//6Sqs/wAJVVj//+VVVIv//+aqqot1///2qqj//+1VVv//7VVY///tVVb//+1VWP//9qqq///pVVCL///lVVgIi///5VVY/wAJVVb//+lVUP8AEqqq///tVVj/ABKqqv//7VVYof//9qqo/wAZVVaLCA74gvmvchX3Fov3Cv8AHtVV9f8APaqr9f8APaqr/wBS1Vj/AFN///8AO6qo/wBpVVb/ADuqqP8AaVVW/wAd1Vj/AHP//ov/AH6qrIv/AF6qrP//7lVY/wBZqqj//9yqqP8AVKqs///cqqj/AFSqrFv/AEkqrP//w1VY/wA9qqj//8NVWP8APaqo//+2qqi8Nf8AJFVYCDX/ACRVWP//pFVU/wASKqj//56qrIspi///o9VU///t1Vj//6mqrP//26qo//+pqqr//9uqqP//toAAWv//w1VW///CVVj//8NVVf//wlVY///QKqv//7bVVGj//6tVVGj//6tViP//7oAA//+mVVSL//+hVSSL//+hVVT/ABGAAP//piqqrv//qwACCK42/wAv1VX//7aqq/8APKqr///CVVX/ADyqqv//wlVV/wBJgABa/wBWVVb//9uqq/8AVlVU///bqqv/AFwqrP//7dVV7YsI3QT7Bov//5iqrKb//6NVVMH//6NVVsH//7eqqv8ASYAAV+hX6HH/AGaAAIv3BIv3BKX/AGaAAL/ov+j/AEhVVv8ASVVY/wBcqqr/ADWqqP8AXKqs/wA1qqj/AGdVVP8AGtVY9waLCP8AVKqsi/8AT9VU///wKqjW///gVVjW///gVVj/AD/VWGD/ADSqqP//yaqo/wA0qWj//8mrKP8AKaqo//+/gAD/AB6r8P//tVTY/wAeqqj//7VVVP8AD1VY//+wqqyLN4v7BP//5iqo//+ZgAD//8xVWC7//8xVWC5D//+2gAD//6OqqFUI//+jqqxV//+ZKqhw//+OqqyLCJf3YRX/AEKqrIv/AD2qqP8ADSqq/wA4qqz/ABpVVv8AOKqo/wAaVVa5/wAkKqr/ACNVWLkIi5FSxIWLBf//xKqs//+vVVb//6qqqP//16qq//+QqqyL//+eqqyL//+zgAD/AB2qqv//yFVU/wA7VVb//8hVlP8AO1VW///kKqr/AEuqqv/////C54v/AFtVJP8AG9VU/wBLVVT/ADeqrP8AO1WI/wA3qqz/ADtVVP8AS9VU/wAdqqzri/8Abqqsi+H//9eqrP8APVVU//+vVVQIkYvEw4uRBf//3Kqo/wAuqqxd/wAkgAD//8dVWP8AGlVU///HVZD/ABpVWP//wlVU/wANKqj//71VHIv//4qqrIv//55VVP//2SqoPf//slVYPf//slVwZP//n9VUi///jVU8i///jKqssv//n3/+2f//slVW2f//slVW/wBhqqz//9kqqv8AdVVUiwgO+1j4XfoTFYuRUcSDi/u/++qLdfe/++qTi8XEi5H7jPe3Bfi/97sVUsSCi/u/++qLdfe/++qUi8TEi5H7jPe394z3tQUO9x/5JRU1+ULhBw74gvmvHAVMFSmL//+j1VT//+3VWP//qaqs///bqqj//6mqqv//26qo//+2gABa///DVVb//8JVWP//w1VV///CVVj//9Aqq///ttVUaP//q1VUaP//q1WI///ugAD//6ZVVIv//6FVJIv//6FVVP8AEYAA//+mKqqu//+rAAKuNv8AL9VV//+2qqv/ADyqq///wlVVCP8APKqq///CVVX/AEmAAFr/AFZVVv//26qr/wBWVVT//9uqq/8AXCqs///t1VXti/cWi/cK/wAe1VX1/wA9qqv1/wA9qqv/AFLVWP8AU3///wA7qqj/AGlVVv8AO6qo/wBpVVb/AB3VWP8Ac//+i/8Afqqsi/8AXqqs///uVVj/AFmqqP//3Kqo/wBUqqwI///cqqj/AFSqrFv/AEkqrP//w1VY/wA9qqj//8NVWP8APaqo//+2qqi8Nf8AJFVYNf8AJFVY//+kVVT/ABIqqP//nqqsiwg5BP8AVKqsi/8AT9VU///wKqjW///gVVjW///gVVj/AD/VWGD/ADSqqP//yaqo/wA0qWj//8mrKP8AKaqo//+/gAD/AB6r8P//tVTY/wAeqqj//7VVVP8AD1VY//+wqqyLN4v7BP//5iqo//+ZgAD//8xVWC7//8xVWC5D//+2gAD//6OqqFUI//+jqqxV//+ZKqhw//+OqqyL+waL//+Yqqym//+jVVTB//+jVVbB//+3qqr/AEmAAFfoV+hx/wBmgACL9wSL9wSl/wBmgAC/6L/o/wBIVVb/AElVWP8AXKqq/wA1qqgI/wBcqqz/ADWqqP8AZ1VU/wAa1Vj3BosI91j+hhXyi/tw+AMF/wBHVVT/AASqrP8ANiqs/wAXKqiw/wApqqyw/wApqqz/ABKAAP8ANSqoi/8AQKqsi/8ATKqs///n1Vj/ADrVVP//z6qotP//z6qstP//uyqo/wAUgAD//6aqrIsI+7n91t/3//c8BsTWFft199T3dQb/ADlU5Iv/ACvVVP//8Sqs/wAeVcj//+JVVP8AHlVU///iVVT/AA8qrP//2YAAi///0Kqsi///0VVU///w1VT//9mqrP//4aqsbf//4aqsbf//1CqofP//xqqsiwgO/KT4NBwFwRX74vuhi4OyWpOL9/b3houTTtcFDvx/96svFY2HBZ+TpI+pi7eLsP//8aqqqf//41VWqf//41VVmv//26qri1+L///JVVb//+uqqv//1FVU///XVVb//99VVv//11VW///fVVZV///vqqr//7yqqov//9dVWYv//9bVVf8AB9VW///WVVL/AA+qqgj//9ZVV/8AD6rC///fgAD/ABQqqv//6Kqp/wAYqpQIi5O8w5OLBf8AKKqr///Sqqq////pVVb/AD9VVYv/ACaqqov/AB+AAP8ACCqq/wAYVVb/ABBVVv8AGFVW/wAQVVb/AAwqqv8AFoAAi/8AHKqqi/8AF1VVgf8AE4AAd/8AD6qrd/8AD6qr///mVVb/AAfVVf//4Kqqi///2Kqyi2T///dVVf//2VVO///uqqsIXqXP9zKLtvOLi2AFDvtY+Ib4/BX7wffqhItSUouF94z7tfuM+7eLhcRSkov3wffqBZH4ABWFi1FSi4X3jPu1+4z7t4uFxVKRi/fB9+qLoQUO+/j4GxwFdRV3i/u1+0+Lg7hUkYv3jPcj94r7I5OLuMKLkwUO/MX3nvr+Ff8ANKqqi/8ALFVW/wARqqiv/wAjVViv/wAjVVid/wAqqqiLvYu9ef8AKoAAZ65nrv//06qq/wARgAD//8tVVotXi1///+6AAGdoZ2h5///VgACLWQiLWZ3//9VVWK///9yqqK///9yqqLf//+5VWL+LCNkEbYv//+eAAP8ACiqoeP8AFFVYeP8AFFVY///2gAD/ABgqqIuni6f/AAlVVaP/ABKqq5//ABKqq5//ABiqqpX/AB6qq4v/AB9VVoukgf8AEqqqd/8AEqqqd/8ACVVWc4tvCItv///2qqr//+fVWP//7VVW///rqqj//+1VVv//66qocv//9dVY///gqqqLCA77pveCHAUvFf//vqqvi1f//+SqqP//2VVR///JVVgIi4OwQZOLBf8AFVVVu7Cj/wA0qquL/wAmqqqL/wA41VZ/1nPWc/8AOdVUf/8AKKqsi/8AQKqsi/8AM6qo/wAbVVj/ACaqrP8ANqqoCIuTZtWDiwX//+iqrFv//9tVVHNZi///3Kqsi///x//+l///s1VWo///s1VWo///xVVUl///11VWiwgO+/AO+CIO+/AO+CIO/OgO/WUO/eEO/eEO/h8O/a8O/ocO9x/5JRU1+ULhBw73H/klFTX5QuEHDvcf+SUVNflC4QcOzfcf+SUVNfoF4QcO+AX3H/klFTUcBKDhBw79NPdd+mMVIgoO/Tr3dxwFdRX//+Sqq4v//+kqqv//9oAA///tqqt4///tqqt4///21VX//+kqqIv//+VVWIt3kf//7dVYl///76qol///760Q/wAPVVX///QqqP8AEqqr///4qEj///6qq///8Kqo///4gAD//+fVWP//8lVVav//8lVfav//7NVV///cKqj//+dVTP//2VVYCIuFwmKViwXt9xy7/wBoVViJ/wBIqqiL/wAcqqj///aqqqP//+1VVv8AE1VY///tVVb/ABNVWP//6P///wAJqqj//+Sqq4sIDv0Z93P3NhX//+Sqq4v//+kqqv//9qqr///tqqv//+1VVf//7aqr///tVVb///bVVf//6VVUi///5VVWi///61VW/wAF1VX//+0qqv8AC6qrev8AC6qrev8ADyqq///0gAD/ABKqq4X///yqq///1VVU///lqqpP///Oqqv//7KqrAiLg8JilYsF/wBhVVb/AIdVVf8AL6qq9In/AEqqq4un///21Vb/ABfVVv//7aqq/wATqqr//+2qqv8AE6qr///pKqv/AAnVVf//5KqriwgO/B/3XfpjFSIK96oW/wAbVVaL/wAW1Vb/AAlVVP8AElVU/wASqqz/ABJVVP8AEqqs/wAJKqz/ABaqrIv/ABqqqIuf///6Kqz/ABIqqP//9FVU/wAQVVj///RV3P8AEFVY///w1VT/AAvVUP//7VTQ/wAHVVj/AAFVVP8AD1VY/wAHgAD/ABgqqP8ADaqsrP8ADaqsrP8AEyqo/wAj1Vj/ABiqrP8AJqqoCIuSVLSAiwX//56qqv//eKqo///QVVb//5dVWI1Bi///41VY/wAJKqr//+gqqP8AElVWeP8AElVWeP8AFtVU///2gAD/ABtVVosIDvwh93ccBXcV///lVVWL///pVVX///aqqP//7VVW///tVVj//+1VVf//7VVY///2qqv//+lVUIv//+VVWIv//+yqqJH//+3VWJd6l3r/AA9VVf//9IAA/wASqquF///8qqv//9VVWHFP///PVVX//7KqqAiLg8JilYsF6/8AhVVYu/SL/wBMqqj///6qqqeB/wAXgAD//+1VVp7//+1VVp7//+j///8ACYAA///kqquLCPerFv//5KrIi///6Sqq///2qqj//+2qjv//7VVY///tqqr//+1VWP//9tVW///pVVCL///lVViL///sqqj/AAXVVv//7dVY/wALqqp6/wALqnR6/wAPKqr///SAAP8AEqrihf///Kqq///Uqqj//+VVVk9Z//+zVVgIi4PDYpWLBf8AYVVU/wCHVVj/AC+qrPSJ/wBKqqiLp///9tVU/wAXgAD//+2qrJ7//+2qrJ7//+kqqP8ACYAA///kqqyLCA78Avdz9zQV///kqquL///pKqr///aAAP//7aqreP//7aqreP//9tVV///pKqqL///lVVaLd/8ABdVV///t1VX/AAuqq///76qr/wALqqv//++qqv8ADyqq///0Kqv/ABKqq///+Kqr///+qqv///Cqq///+Kqq///n1VX///Kqq2r///Kqq2p4///cKqv//+dVVf//2VVVCIuFwmKViwX/AGFVVv8Ah1VV/wAvqqr/AGhVVYn/AElVVov/AByqqv//9tVWo///7aqq/wATVVb//+2qqv8AE1VV///pKqv/AAmqq///5Kqriwj3qxb//+SqyIv//+iqqv//9oAA///sqo54///sqqp4///2VVb//+kqqov//+VVVot3kf//7dVVl///76qrl///76qqm///9Cqrn///+Kqr///+qqr///Cqq///+IAA///n1VX///JVVmr///JVVmr//+zVVP//3Cqr///nVVb//9lVVQiLhcJilosF/wBfVVT3GP8AL6qs/wBoVVaL/wBMqqr///6qrP8AHKqq///2VVSjef8AE1VWef8AE1VV///pqqz/AAmqq///5VVUiwgOcfdtchUhCvfSFv8AGqqsi/8AFqqo/wAJgAD/ABKqrJ7/ABKqrJ7/AAlVVP8AFtVVi/8AGqqri/8AGqqp///2qqz/ABaqq///7VVU/wASqqz//+1VaP8AEqqr///pVVT/AAlVVf//5VVEi///5VVWi///6Sqq///2qqt4///tVVV4///tVVb///aAAP//6VVUi///5VVWCIv//+VVVv8ACYAA///pKqqeeJ54/wAW1Vb///aAAP8AGqqqiwj3zxb/ABqqrIv/ABaqqP8ACYAA/wASqqye/wASqqye/wAJVVT/ABbVVYv/ABqqq4v/ABqqqf//9qqs/wAWqqv//+1VVP8AEqqs///tVjT/ABKqq///6VVU/wAJVVX//+VUeIv//+aqrIt1///2qqv//+1VVP//7VVV///tVVT//+1VVv//9qqs///pVVSL///lVVYIi///5VVW/wAJVVT//+kqqv8AEqqseP8AEqqseKH///aAAP8AGVVUiwgO/a8O/I74W/ohFVPFg4v7v/vqi3b3v/vqk4vDwouU+4z3tPeM97UFDvyO91n6WxWCi1RRi4X3jPu1+4z7tIuCwlSUi/e/9+qLoAUO/WUO+HEcBbr3ghVExIKJBVP//7iqqv//vNVYVP//saqo///ZVVb//7GqqP//2VVW//+rKqz//+yqq///pKqs/////////4CqrIv//42qqP8AJFVW//+aqqz/AEiqqv//mqqy/wBIqqn//7iqqv8AX1VV///WqqT/AHYAAgj5Bouu2YmT/T6LBf//+VVW/wApVQj///yqqv8AJlVUi/8AI1Wki6eN/wAcqqyP/wAdVVQI+TqLrtiHlP1GiwX/ACNVVvcS/wBFVVT/AGYqqP8AZ1VW/wBOVVj/AGdVKP8ATlVY/wB2VVT/ACcqqP8AhVWEi/8AXKqsi/8AVlVUd9tj22P/AEJVWP//yVVY/wA0qqj//7qqqAiUi9K/i5MF///BVVj/AFCqGD3/AD8qqP//oqqo/wAtq0D//6KqqP8ALaqoJf8AFtVY//+RVViL+zaL//9xgAD//8/VWPsP//+fqqj7D///n6qo//+v1Vb//4OAAP//2qqq//9nVVgI+xeLaD2Ng/coiwX///1VVf//2VWs///+qqv//+NVVIv//+1VAItf/wACqqv//9mqrP8ABVVV///fVVQI+ySLaT2Pg/dWiwX/ACqqoP//bgAE/wBRqqr//4nVVf8AeKq2//+lqqf/AHiqrP//paqq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ABP/kQAU/6gAGP+HADAAEP4OABD+DgAQ/g4AEP4OABD+DgAQ/g4AEf/RABH/0QAR/9EAEf/RABH/0QAR/9EAFf9vABX/bwAV/28AFf9vABX/bwAV/28AF/+WABf/lgAX/5YAF/+WABf/lgAX/5YAGf/PABn/zwAZ/88AGf/PABn/zwAZ/88AK//PACv/zwAr/88AK//PACv/zwAr/88ALv/dAC7/3QAu/90ALv/dAC7/3QAu/90AWf/uAFn/7gBZ/+4AWf/uAFn/7gBZ/+4AQgAK/8kACv/JAAr/yQAK/8kACv/JAAr/yQAQ/9EAEP/RABD/0QAQ/9EAEP/RABD/0QAS/+cAEv/nABL/5wAS/+cAEv/nABL/5wAT/+cAE//nABP/5wAT/+cAE//nABP/5wAU//AAFP/wABT/8AAU//AAFP/wABT/8AAY/9sAGP/bABj/2wAY/9sAGP/bABj/2wAr/90AK//dACv/3QAr/90AK//dACv/3QA5/9kAOf/ZADn/2QA5/9kAOf/ZADn/2QA9/9EAPf/RAD3/0QA9/9EAPf/RAD3/0QA+/9kAPv/ZAD7/2QA+/9kAPv/ZAD7/2QBe/8sAXv/LAF7/ywBe/8sAXv/LAF7/ywASAAz/2wAM/9sADP/bAAz/2wAM/9sADP/bABX/2wAV/9sAFf/bABX/2wAV/9sAFf/bABf/9gAX//YAF//2ABf/9gAX//YAF//2AB4ACv/bAAr/2wAK/9sACv/bAAr/2wAK/9sAEv/4ABL/+AAS//gAEv/4ABL/+AAS//gAGP/6ABj/+gAY//oAGP/6ABj/+gAY//oAPv/0AD7/9AA+//QAPv/0AD7/9AA+//QAXv/ZAF7/2QBe/9kAXv/ZAF7/2QBe/9kAQgAK/9UACv/VAAr/1QAK/9UACv/VAAr/1QAS/+cAEv/nABL/5wAS/+cAEv/nABL/5wAT/+kAE//pABP/6QAT/+kAE//pABP/6QAU//oAFP/6ABT/+gAU//oAFP/6ABT/+gAY/+4AGP/uABj/7gAY/+4AGP/uABj/7gAa//AAGv/wABr/8AAa//AAGv/wABr/8AAr//AAK//wACv/8AAr//AAK//wACv/8AA5/+4AOf/uADn/7gA5/+4AOf/uADn/7gA9/+EAPf/hAD3/4QA9/+EAPf/hAD3/4QA+/+4APv/uAD7/7gA+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"
PHOTO_DATA = "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"

ICON_DATA = "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"


# --- FASTQ PREPROCESSOR LOGIC ---


def load_preprocessed(input_path: str, output_path: str, min_quality: int, trim_ends: int, 
                      max_reads: int, reverse: bool, cancel_event=None):
    """
    Reads a FASTQ file, filters by quality and length, trims ends, optionally generates reverse complement,
    and writes to output FASTA and FASTQ formats.
    """
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        # Determine base path for outputs
        base_path = os.path.splitext(output_path)[0]
        fasta_path = base_path + ".fasta"
        fastq_path = base_path + ".fastq"
        
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f_in, \
             open(fasta_path, 'w', encoding='utf-8') as f_fasta, \
             open(fastq_path, 'w', encoding='utf-8') as f_fastq:
            
            max_counter = 0
            
            while True:
                if cancel_event and cancel_event.is_set():
                    break
                    
                header = f_in.readline().strip()
                if not header: break
                
                # Input FASTQ Header usually starts with @. For output we need a clean ID.
                seq_id = header[1:] if header.startswith('@') else header
                
                seq = f_in.readline().strip()
                plus = f_in.readline()
                qual = f_in.readline().strip()
                
                if not qual: break 
                
                if len(seq) > 55:
                    if average_quality(qual) > min_quality:
                        
                        trimmed_seq = seq[trim_ends : len(seq) - trim_ends]
                        # Trim quality too for FASTQ output consistency
                        trimmed_qual = qual[trim_ends : len(qual) - trim_ends]
                        
                        if len(trimmed_seq) > 0:
                            # Write FASTA
                            f_fasta.write(f">{seq_id}\n{trimmed_seq}\n")
                            
                            # Write FASTQ
                            f_fastq.write(f"@{seq_id}\n{trimmed_seq}\n+\n{trimmed_qual}\n")
                            
                            if reverse:
                                rc_seq = reverse_complement(trimmed_seq)
                                # Reverse quality for RC? usually yes.
                                rc_qual = trimmed_qual[::-1]
                                
                                f_fasta.write(f">{seq_id}_RC\n{rc_seq}\n")
                                f_fastq.write(f"@{seq_id}_RC\n{rc_seq}\n+\n{rc_qual}\n")
                            
                            max_counter += 1
                
                if max_counter >= max_reads:
                    break
                    
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        raise e

def convert_quality_string(quality_string: str):
    # Phred+33
    return [ord(c) - 33 for c in quality_string]

def average_quality(quality_string: str) -> float:
    try:
        qualities = convert_quality_string(quality_string)
        if not qualities: return 0.0
        return sum(qualities) / len(qualities)
    except Exception:
        return 0.0

def reverse_complement(dna_sequence: str) -> str:
    if not dna_sequence: return ""
    
    mapping = {
        'A': 'T', 'a': 't',
        'T': 'A', 't': 'a',
        'C': 'G', 'c': 'g',
        'G': 'C', 'g': 'c'
    }
    
    # Efficient builder
    cmp_list = []
    # Reverse iteration
    for base in reversed(dna_sequence):
        cmp_list.append(mapping.get(base, 'N'))
        
    return "".join(cmp_list)

# --- ASSEMBLER LOGIC ---


class Node:
    __slots__ = ['sequence', 'in_nodes', 'out_nodes']
    
    def __init__(self, kmer: str):
        self.sequence = kmer
        self.in_nodes = set()
        self.out_nodes = set()
        
    def get_first_kmer(self, kmer_size: int):
        return self.sequence[:min(len(self.sequence), kmer_size)]
        
    def in_degree(self):
        return len(self.in_nodes)
        
    def out_degree(self):
        return len(self.out_nodes)
        
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.sequence == other.sequence
        
    def __hash__(self):
        return hash(self.sequence)

class DeBruijnGraph:
    def __init__(self):
        self.nodes = {}  # Map<String, Node>

    def get_or_create_node(self, kmer: str):
        if kmer not in self.nodes:
            self.nodes[kmer] = Node(kmer)
        return self.nodes[kmer]

    def add_edge(self, source_kmer: str, dest_kmer: str):
        source = self.get_or_create_node(source_kmer)
        dest = self.get_or_create_node(dest_kmer)
        source.out_nodes.add(dest)
        dest.in_nodes.add(source)

    def merge_nodes(self, node_a: Node, node_b: Node, kmer_size: int):
        # node_a -> node_b
        # Python substring: s[start:] (inclusive)
        # Java: substring(kmerSize - 1)
        suffix = node_b.sequence[kmer_size - 1:]
        node_a.sequence += suffix
        
        # Update edges
        # Start with a copy of node_b.out_nodes because we modify the set during iteration? No, we modify downstream.
        node_a.out_nodes = set(node_b.out_nodes)
        
        for downstream_node in node_a.out_nodes:
            if node_b in downstream_node.in_nodes:
                downstream_node.in_nodes.remove(node_b)
            downstream_node.in_nodes.add(node_a)
            
        # Remove node_b from graph dictionary using its k-mer key
        b_key = node_b.get_first_kmer(kmer_size)
        if b_key in self.nodes:
            del self.nodes[b_key]

    def remove_node(self, node: Node, kmer_size: int):
        key = node.get_first_kmer(kmer_size)
        if key in self.nodes:
            del self.nodes[key]
            
        for prev in node.in_nodes:
            if node in prev.out_nodes:
                prev.out_nodes.remove(node)
                
        for next_node in node.out_nodes:
            if node in next_node.in_nodes:
                next_node.in_nodes.remove(node)


def count_kmers(sequences, k):
    kmer_counts = Counter()
    for seq in sequences:
        if len(seq) >= k:
            for i in range(len(seq) - k + 1):
                kmer = seq[i : i+k]
                kmer_counts[kmer] += 1
    return kmer_counts

def build_graph(sequences, kmer_counts, k, min_freq):
    graph = DeBruijnGraph()
    for seq in sequences:
        if len(seq) > k:
            for i in range(len(seq) - k):
                kmer1 = seq[i : i+k]
                kmer2 = seq[i+1 : i+1+k]
                
                c1 = kmer_counts.get(kmer1, 0)
                c2 = kmer_counts.get(kmer2, 0)
                
                if c1 >= min_freq and c2 >= min_freq:
                    graph.add_edge(kmer1, kmer2)
    return graph

# Simplification Logic

def compact_paths(graph, kmer_size):
    changed = False
    # Create a list of keys to avoid modification during iteration issues
    node_keys = list(graph.nodes.keys())
    
    for key in node_keys:
        if key not in graph.nodes: continue
        node = graph.nodes[key]
        
        if node.out_degree() == 1:
            # We fetch the *only* out node
            # Since out_nodes is a set, we convert to list
            next_node = list(node.out_nodes)[0]
            
            if next_node != node and next_node.in_degree() == 1:
                graph.merge_nodes(node, next_node, kmer_size)
                changed = True
                
    return changed

def remove_tips(graph, kmer_size, tip_threshold_factor):
    changed = False
    nodes = list(graph.nodes.values())
    tips = [n for n in nodes if n.in_degree() == 0 or n.out_degree() == 0]
    
    threshold = kmer_size * tip_threshold_factor
    
    for tip in tips:
        # Check if tip still exists in graph (might have been removed)
        key = tip.get_first_kmer(kmer_size)
        if key in graph.nodes and len(tip.sequence) < threshold:
            graph.remove_node(tip, kmer_size)
            changed = True
            
    return changed

def calculate_path_coverage(path, kmer_counts, kmer_size):
    if not path or len(path) <= 1: return 0.0
    
    total_cov = 0
    node_count = 0
    
    for i in range(len(path) - 1):
        kmer = path[i].get_first_kmer(kmer_size)
        total_cov += kmer_counts.get(kmer, 0)
        node_count += 1
        
    return total_cov / node_count if node_count > 0 else 0.0

def pop_bubbles(graph, kmer_counts, kmer_size, max_bubble_path_len, bubble_cov_ratio):
    changed = False
    potential_starts = [n for n in graph.nodes.values() if n.out_degree() >= 2]
    
    for start_node in potential_starts:
        if find_and_resolve_bubble(start_node, graph, kmer_counts, kmer_size, max_bubble_path_len, bubble_cov_ratio):
            changed = True
            
    return changed

def find_and_resolve_bubble(start_node, graph, kmer_counts, kmer_size, max_len, ratio):
    key = start_node.get_first_kmer(kmer_size)
    if key not in graph.nodes or start_node.out_degree() < 2: return False
    
    paths = []
    
    # Explore paths
    for path_start in list(start_node.out_nodes):
        current_path = []
        current_node = path_start
        current_len = 0
        
        while current_node.in_degree() == 1 and current_len < max_len:
            current_path.append(current_node)
            current_len += len(current_node.sequence) - kmer_size + 1
            if current_node.out_degree() != 1: break
            # Get next
            if len(current_node.out_nodes) > 0:
                current_node = list(current_node.out_nodes)[0]
            else:
                break
        
        if current_node.in_degree() > 1 and current_path:
            current_path.append(current_node)
            paths.append(current_path)
            
    # Group by end node
    bubbles = defaultdict(list)
    for p in paths:
        if p:
            end_node = p[-1]
            bubbles[end_node].append(p)
            
    popped = False
    
    for end_node, bubble_paths in bubbles.items():
        if len(bubble_paths) > 1:
            # Sort by coverage descending
            bubble_paths.sort(key=lambda p: calculate_path_coverage(p, kmer_counts, kmer_size), reverse=True)
            
            best_path = bubble_paths[0]
            best_cov = calculate_path_coverage(best_path, kmer_counts, kmer_size)
            
            # Others are candidates for removal
            for i in range(1, len(bubble_paths)):
                loser_path = bubble_paths[i]
                loser_cov = calculate_path_coverage(loser_path, kmer_counts, kmer_size)
                
                if best_cov > loser_cov * ratio and loser_cov > 0:
                    # Remove nodes in loser path (except the last one which is the merge point)
                    # The last node is `end_node`, shared.
                    # The `start_node` is shared but not in `loser_path` list (we started from its children)
                    
                    # Graph.removeNode logic from Java:
                    # graph.removeNode(loserPath.get(j), kmerSize);
                    # Iterate to size - 1 (exclusive of last strict node)
                    
                    for j in range(len(loser_path) - 1):
                        node_to_remove = loser_path[j]
                        graph.remove_node(node_to_remove, kmer_size)
                        
                    popped = True
                    
    return popped


def simplify(graph, kmer_counts, kmer_size, tip_factor, max_bubble, bubble_ratio):
    if not graph.nodes: return
    pass_count = 0
    changed = True
    
    while changed and pass_count < 10:
        pass_count += 1
        changed = False
        c = compact_paths(graph, kmer_size)
        b = pop_bubbles(graph, kmer_counts, kmer_size, max_bubble, bubble_ratio)
        t = remove_tips(graph, kmer_size, tip_factor)
        if c or b or t:
            changed = True

def load_reads(path, cancel_event=None):
    print(f"Loading reads from {path}...")
    reads = []
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if cancel_event and cancel_event.is_set(): break
                l = line.strip()
                if l and all(c.upper() in 'ACGTN' for c in l):
                    reads.append(l.upper())
    except Exception as e:
        print(f"Error loading reads: {e}")
    return reads

def save_contigs(contigs, path, min_len, cancel_event=None):
    print(f"Saving contigs to {path}...")
    # Sort by length desc
    contigs.sort(key=len, reverse=True)
    count = 0
    
    try:
        with open(path, 'w') as f:
            line_width = 80
            for contig in contigs:
                if cancel_event and cancel_event.is_set(): break
                
                if len(contig) < min_len: continue
                
                count += 1
                f.write(f">Contig_{count}_length_{len(contig)}\n")
                for j in range(0, len(contig), line_width):
                    f.write(contig[j : j+line_width] + "\n")
                    
        print(f"Saved {count} contigs.")
    except Exception as e:
        print(f"Error saving contigs: {e}")

def run_assembly(input_file, output_file, kmer_sizes_str, min_kmer_freq, min_contig_len,
                tip_factor, max_bubble, bubble_ratio, cancel_event=None):
    
    try:
        kmer_sizes = [int(x) for x in kmer_sizes_str.split(';')]
        print(f"K-mer sizes: {kmer_sizes}")
        
        initial_reads = load_reads(input_file, cancel_event)
        current_input = list(initial_reads)
        final_contigs = []
        
        for k in kmer_sizes:
            if cancel_event and cancel_event.is_set(): break
            
            print(f"Assembling K={k} with {len(current_input)} input sequences.")
            
            counts = count_kmers(current_input, k)
            graph = build_graph(current_input, counts, k, min_kmer_freq)
            simplify(graph, counts, k, tip_factor, max_bubble, bubble_ratio)
            
            # Generate contigs
            generated = [n.sequence for n in graph.nodes.values()]
            print(f"Generated {len(generated)} contigs for K={k}")
            
            current_input = list(initial_reads) + generated
            final_contigs = generated
            
        save_contigs(final_contigs, output_file, min_contig_len, cancel_event)
        
    except Exception as e:
        print(f"Assembly error: {e}")
        raise e

# --- CLASSIFIER LOGIC ---


BLAST_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

def classify_sequences(input_fasta, output_file, mode='nt', cancel_event=None):
    """
    Classifies sequences using NCBI BLAST.
    mode: 'nt' (blastn/nt) or 'p' (blastp/nr)
    """
    
    # Determine parameters based on mode
    program = 'blastn' if mode == 'nt' else 'blastp'
    database = 'nt' if mode == 'nt' else 'nr'
    
    print(f"Starting classification ({program}/{database})...")
    
    sequences = read_fasta(input_fasta)
    print(f"Read {len(sequences)} sequences.")
    
    output_unclassified = output_file.rsplit('.', 1)[0] + "_no_identificados.fasta"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f_out, \
             open(output_unclassified, 'w', encoding='utf-8') as f_un:
            
            # Header
            header_cols = ["ID_SECUENCIA", "DESCRIPCION", "SCIENTIFIC_NAME", "ACCESSION", 
                          "QUERY_COVER", "E_VALUE", "PERCENT_IDENTITY", "MAX_SCORE", 
                          "TOTAL_SCORE", "ACC_LEN"]
            f_out.write("\t".join(header_cols) + "\n")
            
            for seq_id, seq_data in sequences.items():
                if cancel_event and cancel_event.is_set(): break
                
                print(f"\nProcessing: {seq_id}")
                full_header = seq_data['header']
                sequence = seq_data['sequence']
                
                # 1. TIMEOUT / RID RETRIEVAL
                rid = start_blast(program, database, sequence)
                if not rid:
                    handle_error(f_out, f_un, seq_id, "ERROR_NO_RID", full_header, sequence)
                    continue
                    
                print(f"  -> RID: {rid}. Waiting...")
                
                # 2. POLL FOR COMPLETION
                if not wait_for_results(rid, cancel_event):
                    handle_error(f_out, f_un, seq_id, "TIMEOUT_OR_FAILED", full_header, sequence)
                    continue
                    
                # 3. GET XML RESULTS
                print("  -> Fetching XML...")
                xml_content = get_results_xml(rid)
                
                # 4. PARSE XML
                result = parse_blast_xml(xml_content)
                
                if not result['classified']:
                    print("  -> No significant hits.")
                    write_result(f_out, seq_id, result)
                    write_fasta(f_un, full_header, sequence)
                else:
                    print(f"  -> Match: {result['description']} (Acc: {result['accession']})")
                    write_result(f_out, seq_id, result)
                
                # Respectful delay
                time.sleep(1)
                
    except Exception as e:
        print(f"Classification error: {e}")
        raise e

def read_fasta(path):
    seqs = OrderedDict()
    current_header = None
    current_seq = []
    
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                if line.startswith(">"):
                    if current_header:
                        # Store previous
                        seq_id = current_header.split()[0][1:] # Remove > and take first word
                        seqs[seq_id] = {'header': current_header, 'sequence': "".join(current_seq)}
                    
                    current_header = line
                    current_seq = []
                else:
                    current_seq.append(line)
            
            # Last one
            if current_header:
                seq_id = current_header.split()[0][1:]
                seqs[seq_id] = {'header': current_header, 'sequence': "".join(current_seq)}
                
    except Exception as e:
        print(f"Error reading FASTA: {e}")
        
    return seqs

def write_fasta(f, header, seq):
    f.write(f"{header}\n")
    for i in range(0, len(seq), 60):
        f.write(seq[i:i+60] + "\n")

def write_result(f, seq_id, res):
    # Order matches header
    row = [
        seq_id,
        res.get('description', 'N/A'),
        res.get('scientific_name', 'N/A'),
        res.get('accession', 'N/A'),
        str(res.get('query_cover', 'N/A')),
        str(res.get('e_value', 'N/A')),
        str(res.get('percent_identity', 'N/A')),
        str(res.get('max_score', 'N/A')),
        str(res.get('total_score', 'N/A')),
        str(res.get('accession_len', 'N/A'))
    ]
    f.write("\t".join(row) + "\n")

def handle_error(f_out, f_un, seq_id, msg, header, seq):
    print(f"  -> Error: {msg}")
    # Write empty result line with error msg in description
    res = {'classified': False, 'description': msg}
    write_result(f_out, seq_id, res)
    write_fasta(f_un, header, seq)

def start_blast(program, database, sequence):
    params = {
        'CMD': 'Put',
        'PROGRAM': program,
        'DATABASE': database,
        'QUERY': sequence
    }
    try:
        resp = requests.post(BLAST_URL, data=params)
        resp.raise_for_status()
        
        # Parse RID from HTML response (standard Put response is HTML)
        # Look for <input name="RID" value="..." /> or similar, 
        # but often it's in a comment or plain text: "RID = ..."
        # Java uses: name="RID" value="...
        
        content = resp.text
        marker = 'name="RID" value="'
        start = content.find(marker)
        if start != -1:
            start += len(marker)
            end = content.find('"', start)
            if end != -1:
                return content[start:end]
                
        # Alternative search
        if "RID =" in content:
            # QBlast Info often has RID = XXXXX
            import re
            m = re.search(r'RID\s*=\s*([A-Z0-9]+)', content)
            if m: return m.group(1)
            
        return None
        
    except Exception as e:
        print(f"Request error: {e}")
        return None

def wait_for_results(rid, cancel_event):
    for _ in range(60): # 60 attempts * 5s = 5 mins max wait
        if cancel_event and cancel_event.is_set(): return False
        
        params = {
            'CMD': 'Get',
            'FORMAT_OBJECT': 'SearchInfo',
            'RID': rid
        }
        try:
            resp = requests.get(BLAST_URL, params=params)
            content = resp.text
            
            if 'Status=READY' in content:
                return True
            if 'Status=FAILED' in content or 'Status=UNKNOWN' in content:
                return False
                
            time.sleep(5)
            
        except Exception:
            return False
            
    return False

def get_results_xml(rid):
    params = {
        'CMD': 'Get',
        'RID': rid,
        'FORMAT_TYPE': 'XML'
    }
    resp = requests.get(BLAST_URL, params=params)
    return resp.text

def parse_blast_xml(xml_content):
    result = {
        'classified': False,
        'description': 'NO_CLASIFICADA',
        'scientific_name': 'N/A',
        'accession': 'N/A',
        'query_cover': 'N/A',
        'e_value': 'N/A',
        'percent_identity': 'N/A',
        'max_score': 'N/A',
        'total_score': 'N/A',
        'accession_len': 'N/A'
    }
    
    try:
        root = ET.fromstring(xml_content)
        # BlastOutput -> BlastOutput_iterations -> Iteration -> Iteration_hits -> Hit
        
        # Check query len
        query_len = 0
        try:
            query_len = int(root.find(".//Iteration_query-len").text)
        except: pass
        
        hits = root.findall(".//Hit")
        if not hits:
            return result
        
        # Take best hit (first one)
        hit = hits[0]
        
        result['classified'] = True
        result['description'] = hit.find("Hit_def").text
        result['accession'] = hit.find("Hit_accession").text
        result['accession_len'] = hit.find("Hit_len").text
        
        # Scientific name is often part of Hit_def in brackets [Name]
        import re
        m = re.search(r'\[(.*?)\]', result['description'])
        if m:
            result['scientific_name'] = m.group(1)
        
        # HSP details (First HSP of first Hit)
        hsps = hit.findall("Hit_hsps/Hsp")
        if hsps:
            hsp = hsps[0]
            result['max_score'] = hsp.find("Hsp_bit-score").text
            result['total_score'] = result['max_score'] # Approximation
            result['e_value'] = hsp.find("Hsp_evalue").text
            
            identity = int(hsp.find("Hsp_identity").text)
            align_len = int(hsp.find("Hsp_align-len").text)
            
            if align_len > 0:
                result['percent_identity'] = f"{(identity/align_len)*100:.2f}%"
            
            if query_len > 0:
                result['query_cover'] = f"{(align_len/query_len)*100:.0f}%"

    except Exception as e:
        print(f"XML Parse error: {e}")
        
    return result

# --- GUI Logic ---





# Logic Imports

# --- Color Palette (Placeholder - Replace with OneResearchHub colors) ---
COLORS = {
    "bg_dark": "#1e293b",       # Dark Slate Blue/Grey
    "bg_medium": "#334155",
    "bg_light": "#cbd5e1",
    "primary": "#0ea5e9",       # Sky Blue
    "primary_hover": "#0284c7",
    "secondary": "#64748b",
    "text_light": "#f1f5f9",
    "text_dark": "#0f172a",
    "success": "#22c55e",       # Green
    "danger": "#ef4444",        # Red
    "warning": "#eab308"        # Yellow
}

def get_stylesheet(font_family="Segoe UI"):
    return f"""
QMainWindow {{
    background-color: {COLORS['bg_dark']};
}}
QWidget {{
    color: {COLORS['text_light']};
    font-family: '{font_family}', sans-serif;
    font-size: 14px;
}}
QGroupBox {{
    border: 1px solid {COLORS['secondary']};
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
    color: {COLORS['primary']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}}
QLineEdit {{
    background-color: {COLORS['bg_medium']};
    border: 1px solid {COLORS['secondary']};
    border-radius: 4px;
    padding: 5px;
    color: {COLORS['text_light']};
}}
QLineEdit:focus {{
    border: 1px solid {COLORS['primary']};
}}
QComboBox {{
    background-color: {COLORS['bg_medium']};
    border: 1px solid {COLORS['secondary']};
    border-radius: 4px;
    padding: 5px;
    color: {COLORS['text_light']};
}}
QComboBox::drop-down {{
    border: none;
}}
QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLORS['primary_hover']};
}}
QPushButton:disabled {{
    background-color: {COLORS['secondary']};
    color: #94a3b8;
}}
QPushButton#cancel_btn {{
    background-color: {COLORS['danger']};
}}
QPushButton#cancel_btn:hover {{
    background-color: #dc2626;
}}
QPushButton#save_btn {{
    background-color: {COLORS['success']};
}}
QPushButton#save_btn:hover {{
    background-color: #16a34a;
}}
QScrollArea {{
    border: none;
    background-color: transparent;
}}
"""

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result_ready = pyqtSignal(dict) # To pass back file paths

class Worker(QThread):
    def __init__(self, mode, inp, out, params):
        super().__init__()
        self.mode = mode
        self.inp = inp
        self.out = out
        self.params = params
        self.signals = WorkerSignals()
        self.cancel_event = threading.Event()
        self.generated_files = {}

    def run(self):
        try:
            os.makedirs(os.path.dirname(self.out), exist_ok=True)
            self.generated_files = {}

            if self.mode == "Preprocess FASTQ":
                load_preprocessed(self.inp, self.out, self.params['min_qual'], 
                                                     self.params['trim_ends'], self.params['max_reads'], 
                                                     self.params['reverse'], self.cancel_event)
                if not self.cancel_event.is_set():
                    base = os.path.splitext(self.out)[0]
                    self.generated_files['fasta'] = base + ".fasta"
                    self.generated_files['fastq'] = base + ".fastq"

            elif self.mode == "Assemble":
                out_asm = self.out + ".fasta"
                run_assembly(self.inp, out_asm, self.params['kmers'], self.params['min_kfreq'], 
                                       self.params['min_contig'], self.params['tip_thres'], 
                                       self.params['max_bubble'], self.params['bubble_cov'], self.cancel_event)
                if not self.cancel_event.is_set():
                    self.generated_files['fasta'] = out_asm

            elif "Classify" in self.mode:
                out_cls = self.out + ".txt"
                classify_sequences(self.inp, out_cls, mode=('nt' if 'nt' in self.mode else 'p'), 
                                              cancel_event=self.cancel_event)
                if not self.cancel_event.is_set():
                    self.generated_files['txt'] = out_cls
                    self.generated_files['fasta'] = out_cls.rsplit('.', 1)[0] + "_no_identificados.fasta"

            if not self.cancel_event.is_set():
                self.signals.result_ready.emit(self.generated_files)
                self.signals.finished.emit()
            else:
                self.signals.error.emit("Operation cancelled by user.")

        except Exception as e:
            self.signals.error.emit(str(e))

    def cancel(self):
        self.cancel_event.set()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SeqAnalysis")
        # Dynamic sizing to fit within screen space
        screen = QApplication.primaryScreen().availableGeometry()
        width = min(1000, screen.width() * 0.95)
        height = min(750, screen.height() * 0.95)
        self.resize(int(width), int(height))
        self.setMinimumSize(800, 600)

        # Center on screen
        qr = self.frameGeometry()
        cp = screen.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # Set Icon
        if 'ICON_DATA' in globals():
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(ICON_DATA))
            self.setWindowIcon(QIcon(pixmap))
        else:
            self.setWindowIcon(QIcon("icon.ico"))
        # Stylesheet is managed by QApplication now

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # Temp path
        self.temp_output_base = os.path.join(os.getcwd(), "temp_seqanalysis", "result")
        self.generated_files = {}
        self.last_mode = ""
        self.title_label = None # To hold ref

        self.setup_ui()

    def setup_ui(self):
        # Use a scroll area for the main content to handle small screens
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("MainScrollArea")
        self.scroll_area.setStyleSheet("#MainScrollArea { background: transparent; border: none; }")
        self.scroll_area.viewport().setStyleSheet("background: transparent; border: none;")
        
        content_wrapper = QWidget()
        content_wrapper_layout = QVBoxLayout(content_wrapper)
        content_wrapper_layout.setContentsMargins(20, 20, 20, 20)
        content_wrapper_layout.setSpacing(20)

        # Header
        title = QLabel("SeqAnalysis")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold)) # Default fallback
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['primary']}; margin-bottom: 5px;")
        content_wrapper_layout.addWidget(title)
        self.title_label = title

        # Description
        desc_label = QLabel("Comprehensive Sequence Analysis Tool for Quality Control, Assembly, and Classification")
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet(f"color: {COLORS['text_light']}; margin-bottom: 15px;")
        content_wrapper_layout.addWidget(desc_label)

        # Content Area (Horizontal Layout for Landscape)
        content_layout = QHBoxLayout()
        
        # Left: Input Section
        input_group = QGroupBox("Input Configuration")
        input_layout = QVBoxLayout()
        
        file_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Select input file...")
        self.input_path.setReadOnly(True)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_input_file)
        
        file_layout.addWidget(self.input_path)
        file_layout.addWidget(browse_btn)
        
        input_layout.addLayout(file_layout)
        input_group.setLayout(input_layout)
        content_layout.addWidget(input_group, 1) # Stretch factor 1

        # Right: Operation Mode
        mode_group = QGroupBox("Analysis Settings")
        mode_layout = QVBoxLayout()
        
        mode_row = QHBoxLayout()
        mode_label = QLabel("Operation Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Select ...", "Preprocess FASTQ", "Assemble", "Classify nt", "Classify aa"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        
        mode_row.addWidget(mode_label)
        mode_row.addWidget(self.mode_combo)
        mode_layout.addLayout(mode_row)

        # Dynamic Parameters Area
        self.param_widget = QWidget()
        self.param_layout = QVBoxLayout(self.param_widget)
        self.param_layout.setContentsMargins(0,0,0,0)
        mode_layout.addWidget(self.param_widget)
        
        mode_group.setLayout(mode_layout)
        content_layout.addWidget(mode_group, 1) # Stretch factor 1
        
        content_wrapper_layout.addLayout(content_layout)

        # Spacer to push buttons down
        content_wrapper_layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.analyze_btn.setMinimumHeight(40)
        
        self.save_btn = QPushButton("Save Results")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.cancel_analysis)
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setEnabled(False)

        btn_layout.addWidget(self.analyze_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        content_wrapper_layout.addLayout(btn_layout)
        
        # Add wrapper to scroll area and scroll area to main layout
        self.scroll_area.setWidget(content_wrapper)
        self.main_layout.addWidget(self.scroll_area)

        # Footer Area
        # 1. System Status Mini-Bar
        self.status_bar = QLabel("SYSTEM: READY")
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setStyleSheet(f"color: {COLORS['primary']}; font-family: 'Consolas'; font-size: 10px; background: rgba(0,0,0,0.1); border-top: 1px solid {COLORS['secondary']}; padding: 2px;")
        self.main_layout.addWidget(self.status_bar)
        
        # Link for compatibility
        self.status_label = self.status_bar

        # 2. Main Branding Footer
        footer_wrap = QFrame()
        footer_wrap.setObjectName("FooterWrap")
        footer_wrap.setStyleSheet(f"""
            #FooterWrap {{
                background: {COLORS['bg_medium']};
                border-top: 1px solid {COLORS['secondary']};
            }}
        """)
        footer_wrap.setFixedHeight(50)
        footer_layout = QHBoxLayout(footer_wrap)
        footer_layout.setContentsMargins(40, 0, 40, 0)

        # Left: Gmail Support
        gmail_container = QWidget()
        gmail_layout = QHBoxLayout(gmail_container)
        gmail_layout.setContentsMargins(0, 0, 0, 0)
        gmail_layout.setSpacing(6)
        
        gmail_icon = QLabel("✉")
        gmail_icon.setStyleSheet(f"color: {COLORS['danger']}; font-size: 16px;")
        
        gmail_link = QLabel("support@oneresearchhub.in")
        gmail_link.setCursor(Qt.CursorShape.PointingHandCursor)
        gmail_link.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px; text-decoration: none; border: none; background: transparent;")
        
        def open_mailto(event):
            QDesktopServices.openUrl(QUrl("mailto:support@oneresearchhub.in"))
            
        gmail_link.mousePressEvent = open_mailto
        
        gmail_layout.addWidget(gmail_icon)
        gmail_layout.addWidget(gmail_link)
        footer_layout.addWidget(gmail_container, 1, Qt.AlignmentFlag.AlignLeft)

        # Center: Copyright
        copyright_lbl = QLabel("COPYRIGHT © 2026 ONE RESEARCH HUB. ALL RIGHTS RESERVED")
        copyright_lbl.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 9px; letter-spacing: 1.5px; font-weight: 500; border: none; background: transparent;")
        footer_layout.addWidget(copyright_lbl, 2, Qt.AlignmentFlag.AlignCenter)

        # Right: Developer Quote
        dev_container = QWidget()
        dev_layout = QHBoxLayout(dev_container)
        dev_layout.setContentsMargins(0, 0, 0, 0)
        dev_layout.setSpacing(8)
        
        dev_text = QLabel("Developed by Dr. Kanmani Bharathi")
        dev_text.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px; border: none; background: transparent; font-weight: bold;")
        
        dev_layout.addWidget(dev_text)

        if 'PHOTO_DATA' in globals():
            try:
                photo_lbl = QLabel()
                pixmap = QPixmap()
                pixmap.loadFromData(base64.b64decode(PHOTO_DATA))
                rounded_pixmap = self.get_circular_pixmap(pixmap, 28)
                photo_lbl.setPixmap(rounded_pixmap)
                dev_layout.addWidget(photo_lbl)
            except Exception as e:
                print(f"Failed to load photo: {e}")

        footer_layout.addWidget(dev_container, 1, Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(footer_wrap)


        # Initialize Param Widgets holders
        self.entries = {}
        self.param_container_fastq = None
        self.param_container_assemble = None

        self.create_param_widgets()
        self.on_mode_change("Select ...")

    def create_param_widgets(self):
        # Create hidden widgets for switching
        self.param_container_fastq = QWidget()
        l_fq = QGridLayout(self.param_container_fastq)
        self.entries['min_qual'] = self.add_param_row(l_fq, 0, "Min. Qual:", "20")
        self.entries['max_reads'] = self.add_param_row(l_fq, 1, "Max Reads:", "5000")
        self.entries['trim_ends'] = self.add_param_row(l_fq, 2, "Trim Ends:", "10")
        self.rev_chk = QCheckBox("Reverse Complement")
        self.rev_chk.setChecked(True)
        l_fq.addWidget(self.rev_chk, 3, 1)

        self.param_container_assemble = QWidget()
        l_asm = QGridLayout(self.param_container_assemble)
        self.entries['kmers'] = self.add_param_row(l_asm, 0, "K-MERS (sep ;):", "21;33;45;55;65")
        self.entries['min_kfreq'] = self.add_param_row(l_asm, 1, "Min. k-mer Freq:", "5")
        self.entries['min_contig'] = self.add_param_row(l_asm, 2, "Min. Contig:", "200")
        self.entries['tip_thres'] = self.add_param_row(l_asm, 3, "Tip Threshold Factor:", "2")
        self.entries['max_bubble'] = self.add_param_row(l_asm, 4, "Max Bubble Path:", "250")
        self.entries['bubble_cov'] = self.add_param_row(l_asm, 5, "Bubble Cov Ratio:", "2.0")

    def add_param_row(self, layout, row, label, default):
        lbl = QLabel(label)
        edit = QLineEdit(default)
        layout.addWidget(lbl, row, 0)
        layout.addWidget(edit, row, 1)
        return edit

    def on_mode_change(self, text):
        # Clear current param widget
        if self.param_layout.count():
            item = self.param_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None) # Detach

        if text == "Preprocess FASTQ":
            self.param_layout.addWidget(self.param_container_fastq)
            self.param_container_fastq.show()
        elif text == "Assemble":
            self.param_layout.addWidget(self.param_container_assemble)
            self.param_container_assemble.show()
            
        self.save_btn.setEnabled(False)
        self.generated_files = {}

    def select_input_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if f:
            self.input_path.setText(f)

    def start_analysis(self):
        mode = self.mode_combo.currentText()
        inp = self.input_path.text()
        
        if mode == "Select ..." or not inp:
            QMessageBox.warning(self, "Warning", "Please select a file and a valid operation mode.")
            return

        if not os.path.exists(inp):
            QMessageBox.critical(self, "Error", "Input file does not exist.")
            return

        # Gather Params
        params = {}
        try:
            if mode == "Preprocess FASTQ":
                params['min_qual'] = int(self.entries['min_qual'].text())
                params['trim_ends'] = int(self.entries['trim_ends'].text())
                params['max_reads'] = int(self.entries['max_reads'].text())
                params['reverse'] = self.rev_chk.isChecked()
            elif mode == "Assemble":
                params['kmers'] = self.entries['kmers'].text()
                params['min_kfreq'] = int(self.entries['min_kfreq'].text())
                params['min_contig'] = int(self.entries['min_contig'].text())
                params['tip_thres'] = int(self.entries['tip_thres'].text())
                params['max_bubble'] = int(self.entries['max_bubble'].text())
                params['bubble_cov'] = float(self.entries['bubble_cov'].text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid numeric parameters.")
            return

        self.last_mode = mode
        self.toggle_inputs(False)
        self.status_label.setText("Running Analysis...")
        
        self.worker = Worker(mode, inp, self.temp_output_base, params)
        self.worker.signals.finished.connect(self.on_finished)
        self.worker.signals.error.connect(self.on_error)
        self.worker.signals.result_ready.connect(self.on_result)
        self.worker.start()

    def on_finished(self):
        self.toggle_inputs(True)
        self.status_label.setText("Analysis Complete")
        QMessageBox.information(self, "Success", "Analysis complete. Please save your results.")
        self.save_btn.setEnabled(True)

    def on_error(self, msg):
        self.toggle_inputs(True)
        self.status_label.setText("Error")
        QMessageBox.critical(self, "Error", msg)

    def on_result(self, files):
        self.generated_files = files

    def cancel_analysis(self):
        if self.worker.isRunning():
            self.worker.cancel()
            self.status_label.setText("Cancelling...")

    def toggle_inputs(self, enabled):
        self.analyze_btn.setEnabled(enabled)
        self.cancel_btn.setEnabled(not enabled)
        self.mode_combo.setEnabled(enabled)
        # self.save_btn handled separately
        
    def get_circular_pixmap(self, pixmap, size):
        scaled = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        out = QPixmap(size, size)
        out.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(out)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        return out

    def save_results(self):
        if not self.generated_files: return
        
        initial_file = "result"
        extensions = "" # "Format Name (*.ext);;Others (*.txt)"
        
        if "Preprocess" in self.last_mode:
            extensions = "FASTA (*.fasta);;FASTQ (*.fastq)"
            initial_file = "trimmed_reads"
        elif "Assemble" in self.last_mode:
            extensions = "FASTA (*.fasta)"
            initial_file = "assembly"
        elif "Classify" in self.last_mode:
            extensions = "Text Table (*.txt);;FASTA Unclassified (*.fasta)"
            initial_file = "classification"
            
        f, selected_filter = QFileDialog.getSaveFileName(self, "Save Results", initial_file, extensions)
        
        if f:
            ext = os.path.splitext(f)[1].lower()
            source = None
            
            # Simple matching logic
            if ".fastq" in selected_filter or ext == ".fastq":
                source = self.generated_files.get('fastq')
            elif ".fasta" in selected_filter or ext == ".fasta":
                source = self.generated_files.get('fasta')
            elif ".txt" in selected_filter or ext == ".txt":
                source = self.generated_files.get('txt')
            
            # Fallback
            if not source and len(self.generated_files) == 1:
                source = list(self.generated_files.values())[0]

            if source and os.path.exists(source):
                try:
                    shutil.copy2(source, f)
                    QMessageBox.information(self, "Saved", f"File saved successfully to {f}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")


if __name__ == "__main__":
    # Taskbar icon fix for Windows
    if sys.platform == 'win32':
        myappid = 'oneresearchhub.seqanalysis.v1' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    
    # Load Custom Font
    font_path = "Isidora.otf"
    font_family = "Segoe UI" # Default
    
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFontFromData(base64.b64decode(FONT_DATA))
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font_family = font_families[0]
                # Update default font for App
                app.setFont(QFont(font_family, 10))

    # Apply Stylesheet
    app.setStyleSheet(get_stylesheet(font_family))
    
    # Init Window
    palette = QPalette()
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(COLORS['bg_dark']))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(COLORS['text_light']))
    app.setPalette(palette)
    
    window = MainWindow()
    
    # Specifically update title font if custom font loaded
    if font_family != "Segoe UI":
        window.title_label.setFont(QFont(font_family, 24, QFont.Weight.Bold))
        
    window.show()
    sys.exit(app.exec())
