<template>
  <div class="live2d-container" style="width:100%;height:100%;z-index: -1000;">
    <canvas id="canvas_view"></canvas>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { init, destroy } from '@/utils/live2d-init.js'

// 定义props
const props = defineProps({
  modelPath: {
    type: String,
    default: '/live2d/Nahida_1080/Nahida_1080.model3.json'
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
    default: 0.3
  }
})

const pixiApp = ref(null)
const live2dModel = ref(null)

// 组件挂载时初始化Live2D
onMounted(async () => {
  try {
    const result = await init()
    pixiApp.value = result.app
    live2dModel.value = result.model
    
    // 应用传入的配置
    if (live2dModel.value) {
      live2dModel.value.scale.set(props.scale)
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
}

#canvas_view {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
