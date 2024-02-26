from mmdeploy.apis.utils import build_task_processor
from mmdeploy.utils import get_input_shape, load_config
from mmdeploy.apis import inference_model
import argparse
import os
import numpy as np
import cv2
import shutil

def get_models():
    model_dict = {
    "FCN" : { "backbone" : ["ResNet18","ResNet50","ResNet101"] , "data" : ["LoveDA","Potsdam","Vaihingen"] , "cropsize" : ["512","1024"] , "quant" : ["no","fp16","int8"]},
    "DeepLabV3+" : {"backbone" : ["ResNet18","ResNet50","ResNet101"] , "data" : ["LoveDA","Potsdam","Vaihingen"] , "cropsize" : ["512","1024"] , "quant" : ["no","fp16","int8"]},
    "PSPNet" : {"backbone" : ["ResNet18","ResNet50","ResNet101"] , "data" : ["LoveDA","Potsdam","Vaihingen"] , "cropsize" : ["512","1024"] , "quant" : ["no","fp16","int8"]},
    "ResNet" : {"backbone" : ["ResNet18","ResNet50","ResNet101"] , "data" : ["NWPU"] , "cropsize" : ["224"] , "quant" : ["no","fp16","int8"]},
    "EfficientNet" : {"backbone" : ["B0","B1","B2","B3","B4"] , "data" : ["NWPU"] , "cropsize" : ["224"] , "quant" : ["no","fp16","int8"]},
    "VIT" : {"backbone" : ["Base",] , "data" : ["NWPU"] , "cropsize" : ["224"] , "quant" : ["no",]},
    }
    return model_dict

def get_palette(dataset):
    if(dataset == 'LoveDA'):
        palette=[[255, 255, 255], [255, 0, 0], [255, 255, 0], [0, 0, 255],
                 [159, 129, 183], [0, 255, 0], [255, 195, 128]]
    elif(dataset == 'Potsdam'):
        palette=[[255, 255, 255], [0, 0, 255], [0, 255, 255], [0, 255, 0],
                 [255, 255, 0], [255, 0, 0]]
    elif(dataset == 'Vaihingen'):
        palette=[[255, 255, 255], [0, 0, 255], [0, 255, 255], [0, 255, 0],
                 [255, 255, 0], [255, 0, 0]]
    return palette

def inference_trt(
        mode,
        cropsize,
        quant,
        model,
        data,
        backbone,
        user,
        src,
        workdirs='./',
):
    model_dict = get_models()
    deploy_cfg=workdirs+'/mmdeploy-main/configs/mmseg/segmentation_tensorrt_static-'+cropsize+'x'+cropsize+'.py'
    model_cfg=workdirs+'/backends/configs/'+model+'_'+data+'_'+backbone+'.py'
    device='cuda:0'
    backend_model = [workdirs+'/backends/'+model+'_'+data+'_'+backbone+'_'+cropsize+'_'+quant+'/end2end.engine']
    palette = get_palette(data)
    #print(palette)
    #assert palette != None , '需要输入正确的数据集参数'

    assert model in model_dict.keys() , '需要输入正确的模型参数'
    assert data in model_dict.get(model).get("data") , '需要输入正确的数据集参数'
    assert backbone in model_dict.get(model).get("backbone") , '需要输入正确的backbone参数'
    assert cropsize in model_dict.get(model).get("cropsize") , '需要输入正确的裁切尺寸'
    assert quant in model_dict.get(model).get("quant") , '需要输入正确的量化方式'

    dst_dir = workdirs+'/result/'+str(user)+'-'+str(src)
    os.makedirs(dst_dir,exist_ok=True)

    for imgs in os.listdir(workdirs+'/source/'+src):
        image = workdirs+'/source/'+src+'/'+imgs
        ori = cv2.imread(image)
        res = cv2.resize(ori,(int(cropsize),int(cropsize)), interpolation=cv2.INTER_LINEAR)
        # print(image.split('/')[-1])

        result = inference_model(
            model_cfg=model_cfg,
            deploy_cfg=deploy_cfg,
            backend_files=backend_model,
            img=image,
            device=device
        )
        pred_mask = result[0].pred_sem_seg.data.squeeze(0).detach().cpu().numpy().astype(np.uint8)
        #print(pred_mask.shape)
        pred_mask = cv2.resize(pred_mask,(int(cropsize),int(cropsize)), interpolation=cv2.INTER_LINEAR)
        colored_mask = np.zeros([int(cropsize),int(cropsize),3],dtype=np.uint8)
        for label, color in enumerate(palette):
            colored_mask[pred_mask == label] = color  # 注意数组的特别用法
        # pred = (np.array(result[0].pred_sem_seg)).astype(np.uint8)
        
        combine = cv2.addWeighted(res,0.5,colored_mask,0.5,0)
        cv2.imwrite(os.path.join(dst_dir,imgs),combine)

