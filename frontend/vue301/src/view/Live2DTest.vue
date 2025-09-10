<template>
  <div class="test-container">
    <h1>Live2D 简化测试</h1>
    <div class="canvas-wrapper">
      <canvas id="canvas_view" style="border: 2px solid #ccc;"></canvas>
    </div>
    <div class="controls">
      <button @click="initModel">初始化模型</button>
      <button @click="playMotion" :disabled="!modelReady">播放动作</button>
      <button @click="testExpression" :disabled="!modelReady">测试表情</button>
    </div>
    <div class="debug-info">
      <p>状态: {{ status }}</p>
      <p>模型就绪: {{ modelReady }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { initSimple } from '@/utils/live2d-simple.js'

const status = ref('等待初始化')
const modelReady = ref(false)
let live2dApp = null
let live2dModel = null

onMounted(() => {
  initModel()
})

const initModel = async () => {
  try {
    status.value = '正在初始化...'
    const result = await initSimple()
    live2dApp = result.app
    live2dModel = result.model
    modelReady.value = true
    status.value = '模型加载成功'
  } catch (error) {
    console.error('初始化失败:', error)
    status.value = '初始化失败: ' + error.message
  }
}

const playMotion = () => {
  if (live2dModel) {
    live2dModel.motion('Idle')
    status.value = '播放动作: Idle'
  }
}

const testExpression = () => {
  if (live2dModel && live2dModel.expression) {
    live2dModel.expression('Happy1')
    status.value = '设置表情: Happy1'
  }
}
</script>

<style scoped>
.test-container {
  padding: 20px;
  text-align: center;
}

.canvas-wrapper {
  margin: 20px auto;
  display: inline-block;
}

.controls {
  margin: 20px 0;
}

.controls button {
  margin: 0 10px;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.controls button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.controls button:hover:not(:disabled) {
  background: #0056b3;
}

.debug-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
  margin: 20px auto;
  max-width: 400px;
}

.debug-info p {
  margin: 5px 0;
  font-family: monospace;
}
</style>
