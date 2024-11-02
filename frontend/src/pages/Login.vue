<template>
    <div>
        <div class="max-w-[400px] mx-auto mt-[100px] p-4">
            <div
                class="title text-6 mb-12 text-center flex justify-center items-center"
            >
                <div class="mr-4">
                    <img class="w-[40px] h-[40px]" src="/book.svg" />
                </div>
                <div>智慧交通预测系统</div>
            </div>
            <el-card shadow="never">
                <el-form
                    label-width="100"
                    :model="loginForm"
                    label-position="top"
                    ref="loginFromRef"
                >
                    <el-form-item label="用户类型">
                        <el-radio-group v-model="loginForm.type">
                            <el-radio :label="0">管理员</el-radio>
                            <el-radio :label="1">用户</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="账号" prop="userid" required>
                        <el-input v-model="loginForm.userid"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password" required>
                        <el-input
                            type="password"
                            v-model="loginForm.password"
                        ></el-input>
                    </el-form-item>
                    <div class="flex justify-center mt-8">
                        <el-button type="primary" size="large" icon="Check"
                            @click="hadleLogin"
                            >登录</el-button
                        >
                    </div>
                </el-form>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { postLoginApi } from '../apis/login';
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loginFromRef = ref(null)
const loginForm = ref({
    type: 0, // 0: 管理员 1: 用户
    username: 'postgres',
    userid:'123',
    password: '',
})

const hadleLogin = () => {
    loginFromRef.value.validate(async (valid) => {
        if (valid) {
            const res = await postLoginApi(loginForm.value) as any
            if(res) {
                ElMessage.success('登录成功')
                localStorage.setItem('user', JSON.stringify(res))
                const to = res.type === 0 ? '/' : '/u'
                router.push(to)
            }
            else {
                ElMessage.error('登录失败')
            }
        }
    })
}
</script>

<style scoped></style>
