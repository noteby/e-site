<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-if="$route.meta.requiresAuth">管理</el-breadcrumb-item>
    <el-breadcrumb-item v-else></el-breadcrumb-item>
    <el-breadcrumb-item> {{ $route.meta.desc || '?' }}</el-breadcrumb-item>
  </el-breadcrumb>
</template>
