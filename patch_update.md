## 补丁包更新说明

注意：补丁包的下载、解压、处理等操作请在工作文件夹`IPCC`下进行

**1. 从共享云盘下载各个补丁包（补丁包之间相互独立），并传到Jetson Orin NX上**

关于补丁包的传输，可以采用以下两种方式：

- 直接在Jetson Orin NX上下载`backends_patchv1.zip`以及其分卷`backends_patchv1.z01`等补丁包


- 先在电脑端下载各个补丁包，然后使用U盘（可直接使用创乐博官方套件中的U盘）将补丁包拷贝到Jetson上 **(推荐)**

若第一次进行补丁包更新，请同步下载`backends_update.py`、`check_backends.py`以及新版`inference_trt.py`三个后端处理脚本


**2. 恢复并解压补丁包**

````sh
zip -F backends_patchv1.zip --out patch1-re.zip
unzip patch1-re.zip
````

**3. 进行补丁包更新**

````sh
python backends_update.py
````

若程序正常运行，应能够输出后端更新的后端模型、更新的后端模型数量、更新的配置文件数量、自动移除的onnx后端数量

**4. 进行后端模型检查**

````sh
python check_backends.py
````

若程序正常，应当输出：

````sh
XXX backends is available!
````

至此，后端模型补丁包更新完毕！相关压缩包可以自行删除

**5. 试运行推理脚本**

````sh
conda activate ipcc
python inference_trt.py --mode mmseg --cropsize 512 --quant no --model DeepLabV3+ --data Vaihingen --backbone ResNet101 --workdirs ./ --user test --src c512/
````

若配置正常，应当可在`result/test-c512`中查看推理结果

相关参数支持详见`README.md`文件