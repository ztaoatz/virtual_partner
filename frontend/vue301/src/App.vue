<template>
  <div>
    <!-- Live2D背景层 -->
    <div style="width:100%;height:100%;z-index: -1000;">
      <canvas id="canvas_view"></canvas>
    </div>
    
    <!-- 主要内容 -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { initRouter } from "./utils/permission";
import router from "./router";
import { init } from './components/index'

// 解决刷新页面，页面空白的问题
onMounted(async () => {
  await initRouter();
  // 获取路由 path 地址，并跳转
  router.replace(router.options.history.location);
  
  // 注意一定要在mounted钩子执行，不然拿不到节点，会报错
  try {
    await init();
    console.log('Live2D背景模型加载成功');
  } catch (error) {
    console.error('Live2D背景模型加载失败:', error);
  }
});
</script>
