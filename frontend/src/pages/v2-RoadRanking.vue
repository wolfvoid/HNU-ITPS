<template>
    <div>
        <h2 style="font-size: 36px;">路段通行时间排名</h2>
        <br><br>
        <!-- 装饰的选择框 -->
        <div style="margin: 20px 0;">
            <br><br>
            <p>“选定”后重新进行推理并生成图片<br>可能需要等待30s左右</p>
            <label for="timeRanking" style="font-weight: bold;">选择查看前k位:</label>
            <select id="timeRanking" v-model="selectedRank" @change="sendRankToBackend"
                style="margin-left: 10px; padding: 5px; border-radius: 5px;">
                <option disabled value="">请选择</option>
                <option v-for="rank in ranks" :key="rank" :value="rank">{{ rank }}</option>
            </select>
        </div>

        <!-- 显示图片 -->
        <img :src="imageSrc" alt="展示图片" style="max-width: 100%; height: auto;">
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 定义一个变量来存储选择的排名
const selectedRank = ref('');

// 创建一个数组，从1到20
const ranks = Array.from({ length: 20 }, (_, i) => i + 1);

// 定义图片 URL 变量
const imageSrc = ref('/images/hnu.png'); // 初始显示图片A
const imageB = '/images/loading.png'; // 发送请求时显示图片B
const imageC = '/images/v2.png'; // 接收到返回后显示图片C

// 定义一个方法，发送请求到后端
const sendRankToBackend = async () => {
    if (selectedRank.value) {
        console.log('发送的选择排名:', selectedRank.value);
        imageSrc.value = imageB;
        try {
            const response = await axios.post('http://127.0.0.1:5000/vision/v2/roadrank', { rank: selectedRank.value });
            if (response.data.success) {
                ElMessage.success('请求成功');
                imageSrc.value = imageC + '?' + new Date().getTime();
            } else {
                console.error('请求失败:', response.data.msg);
                ElMessage.error('后端返回失败');
            }
        } catch (error) {
            console.error('发送失败:', error);
            ElMessage.error('发送请求失败');
        }
    } else {
        ElMessage.warning('请先选择一个排名');
    }
};
</script>

<style scoped>
/* 样式 */
select {
    padding: 5px 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    font-size: 16px;
}

img {
    margin-top: 20px;
    border-radius: 10px;
}
</style>
