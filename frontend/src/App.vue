<script setup lang="ts"></script>

<template>
    <div>
        <router-view />
        <!-- <el-container class="h-screen">
            <el-header class="p-0 fixed w-full z-1 b-b b-slate-700 b-solid">
                <div
                    class="flex h-full justify-between items-center px-2 bg-slate-700 text-light-50 "
                >
                    <div>
                        <div class="text-6">停车场管理系统</div>
                    </div>
                    <div class="flex-grow" />
                    <div>用户名</div>
                </div>
            </el-header>
            <el-container class="mt-[60px]">
                <el-aside width="200px" class="fixed top-[60px] bottom-0">
                    <el-menu
                        active-text-color="#569cd6"
                        background-color="#475569"
                        class="aside w-[200px] h-full"
                        default-active="/"
                        text-color="#fff"
                        :router="true"
                    >
                        <el-menu-item index="/">
                            <el-icon> <House /></el-icon>
                            <span>首页</span>
                        </el-menu-item>
                        <el-menu-item index="/user">
                            <el-icon> <House /></el-icon>
                            <span>用户管理</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main class="ml-[200px]">
                    <router-view />
                </el-main>
            </el-container>
        </el-container> -->
    </div>
</template>

<style scoped></style>
