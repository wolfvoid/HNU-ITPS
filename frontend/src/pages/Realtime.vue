<template>
  <div class="container">
    <div class="title mb-8">
      <div class="text-center">
        <h1 class="text-8">实时交通预测</h1>
      </div>
    </div>
    <div class="healthy-doc mb-4">
      <div class="file-upload">
        <!-- 文件选择 -->
        <input type="file" ref="fileInput" @change="onFileChanges" class="file-input" accept=".txt">
        <!-- 上传按钮 -->
        <el-button type="primary" round size="mini" @click="uploadFile">添&nbsp;加</el-button>
      </div>
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
import { ref } from 'vue';
import { cloneDeep, pickBy } from 'lodash-es';
import { ElMessage } from 'element-plus';
import { getRealtimeApi } from '../apis/realtime';
import axios from 'axios';

// 查询表单
const queryForm = ref({
  ID: '',
  Date: '',
  Start_time: '',
  End_time: '',
  Value: '',
  page: 1,
});

// 表格数据
const tableData = ref<any[]>([]);
const total = ref(0);

const getData = async () => {
  const queryData = cloneDeep(queryForm.value);
  const query = pickBy(queryData, (item) => item !== '' && item !== null);
  const res = (await getRealtimeApi(query)) as any;
  tableData.value = res.rows;
  total.value = res.total;
};

// 文件选择变化时处理
const selectedFile = ref<File | null>(null);
const onFileChanges = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0];
  }
};

// 上传文件
const uploadFile = async () => {
  if (!selectedFile.value) {
    ElMessage.error('请先选择一个文件');
    return;
  }
  const formData = new FormData();
  formData.append('file', selectedFile.value);

  try {
    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Axios 会自动处理边界问题
      },
    });
    if (response.data.success) { // 根据后端返回的数据结构判断成功
      ElMessage.success('文件上传成功');
      // 使用返回的数据直接更新表格和总数
      tableData.value = response.data.rows;
      total.value = response.data.total;
    } else {
      console.error('上传失败:', response.data.msg);
      ElMessage.error('文件上传失败');
    }
  } catch (error) {
    console.error('文件上传出现错误:', error);
    ElMessage.error('文件上传出现错误');
  }
};
</script>

<style scoped>
.container {
  max-width: 1000px;
  /* 最大宽度 */
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

.title h1 {
  font-size: 2rem;
  /* 标题字体大小 */
  color: #333;
  /* 标题颜色 */
  margin: 0;
  /* 去掉默认外边距 */
}

.file-upload {
  display: flex;
  align-items: center;
  gap: 10px;
  /* 按钮间距 */
}

.file-input {
  padding: 8px;
  /* 输入框内边距 */
  border: 1px solid #ddd;
  /* 边框颜色 */
  border-radius: 4px;
  /* 边角圆润 */
  transition: border-color 0.3s;
  /* 边框颜色变化动画 */
}

.file-input:focus {
  border-color: #1ba0e3;
  /* 输入框聚焦时边框颜色 */
  outline: none;
  /* 去掉默认轮廓 */
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
</style>
