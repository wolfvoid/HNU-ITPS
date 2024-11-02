<template>
    <div class="container">
        <h2 style="font-size: 36px;">天内通行时段变化</h2>
        <br><br>
        <h3>已选择的道路:</h3>
        <ul class="selected-roads">
            <li v-for="road in Array.from(selectedRoads)" :key="road" class="road-item">{{ road }}</li>
        </ul>

        <!-- 加载图片 -->
        <div v-if="showImage" class="loading-image" style="max-width: 100%; height: auto;">
            <img :src="imageSrc" alt="Loading" />
        </div>

        <!-- 发送按钮 -->
        <button class="send-button" @click="sendRoadsToBackend">分析</button>
        <br><br>
        <p>“分析”将实时进行推理并更新图片<br>可能需要等待30s左右</p>
        <br><br>

        <!-- 道路名称列表 -->
        <div class="road-list">
            <div v-for="road in roads" :key="road" class="road-item">
                <span class="road-name" :title="road">{{ road }}</span>
                <div class="button-group">
                    <button @click="addRoad(road)" :disabled="selectedRoads.has(road)">增添</button>
                    <button @click="removeRoad(road)" :disabled="!selectedRoads.has(road)">删去</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const imageSrc = ref('/images/v7.png'); // 初始图片 URL
const showImage = ref(false); // 新增状态变量，控制图片显示

// 定义道路名称数组（可以替换为实际的132个道路名称）
const roads = [
    '4377906287425800514',
    '4377906287959500514',
    '9377906286566510514',
    '4377906288421600514',
    '4377906288194800514',
    '4377906282541600514',
    '4377906288243600514',
    '4377906280344800514',
    '4377906287063800514',
    '4377906285032600514',
    '4377906283759500514',
    '4377906288663800514',
    '4377906284769500514',
    '4377906283769500514',
    '4377906286041600514',
    '4377906285041600514',
    '4377906289525800514',
    '3377906280028510514',
    '4377906281234600514',
    '4377906287141600514',
    '3377906287674510514',
    '4377906280763800514',
    '3377906287886510514',
    '9377906283125510514',
    '4377906283959500514',
    '4377906285594800514',
    '4377906288893600514',
    '4377906289663800514',
    '4377906288041600514',
    '4377906284514600514',
    '4377906280163800514',
    '9377906285566510514',
    '3377906283328510514',
    '4377906288593600514',
    '4377906282532600514',
    '4377906280863800514',
    '4377906284653600514',
    '4377906286681600514',
    '4377906280329500514',
    '4377906282141600514',
    '4377906285525800514',
    '4377906288959500514',
    '4377906282769500514',
    '4377906280234600514',
    '3377906280395510514',
    '4377906287663800514',
    '4377906286169500514',
    '4377906281241600514',
    '4377906284422600514',
    '3377906281518510514',
    '4377906289425800514',
    '4377906286032600514',
    '4377906283422600514',
    '4377906288063800514',
    '9377906288175510514',
    '4377906281784800514',
    '4377906288738500514',
    '4377906284959500514',
    '4377906289041600514',
    '4377906285681600514',
    '4377906283815800514',
    '4377906286334600514',
    '4377906282653600514',
    '4377906289244800514',
    '9377906283776510514',
    '9377906284555510514',
    '9377906282776510514',
    '3377906282418510514',
    '4377906280334600514',
    '4377906282763800514',
    '4377906282759500514',
    '4377906284594800514',
    '4377906286141600514',
    '4377906287863800514',
    '4377906288869500514',
    '4377906287169500514',
    '4377906281041600514',
    '4377906283525800514',
    '4377906281741600514',
    '4377906282969500514',
    '3377906288228510514',
    '9377906281555510514',
    '4377906289813600514',
    '3377906289434510514',
    '9377906286615510514',
    '4377906289243600514',
    '3377906287934510514',
    '4377906284525800514',
    '4377906288234600514',
    '4377906289869500514',
    '4377906281959500514',
    '4377906285334600514',
    '4377906287194800514',
    '4377906286843600514',
    '4377906281969500514',
    '4377906280913600514',
    '9377906289175510514',
    '3377906282328510514',
    '4377906281141600514',
    '3377906289044510514',
    '3377906289228510514',
    '4377906289141600514',
    '4377906285343600514',
    '3377906286918510514',
    '3377906285434510514',
    '4377906286525800514',
    '4377906284759500514',
    '4377906289863800514',
    '4377906280969500514',
    '4377906282815800514',
    '4377906280141600514',
    '3377906281774510514',
    '4377906289063800514',
    '4377906285141600514',
    '4377906280241600514',
    '4377906282959500514',
    '3377906284028510514',
    '4377906285759500514',
    '3377906284395510514',
    '4377906280815800514',
    '4377906280784800514',
    '3377906285934510514',
    '4377906284141600514',
    '4377906281763800514',
    '4377906284838500514',
    '4377906286343600514',
    '3377906289674510514',
    '4377906288425800514',
    '4377906287243600514',
    '4377906287869500514',
    '4377906283141600514',
    '9377906285615510514',
];

