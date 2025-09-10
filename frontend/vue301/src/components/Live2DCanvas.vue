<template>
  <div class="live2d-container" style="width:100%;height:100%;z-index: -1000;">
    <canvas :id="canvasId"></canvas>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { init, destroy } from '@/utils/live2d-init.js'

// 生成唯一的canvas ID
const canvasId = `canvas_view_${Math.random().toString(36).substr(2, 9)}`

// 定义props
const props = defineProps({
  modelPath: {
    type: String,
    default: '/live2d/Nahida_1080/Nahida_1080.model3.json' // 改为默认使用Nahida
  },
  width: {
    type: Number,
    default: 1920
  },
  height: {
    type: Number,
    default: 1080
  },
  scale: {
    type: Number,
    default: 0.15 // 调整默认缩放
  }
})

const pixiApp = ref(null)
const live2dModel = ref(null)

// 组件挂载时初始化Live2D
onMounted(async () => {
  console.log('Live2DCanvas组件开始挂载, canvasId:', canvasId);
  console.log('Props:', props);
  
  // 等待DOM渲染完成
  await new Promise(resolve => setTimeout(resolve, 100));
  
  try {
    const result = await init({
      modelPath: props.modelPath,
      canvasId: canvasId,
      width: props.width,
      height: props.height,
      transparent: true
    })
    pixiApp.value = result.app
    live2dModel.value = result.model
    
    // 应用传入的配置
    if (live2dModel.value) {
      live2dModel.value.scale.set(props.scale)
      console.log('模型缩放设置为:', props.scale);
    }
    
    console.log('Live2D组件初始化成功')
  } catch (error) {
    console.error('Live2D组件初始化失败:', error)
  }
})

// 组件卸载时清理资源
onUnmounted(() => {
  if (pixiApp.value) {
    destroy(pixiApp.value)
  }
})

// 暴露方法给父组件使用
defineExpose({
  playMotion: (motionGroup, index = 0) => {
    if (live2dModel.value) {
      live2dModel.value.motion(motionGroup, index)
    }
  },
  setExpression: (expressionName) => {
    if (live2dModel.value) {
      live2dModel.value.expression(expressionName)
    }
  },
  getModel: () => live2dModel.value,
  getApp: () => pixiApp.value
})
</script>

<style scoped>
.live2d-container {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

canvas {
  width: 100%;
  height: 100%;
  display: block;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1); /* 添加背景色以便调试 */
}
</style>
