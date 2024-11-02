<template>
    <div>
        <!-- 标题部分 -->
        <div class="title mb-8">
            <div style="text-align: center;">
                <div class="title-text">智慧交通预测系统</div>
            </div>
        </div>

        <!-- 新增的智慧交通预测系统内容描述部分 -->
        <div class="content">
            <p class="intro">
                随着移动互联网的快速发展，交通信息的获取和传播变得更加便捷，海量的交通数据为城市交通的智能管理提供了前所未有的机遇。
                现代城市中，交通流量的管理和预测对于缓解交通拥堵、提高运输效率、优化资源配置具有重要意义。然而，随着城市化进程的加快和车辆数量的增加，
                交通流量的波动性和复杂性也在不断加剧，传统的交通管理手段已难以满足日益增长的需求。
            </p>
            <p class="intro">
                本项目旨在基于互联网交通信息，开发一个先进的交通流量预测系统，通过建立精准的交通预测模型，预测城市中各关键路段的通行时间。
                系统的核心目标是实现对城市交通状态波动的提前预判，为城市出行者提供更加高效、便捷的出行方案。
                同时，系统将为交通管理部门提供科学的决策支持，帮助其在高峰时段和异常情况下更好地进行交通引导和管理，优化城市的交通资源配置和智能化管控水平。
            </p>
            <p class="intro">
                通过该系统，城市交通管理可以更加智能化、精准化，出行者的体验将得到显著提升，不仅可以有效降低出行时间和成本，还能减少交通拥堵带来的环境污染和社会成本。
                这不仅对城市交通管理有重要意义，也符合当前智能城市建设的发展趋势。
            </p>
            <p class="details">
                智慧交通预测系统是一款基于大数据和人工智能技术的高效工具，旨在通过对历史交通数据、实时交通状况以及其他相关因素的全面分析，
                为城市交通管理提供精准的交通流量预测与解决方案。
            </p>
            <p class="details">
                该系统通过采集多个交通数据源，包括道路传感器、交通摄像头、天气预报数据、事件报告等，结合机器学习算法与交通流量模型，自动生成交通趋势预测报告。
                系统不仅可以预测道路流量，还能对突发事件（如交通事故、施工封路）进行预警，并生成应对策略，协助交通管理部门实时做出优化决策。
            </p>
            <p class="details">
                核心功能包括：<br/>
                1. 实时交通流量预测：基于历史数据和当前数据，预测未来不同时间段的交通流量和交通拥堵点。<br/>
                2. 多维数据分析：支持用户通过多种维度查询和分析交通数据，生成多样化的统计报告，帮助更深入理解交通趋势。<br/>
                3. 历史数据对比：用户可以选择特定的时间段进行交通状况的历史数据对比，洞察趋势变化，为长期交通规划提供依据。<br/>
                4. 可视化图表展示：系统支持图表形式的交通数据展示，包括折线图、柱状图、热力图等，帮助用户更直观地查看预测结果。
            </p>
            <p class="details">
                本系统广泛适用于城市规划、交通调度、智能交通设备管理等多个领域，能够帮助提升城市交通管理的智能化水平，减少交通拥堵，提升居民出行体验，最终实现“智慧城市”的愿景。
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus';
import { cloneDeep, keys, pick, pickBy } from 'lodash-es';
import { ref } from 'vue';

// 查询表单
const queryForm = ref({
    bookname: '',
    bookid: '',
    bornum: '',
    page: 1,
});

// 表格数据
const tableData = ref<any>([]);
const total = ref(0);

</script>

<style scoped>
/* 标题样式 */
.title-text {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2c3e50;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* 内容整体布局 */
.content {
    margin-top: 20px;
    padding: 20px 40px;
    background-color: #f9fafb;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 简介部分 */
.intro {
    text-align: justify;
    font-size: 1.3rem;
    margin-bottom: 15px;
    font-weight: 500;
    line-height: 1.8;
    color: #34495e;
}

/* 详细内容部分 */
.details {
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 10px;
    text-align: left;
    color: #666;
    padding-left: 15px;
    position: relative;
}

/* 用于装饰点或编号的图标 */
.details::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #3498db;
    font-size: 1.4rem;
}

/* 调整段落间距 */
p {
    margin: 10px 0;
}

/* 背景色与间距调整 */
body {
    background-color: #ecf0f1;
    margin: 0;
    padding: 20px;
}
</style>