def backends_update():
    count = 0
    count_onnx = 0
    count_configs = 0

    for folders in os.listdir("./"):
        if "backends_patch" in folders:
            for backends in os.listdir("./"+folders):
                if "_" in backends :
                    if os.path.exists(os.path.join("backends",backends)) == False:
                        if "calib_data.h5" in os.listdir(os.path.join(folders,backends)):
                            os.remove(os.path.join(folders,backends,"calib_data.h5"))
                        shutil.copytree(os.path.join(folders,backends),os.path.join("backends",backends))
                        count += 1
                        print(backends + " has been updated!")
                elif "configs" == backends :
                    for configs in os.listdir(os.path.join(folders,backends)):
                        if os.path.exists(os.path.join("backends",backends,configs)) == False:
                            shutil.copy(os.path.join(folders,backends,configs),os.path.join("backends",backends,configs))
                            count_configs += 1


    if count == 0 :
        print("No need to update backends")

    else :
        print(str(count)+"  backends has been updated")

    if count_configs == 0 :
        print("No need to update configs")

    else :
        print(str(count_configs)+"  configs has been updated")

    for folders in os.listdir("./backends/"):
        if os.path.isdir(os.path.join("backends",folders)):
            if "end2end.onnx" in os.listdir(os.path.join("backends",folders)):
                os.remove(os.path.join("backends",folders,"end2end.onnx"))
                count_onnx += 1

    if count_onnx != 0 :
        print("auto remove "+str(count_onnx)+" redundant onnx backends")

    else :
        print("No redundant onnx backends")

def check_backends():
    models = get_models()
    correct_count = 0
    false_count = 0
    miss_configs = 0
    for folders in os.listdir("./backends/"):
        if os.path.isdir(os.path.join("backends",folders)) and "_" in folders :
            if folders.split("_")[0] in models.keys() :
                #print(folders.split("_")[0],type(folders.split("_")[0]))
                model = str(folders.split("_")[0])
                if folders.split("_")[1] in models.get(model).get("data") \
                and folders.split("_")[2] in models.get(model).get("backbone") \
                and folders.split("_")[3] in models.get(model).get("cropsize") \
                and folders.split("_")[4] in models.get(model).get("quant"):
                    if os.path.exists('./backends/configs/'+folders.split("_")[0]+'_'+folders.split("_")[1]+'_'+folders.split("_")[2]+'.py'):
                        correct_count += 1
                    else :
                        miss_configs += 1
                        print(folders.split("_")[0]+'_'+folders.split("_")[1]+'_'+folders.split("_")[2]+'.py' + " missed")

                else :
                    false_count += 1
                    print(folders + " is misnamed!")

    print(str(correct_count) + " backends is available!")
    if false_count != 0 :
        print(str(false_count) + " backends is not available!")
    if miss_configs != 0 :
        print(str(miss_configs) + " configs missed!")