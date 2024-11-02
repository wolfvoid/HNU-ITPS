<template>
    <div>
        <h2 style="font-size: 36px;">单日通行时段排名</h2>
        <br><br>
        <!-- 显示更新时间信息 -->
        <div style="margin-top: 10px;">
            更新至当前时间: {{ currentTime }}
        </div>

        <button @click="recalculateImages" style="margin-top: 20px;">重新计算</button>
        <br><br>
        <p>“重新计算”将重新进行推理并更新图片<br>可能需要等待30s左右</p>
        <!-- 显示交通拓扑图或“请等待”图片 -->
        <img :src="imageSrc" alt="单日通行时段排名" style="max-width: 100%; height: auto;">
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 定义一个变量来存储当前时间
const currentTime = ref('');

// 定义一个变量来存储图片的 URL
const imageSrc = ref('/images/v3.png'); // 初始图片 URL
const loadingImage = '/images/loading.png'; // 请等待的图片 URL

// 更新当前时间的函数
const updateTime = () => {
    const now = new Date();
    currentTime.value = now.toLocaleString(); // 格式化时间为本地字符串
};

// 定义一个方法，发送请求到后端
const recalculateImages = async () => {
    console.log('开始重新计算，显示请等待的图片');
    // 开始重新计算时显示“请等待”图片
    imageSrc.value = loadingImage;
    try {
        const response = await axios.post('http://127.0.0.1:5000/vision/v3/dayrank'); // 替换为您的后端 API 路径
        if (response.data.success) { // 根据后端返回的数据结构判断成功
            ElMessage.success('重新计算成功');
            // 在接收到后端回复后更新当前时间
            updateTime();
            imageSrc.value = '/images/v3.png' + '?' + new Date().getTime();
        } else {
            console.error('重新计算失败:', response.data.msg);
            ElMessage.error('后端返回失败');
        }
    } catch (error) {
        console.error('重新计算失败:', error);
    }
};

// 在组件加载时初始化当前时间
onMounted(updateTime);
</script>

<style scoped>
/* 样式 */
button {
    padding: 10px 20px;
    background-color: #4CAF50;
    /* Green */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #45a049;
    /* Darker green */
}
</style>
