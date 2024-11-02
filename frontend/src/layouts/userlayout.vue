<template>
    <div>
        <el-container class="h-screen">
            <el-header class="!p-0 fixed w-full z-10 b-b b-slate-700 b-solid">
                <div class="flex h-full justify-between items-center px-2 bg-slate-700 text-light-50 ">
                    <div class="flex items-center">
                        <div>
                            <img src="/book.svg" alt="" class="w-[45px] h-[45px]" />
                        </div>
                        <div class="ml-2 text-6">智慧交通预测系统</div>
                    </div>
                    <div class="flex-grow"></div>
                    <div class="flex justify-center items-center">
                        <div class="text-5 mr-2">{{ user.username }} </div>
                        <el-button @click="handleEdit" size="small" type="primary">修改密码</el-button>
                        <el-button @click="handleLogout" size="small" type="danger">退出</el-button>   
                    </div>
                </div>
            </el-header>
            <el-container class="mt-[60px]">
                <el-aside width="150px" class="fixed pt-[60px] top-0 bottom-0 overflow-y-auto overflow-x-hidden">
                    <el-menu active-text-color="#569cd6" background-color="#475569"
                        class="aside w-[200px] min-h-full overscroll-auto" default-active="/" text-color="#fff"
                        :router="true">
                        <el-menu-item index="/">
                            <el-icon>
                                <House />
                            </el-icon>
                            <span>首页</span>
                        </el-menu-item>
                        <el-menu-item index="/u/pre">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <span>交通预测一览</span>
                        </el-menu-item>

                        <el-menu-item index="/u/realtime">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <span>实时交通预测</span>
                        </el-menu-item>

                        <el-menu-item index="/u/vision">
                            <el-icon>
                                <EditPen />
                            </el-icon>
                            <span>可视化界面</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main class="ml-[200px]">
                    <router-view />
                </el-main>
            </el-container>
        </el-container>
        <div class="edit-dialog">
            <el-dialog title="修改密码，嚣张滴不要" v-model="editDialogVisible" width="30%">
                <el-form :model="editForm" label-position="top" ref="editFormRef">
                    <el-form-item label="姓名" required prop="username">
                        <el-input v-model="editForm.username" disabled></el-input>
                    </el-form-item>
                    <el-form-item label="学号" required prop="userid">
                        <el-input v-model="editForm.userid" disabled></el-input>
                    </el-form-item>
                    <el-form-item label="密码" required prop="password">
                        <el-input v-model="editForm.password" placeholder="请输入密码"></el-input>
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
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus';
import { cloneDeep, keys, pick, pickBy } from 'lodash-es';
import { updateUserPasswordApi } from '../apis/password';
import { EditPen } from '@element-plus/icons-vue';

const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const handleLogout = () => {
    localStorage.removeItem('user')
    location.reload()
}
// 编辑表单
const editDialogVisible = ref(false)
const editFormRef = ref<any>(null)
// 编辑表单数据
const defaultEditVal = {
    userid: user.value.userid,
    username: user.value.name,
    password: '',
}
const editForm = ref(cloneDeep(defaultEditVal))
const editingBook = ref('')
// 编辑提交
const editSubmit = () => {
    editFormRef.value!.validate(async (valid) => {
        if (valid) {
            //只能修改 defaultEditVal 中的值
            const picked = pick(editForm.value, keys(defaultEditVal))
            const dir = {
                "oldData": editingBook.value,
                "newData": picked,
            }
            const res = await updateUserPasswordApi(dir)
            if (res) {
                editDialogVisible.value = false
                ElMessage.success('编辑成功')
                editForm.value = cloneDeep(defaultEditVal)
            }
        } else {
            return false
        }
    })
}

// 点击编辑
const handleEdit = () => {
    const row: any = {}
    row["username"] = user.value.username
    row["userid"] = user.value.userid
    editDialogVisible.value = true
    editForm.value = row
    editingBook.value = user.value
}

</script>
<style scoped>
.bg-green-500 {
  background-color: #34D399; /* 将颜色更改为您想要的绿色 */
}

.text-green-500 {
  color: #34D399; /* 将颜色更改为您想要的绿色 */
}

</style>
