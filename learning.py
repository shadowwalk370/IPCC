import streamlit as st
import pandas as pd
import time
import cv2

st.write("""
# 一起来看图吧！

提示：这是某位大学牲尝试使用streamlit部署的一个网站

网站功能极其简单，上传本地的一张图片，会在这个网站打开它

一起来试试吧！！！以后还会更新更多内容的

啊当然，在此之前，请先按照requirements来配置环境嗷~
""")

banner = cv2.imread("./pics/chuaiyourhands.png")
st.image(banner,channels="BGR")

title = st.text_input('请输入图片路径',"./pics/waiting.png")
file = cv2.imread(title)
st.write('Your picture is:')
st.image(file,channels="BGR")