// 使用Set来存储已选择的道路名称
const selectedRoads = ref(new Set());

// 增添道路名称
const addRoad = (road) => {
    selectedRoads.value.add(road);
};

// 删去道路名称
const removeRoad = (road) => {
    selectedRoads.value.delete(road);
};

// 发送请求到后端
const sendRoadsToBackend = async () => {
    if (selectedRoads.value.size > 0) {
        const roadsArray = Array.from(selectedRoads.value);
        try {
            ElMessage.success('正在发送请求');
            const response = await axios.post('http://127.0.0.1:5000/vision/traveltime', {
                status: "aday",
                roads: roadsArray
            });
            if (response.data.success) {
                // 在成功响应后显示图片，并更新图片源以防缓存
                imageSrc.value = '/images/v7.png' + '?' + new Date().getTime();
                showImage.value = true; // 显示图片
                ElMessage.success('请求成功');
            } else {
                ElMessage.error('后端返回失败');
            }
        } catch (error) {
            ElMessage.error('发送请求失败');
        }
    } else {
        ElMessage.warning('请先选择至少一个道路');
    }
};
</script>

<style scoped>
/* 整体容器 */
.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 已选择的道路样式 */
.selected-roads {
    display: flex;
    flex-wrap: wrap;
    padding: 0;
    margin: 10px 0 20px;
}

.selected-roads .road-item {
    background-color: #e0f7fa;
    padding: 8px;
    border-radius: 4px;
    margin: 5px;
}

/* 加载图片样式 */
.loading-image {
    text-align: center;
    margin: 20px 0;
}

.loading-image img {
    max-width: 100%;
    height: auto;
}

/* 发送按钮样式 */
.send-button {
    margin-top: 20px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.send-button:hover {
    background-color: #0056b3;
}

/* 道路名称列表样式 */
.road-list {
    display: flex;
    flex-wrap: wrap;
    margin: 10px 0;
}

/* 道路项样式 */
.road-item {
    margin: 10px;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #ffffff;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-basis: calc(33% - 20px);
    box-sizing: border-box;
}

/* 道路名称样式 */
.road-name {
    font-weight: bold;
    max-width: 150px;
    /* 设置最大宽度 */
    white-space: nowrap;
    /* 不换行 */
    overflow: hidden;
    /* 隐藏溢出的文本 */
    text-overflow: ellipsis;
    /* 末尾添加省略号 */
}

/* 按钮组样式 */
.button-group {
    display: flex;
    gap: 10px;
}

button {
    padding: 5px 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    background-color: #20f7f7;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #e0e0e0;
}

button:disabled {
    background-color: #e0e0e0;
    cursor: not-allowed;
}
</style>
