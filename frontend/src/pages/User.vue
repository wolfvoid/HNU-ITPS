<template>
    <div class="container">
        <div class="title mb-8">
            <div class="text-6">用户管理</div>
        </div>
        <div class="query mb-4">
            <el-form :inline="true" :model="queryForm" class="demo-form-inline">
                <el-form-item label="用户名">
                    <el-input v-model="queryForm.username" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item label="用户ID">
                    <el-input v-model="queryForm.userid" placeholder="请输入用户编号"></el-input>
                </el-form-item>
                <el-form-item label="手机号">
                    <el-input v-model="queryForm.phonenumber" placeholder="请输入手机号"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" icon="search" @click="getData">查询</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="actions mb-4">
            <el-button icon="plus" type="warning" @click="addDialogVisible = true">添加</el-button>
        </div>
        <div class="data mb-4">
            <el-table :data="tableData" class="w-full" border>
                <el-table-column prop="userid" label="用户编号" />
                <el-table-column prop="username" label="用户名" />
                <el-table-column prop="phonenumber" label="联系电话" />
                <el-table-column label="操作" width="200">
                    <template #default="scope">
                        <el-space>
                            <el-button type="primary" icon="edit" @click="handleEdit(scope.row)">编辑</el-button>
                            <el-button type="danger" icon="delete" @click="handleDelete(scope.row)">删除</el-button>
                        </el-space>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="pagination">
            <el-pagination background layout="total, prev, pager, next" :total="total" :page-size="20"
                @current-change="getData" v-model:current-page="queryForm.page" />
        </div>
        <div class="add-dialog">
            <el-dialog title="添加用户" v-model="addDialogVisible" width="30%">
                <el-form :model="addForm" label-position="top" ref="addFormRef">
                    <el-form-item label="用户名" required prop="username">
                        <el-input v-model="addForm.username" placeholder="请输入用户名"></el-input>
                    </el-form-item>
                    <el-form-item label="用户编号" required prop="userid">
                        <el-input v-model="addForm.userid" placeholder="请输入用户编号"></el-input>
                    </el-form-item>
                    <el-form-item label="联系电话" required prop="phonenumber">
                        <el-input v-model="addForm.phonenumber" placeholder="请输入联系电话"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" icon="Check" @click="addSubmit">提交</el-button>
                    </el-form-item>
                </el-form>
            </el-dialog>
        </div>
        <div class="edit-dialog">
            <el-dialog title="修改用户记录" v-model="editDialogVisible" width="30%">
                <el-form :model="editForm" label-position="top" ref="editFormRef">
                    <el-form-item label="用户名" required prop="username">
                        <el-input v-model="editForm.username" placeholder="请输入名称"></el-input>
                    </el-form-item>
                    <el-form-item label="用户编号" required prop="userid">
                        <el-input v-model="editForm.userid" placeholder="请输入联系电话"></el-input>
                    </el-form-item>
                    <el-form-item label="联系电话" required prop="phonenumber">
                        <el-input v-model="editForm.phonenumber" placeholder="请输入联系电话"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" icon="Check" @click="editSubmit">提交</el-button>
                    </el-form-item>
                </el-form>
            </el-dialog>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import { cloneDeep, keys, pick, pickBy } from 'lodash-es'
import { ref } from 'vue'
import {
    createUserApi,
    deleteUserApi,
    getUserPageApi,
    updateUserApi
} from '../apis/user'

const queryForm = ref({
    username: '',
    userid: '',
    phonenumber: '',
    page: 1,
})

// 添加表单
const addDialogVisible = ref(false)
const addFormRef = ref<any>(null)
// 添加表单数据
const defaultAddVal = {
    userid: '',
    username: '',
    phonenumber: '',
}
const addForm = ref(cloneDeep(defaultAddVal))
// 添加提交
const addSubmit = () => {
    addFormRef.value!.validate(async (valid) => {
        if (valid) {
            const res = await createUserApi(addForm.value)
            if (res) {
                addDialogVisible.value = false
                ElMessage.success('添加成功')
                addForm.value = cloneDeep(defaultAddVal)
                getData()
            }
        } else {
            return false
        }
    })
}

// 编辑表单
const editDialogVisible = ref(false)
const editFormRef = ref<any>(null)
// 编辑表单数据
const defaultEditVal = {
    userid: '',
    username: '',
    phonenumber: '',
}
const editForm = ref(cloneDeep(defaultEditVal))
const editingUser = ref('')
// 编辑提交
const editSubmit = () => {
    editFormRef.value!.validate(async (valid) => {
        if (valid) {
            const picked = pick(editForm.value, keys(defaultEditVal))
            const dir = {
                "oldData": editingUser.value,
                "newData": picked,
            }
            const res = await updateUserApi(dir)
            if (res) {
                editDialogVisible.value = false
                ElMessage.success('编辑成功')
                editForm.value = cloneDeep(defaultEditVal)
                getData()
            }
        } else {
            return false
        }
    })
}

// 点击编辑
const handleEdit = (row) => {
    editDialogVisible.value = true
    editForm.value = cloneDeep(row)
    editingUser.value = row
}

// 删除
const handleDelete = (id) => {
    ElMessageBox.confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    })
        .then(async () => {
            await deleteUserApi(id)
            ElMessage.success('删除成功!')
            getData()
        })
        .catch(() => {
            ElMessage.info('已取消删除')
        })
}

// 表格数据
const tableData = ref<any>([])
const total = ref(0)

// 获取表格数据
const getData = async () => {
    const queryData = cloneDeep(queryForm.value)
    const query = pickBy(queryData, (item) => item !== '' && item !== null)
    const res = (await getUserPageApi(query)) as any
    tableData.value = res.rows
    total.value = res.total
}

getData()
</script>

<style scoped>
.container {
    max-width: 900px;
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

.actions {
    display: flex;
    /* 使按钮居中对齐 */
    justify-content: flex-end;
    /* 右对齐 */
}

.query {
    display: flex;
    /* 使用 flexbox 排版 */
    flex-wrap: wrap;
    /* 允许换行 */
    gap: 20px;
    /* 按钮间距 */
}

.query .el-form-item {
    margin-bottom: 0;
    /* 去掉默认外边距 */
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

.el-dialog {
    border-radius: 8px;
    /* 对话框圆角 */
}
</style>
