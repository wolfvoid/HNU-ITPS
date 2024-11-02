<template>
    <div>
        <div class="title mb-8">
            <div style="text-align: center;">
                <div class="text-8">可视化分析</div>
            </div>
        </div>
        <!-- Horizontal Button Selection -->
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="display: flex; justify-content: center; gap: 20px;">
                <button v-for="(label, index) in buttonLabels" :key="index" @click="selectComponent(index)">
                    {{ label }}
                </button>
            </div>
        </div>
        <!-- Display Selected Component -->
        <div style="text-align: center;">
            <component :is="currentComponent"></component>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import v1_top from './v1-top.vue';
import v2_RoadRanking from './v2-RoadRanking.vue';
import v3_dayRanking from './v3-dayRanking.vue';
import v4_weekRanking from './v4-weekRanking.vue';
import v5_months from './v5-months.vue';
import v6_amonth from './v6-amonth.vue';
import v7_aday from './v7-aday.vue';
import v8_aweek from './v8-aweek.vue';

const buttonLabels = ref<string[]>([
    '交通拓扑图',
    '路段通行时间排名',
    '单日通行时段排名',
    '一周通行时间排名',
    '月份通行时段变化',
    '月内通行时段变化',
    '天内通行时段变化',
    '周内通行时段变化'
]);

const components = [
    v1_top,
    v2_RoadRanking,
    v3_dayRanking,
    v4_weekRanking,
    v5_months,
    v6_amonth,
    v7_aday,
    v8_aweek
];

// 获取最后选择的组件索引，默认为0
const lastIndex = localStorage.getItem('lastComponentIndex');
const currentComponent = ref(components[lastIndex ? parseInt(lastIndex) : 0]);

const selectComponent = (index: number) => {
    currentComponent.value = components[index]; // 根据按钮索引切换组件
    localStorage.setItem('lastComponentIndex', index.toString()); // 保存当前索引到 localStorage
};

onMounted(() => {
    // 组件挂载时从 localStorage 读取并更新组件
    const lastIndex = localStorage.getItem('lastComponentIndex');
    if (lastIndex) {
        currentComponent.value = components[parseInt(lastIndex)];
    }
});
</script>

<style scoped>
button {
    padding: 10px 20px;
    cursor: pointer;
    border: none;
    background-color: #1ba0e3;
    color: white;
    border-radius: 5px;
    transition: background-color 0.3s;
    min-width: 100px;
    /* Minimum width for buttons */
}

button:hover {
    background-color: #45a049;
}
</style>
