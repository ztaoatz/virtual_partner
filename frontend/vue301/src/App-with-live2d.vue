<template>
  <div>
    <!-- Live2D背景层 -->
    <div class="live2d-background" style="width:100%;height:100%;z-index: -1000;">
      <canvas id="canvas_view"></canvas>
    </div>
    
    <!-- 主要内容 -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import { initRouter } from "./utils/permission";
import router from "./router";
import { init, destroy } from "./utils/live2d-init";

let pixiApp = null;

// 解决刷新页面，页面空白的问题
onMounted(async () => {
  await initRouter();
  // 获取路由 path 地址，并跳转
  router.replace(router.options.history.location);
  
  // 初始化Live2D模型作为背景
  try {
    const result = await init({
      modelPath: '/live2d/Nahida_1080/Nahida_1080.model3.json',
      canvasId: 'canvas_view',
      width: window.innerWidth,
      height: window.innerHeight,
      transparent: true
    });
    
    pixiApp = result.app;
    console.log('Live2D背景模型初始化成功');
    
    // 监听窗口大小变化
    const handleResize = () => {
      if (pixiApp) {
        pixiApp.renderer.resize(window.innerWidth, window.innerHeight);
      }
    };
    
    window.addEventListener('resize', handleResize);
    
    // 清理函数
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize);
      if (pixiApp) {
        destroy(pixiApp);
      }
    });
    
  } catch (error) {
    console.error('Live2D背景模型初始化失败:', error);
  }
});
</script>

<style>
.live2d-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1000;
  pointer-events: none; /* 让背景不影响页面交互 */
}

#canvas_view {
  width: 100%;
  height: 100%;
  display: block;
}

/* 确保主要内容在Live2D之上 */
.router-view {
  position: relative;
  z-index: 1;
}
</style>
