<div align="center">
    <img src="pics/shortmark.jpg" alt="">
</div>
<div align="center">
    <h2>
        IPCC : Intelligent Perception and Cooperative Computing Platform on  Constellation Network
    </h2>
</div>
<div align="center">
    <a href="#">
        <span>项目主页</span>
    </a>
</div>
<br>


<div align="center">

[![GitHub stars](https://badgen.net/github/stars/shadowwalk370/IPCC)](https://github.com/shadowwalk370/IPCC) &nbsp; [![license](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

</div>

## 简介

本项目是基于多个 **[NVIDIA Jetson Orin NX](https://www.nvidia.cn/autonomous-machines/embedded-systems/jetson-orin/)** 边缘计算设备所搭建的🌏 **分布式遥感图像智能解译平台** 🌏。

其中各个🌟 **后端模型** 🌟基于 **[mmsegmentation](https://github.com/open-mmlab/mmsegmentation)、[mmpretrain](https://github.com/open-mmlab/mmpretrain)、[mmdetection](https://github.com/open-mmlab/mmdetection)** 等开源项目进行开发，并基于 **[mmdeploy](https://github.com/open-mmlab/mmdeploy)** 进行模型的部署和推理工作。

本项目的后端模型目前支持的版本为Python 3.8 、 PyTorch 1.11 、 mmcv 2.0.1 、 mmdet 3.3.0 、 mmsegmentation 1.2.2 、 mmpretrain 1.2.0 , 在NVIDIA Jetson Orin NX 上采用JetPack 5.1.1 ,其余具体环境配置请参考📜 **[IPCC终端环境配置指南](./env.md)、[补丁包更新说明](./patch_update.md)** 📜。

本项目所应用到的🚀 **后端模型及其处理脚本** 🚀可以直接从 **[这个云盘](https://bhpan.buaa.edu.cn/link/AA532216B6F54E4ABE9AED79200C90E84D)** 获取。

## 主要特性

✨ **多场景智能感知**

提供不同数据集场景下的 **多种后端模型** ，涵盖遥感场景分类、遥感地物分割、遥感目标检测等不同任务，并且 **支持fp16与int8量化** ，便于轻松部署和推理

✨ **多星通信组网**

基于底层socket，封装了文件层面的传输，并可进行**命令式交互**，极大简化了传输的流程

✨ **分布式协同计算**

灵感源于pytorch的分布式训练中的通信原语，实现了**文件层面的通信原语操作**，如broadcast、scatter、gather等。

✨ **半实物仿真与可视化前端** （暂未更新）

实现半实物的仿真系统以及流量负载可视化前端

## 更新日志

🎉 **2024.2.1** 正式发布IPCC项目，更新了基本的模型推理脚本以及90余个不同的mmseg模型后端。

🎉 **2024.2.6** 更新了后端模型补丁更新脚本、后端检查脚本，修复了模型推理脚本多张图片存储不一致的问题，新增支持mmseg模型后端，总共包含162个不同的后端。

🎉 **2024.2.26** 更新了通信组网代码，可通过极简单的命令式交互轻松进行图片或者文件的传输；将图片推理脚本融合进通信组网的命令式交互当中；新增更新25个遥感场景分类后端，但暂未更新推理脚本。

## 模型库

目前已经提供的TensorRT后端如下：

<table border="1">
    <tr >
        <th rowspan="2" width="200">框架</th>
        <th rowspan="2" width="150">模型</th>
        <th rowspan="2" width="100">主干</th>
        <th colspan="3">量化方式</th>
    </tr>
    <tr>
        <th width="175">no</th>
        <th width="175">fp16</th>
        <th width="175">int8</th>
    </tr>
    <tr >
        <td  align="center" rowspan="9">mmsegmentation</td>
        <td align="center" rowspan="3" >DeepLabV3+</td>
        <td align="center">ResNet18</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center">ResNet50</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center">ResNet101</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center" rowspan="3">PSPNet</td>
        <td align="center">ResNet18</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center">ResNet50</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center">ResNet101</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center" rowspan="3">FCN</td>
        <td align="center">ResNet18</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center">ResNet50</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr>
        <td align="center">ResNet101</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
        <td align="center">512✅/1024✅</td>
    </tr>
    <tr >
        <td  align="center" rowspan="8">mmpretrain</td>
        <td align="center" rowspan="3" >ResNet</td>
        <td align="center">ResNet18</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
    <tr>
        <td align="center">ResNet50</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
    <tr>
        <td align="center">ResNet101</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
    </tr>
        <td align="center" rowspan="5" >EfficientNet</td>
        <td align="center">B0</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
    <tr>
        <td align="center">B1</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
    <tr>
        <td align="center">B2</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
    <tr>
        <td align="center">B3</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
    <tr>
        <td align="center">B4</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
        <td align="center">224✅</td>
    </tr>
</table>

## 教程文档

<details>
<summary>环境配置</summary>

- [云服务器开发环境配置](./env.md#一云服务器开发环境配置)
- [NVIDIA Jetson 环境配置](./env.md#二jetson-orin-nx开发环境配置)

</details>

<details>
<summary>模型部署和推理</summary>

- [模型推理](./env.md#二jetson-orin-nx开发环境配置)
- [补丁更新](./patch_update.md)

</details>

<details>
<summary>通信组网相关</summary>

- [命令式交互通信](./dist.md)

</details>


## 致谢

本项目是基于 **[mmsegmentation](https://github.com/open-mmlab/mmsegmentation)、[mmpretrain](https://github.com/open-mmlab/mmpretrain)、[mmdetection](https://github.com/open-mmlab/mmdetection)** 等项目进行开发、基于 **[mmdeploy](https://github.com/open-mmlab/mmdeploy)** 进行落地部署的，诚挚感谢相关的开发者们！

## 开源许可证

该项目采用 **[Apache 2.0 开源许可证](LICENSE)**。

## 欢迎联系和交流

如果您有任何想交流的问题或者建议，可以通过以下邮箱联系我们😁。
```
shadowwalk370@hotmail.com
```