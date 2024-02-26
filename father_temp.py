from dist_socket import father_point
import os
import time

def supervised_inference():
    supervised = 'XXX'
    inference_record = 'XXX.txt'
    while True:
        for dirs in os.listdir(supervised):
            if os.path.isdir(os.path.join(supervised,dirs)):
                if dirs not in txt2list(inference_record):
                    if 'config.txt' in os.listdir(os.path.join(supervised,dirs)):
                        with open(inference_record,'a') as fw:
                            fw.write(dirs+"\n")
                        print("-"*70)
                        print("start operating {0}".format(os.path.abspath(os.path.join(supervised,dirs))))
                        inference_source(src = os.path.join(supervised,dirs))
                else :
                    print("waiting for new sources\r",end='')
        time.sleep(2)


def inference_source(src : str = "XXX", dst : str = "XXX"):
    ip_list = ["XXX","XXX",]
    port_list = [8888,8889,]
    name_list = ["XXX","XXX",]
    father = father_point(ip_list,port_list,name_list,src,dst)
    """
    list your orders hear,such as:

    father.father_sending_order("scatter")
    father.father_sending_order("inference")
    father.father_sending_order("gather")
    father.father_sending_order("quit")
    """

def txt2list(filepath):
    txt_list = []
    if os.path.exists(filepath) == False:
        open(filepath, "x")
    with open(filepath,'r') as f:
        for ann in f.readlines():
            ann = ann.strip('\n')
            txt_list.append(str(ann))
    return txt_list
        

if __name__ == "__main__":
    # inference_source()
    supervised_inference()