<template>
    <div class="container">
        <div class="title mb-8">
            <div class="text-center">
                <div class="text-8">智慧交通预测</div>
            </div>
        </div>
        <div class="query mb-4">
            <el-form :inline="true" :model="queryForm" class="demo-form-inline">
                <el-form-item label="ID">
                    <el-input v-model="queryForm.ID" placeholder="请输入ID"></el-input>
                </el-form-item>
                <el-form-item label="日期">
                    <el-input v-model="queryForm.Date" placeholder="请输入日期"></el-input>
                </el-form-item>
                <el-form-item label="开始时间">
                    <el-input v-model="queryForm.Start_time" placeholder="请输入时间"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" icon="search" @click="getData">查询</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="data mb-4">
            <el-table :data="tableData" class="w-full" border>
                <el-table-column prop="ID" label="ID" />
                <el-table-column prop="Date" label="日期" />
                <el-table-column prop="Start_Time" label="开始时间" />
                <el-table-column prop="End_Time" label="结束时间" />
                <el-table-column prop="Value" label="值" />
            </el-table>
        </div>
        <div class="pagination">
            <el-pagination background layout="total, prev, pager, next" :total="total" :page-size="20"
                @current-change="getData" v-model:current-page="queryForm.page" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus';
import { cloneDeep, pickBy } from 'lodash-es';
import { ref } from 'vue';
import { getPreApi } from '../apis/pre';

// 查询表单
const queryForm = ref({
    ID: '',
    Date: '',
    Start_time: '',
    End_time: '',
    Value: '',
    page: 1,
})

// 表格数据
const tableData = ref<any>([])
const total = ref(0)

// 获取表格数据
const getData = async () => {
    const queryData = cloneDeep(queryForm.value)
    const query = pickBy(queryData, (item) => item !== '' && item !== null)
    const res = (await getPreApi(query)) as any
    tableData.value = res.rows
    total.value = res.total
}

getData()
</script>

<style scoped>
.container {
    max-width: 1000px;
    /* 设置最大宽度 */
    margin: 0 auto;
    /* 居中对齐 */
    padding: 20px;
    /* 内边距 */
    background-color: #f9f9f9;
    /* 背景颜色 */
    border-radius: 8px;
    /* 边角圆润 */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    /* 阴影效果 */
}

.title {
    text-align: center;
    /* 标题居中 */
}

.query {
    display: flex;
    /* 使用 flexbox 排版 */
    flex-wrap: wrap;
    /* 允许换行 */
    gap: 20px;
    /* 按钮间距 */
}

.data {
    margin-top: 20px;
    /* 上边距 */
}

.pagination {
    margin-top: 20px;
    /* 上边距 */
    text-align: center;
    /* 居中对齐 */
}

.el-table th {
    background-color: #f5f5f5;
    /* 表头背景色 */
    font-weight: bold;
    /* 加粗 */
}

.el-dialog {
    border-radius: 8px;
    /* 对话框圆角 */
}
</style>
