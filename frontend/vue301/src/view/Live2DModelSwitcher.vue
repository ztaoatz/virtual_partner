<template>
  <div class="model-switcher-container">
    <h1>Live2D 模型切换器</h1>
    
    <!-- 模型选择器 -->
    <div class="model-selector">
      <h3>选择模型：</h3>
      <div class="model-buttons">
        <button 
          v-for="(model, key) in availableModels" 
          :key="key"
          @click="switchToModel(key)"
          :class="{ active: currentModelKey === key }"
          :disabled="isLoading"
          class="model-btn"
        >
          {{ model.name }}
        </button>
      </div>
    </div>

    <!-- 画布区域 -->
    <div class="canvas-wrapper">
      <canvas id="canvas_view" style="border: 2px solid #ccc; border-radius: 10px;"></canvas>
      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <p>正在加载 {{ loadingModelName }}...</p>
      </div>
    </div>

    <!-- 控制面板 -->
    <div class="controls" v-if="modelReady && currentModelConfig">
      <div class="control-group">
        <h4>动作控制</h4>
        <button 
          v-for="motion in currentModelConfig.motions" 
          :key="motion"
          @click="playMotion(motion)"
          class="control-btn"
        >
          {{ motion }}
        </button>
      </div>
      
      <div class="control-group" v-if="currentModelConfig.expressions.length > 0">
        <h4>表情控制</h4>
        <button 
          v-for="expression in currentModelConfig.expressions" 
          :key="expression"
          @click="setExpression(expression)"
          class="control-btn expression-btn"
        >
          {{ expression }}
        </button>
      </div>
    </div>

    <!-- 状态信息 -->
    <div class="status-info">
      <div class="status-item">
        <strong>当前模型:</strong> {{ currentModelConfig?.name || '无' }}
      </div>
      <div class="status-item">
        <strong>状态:</strong> {{ status }}
      </div>
      <div class="status-item">
        <strong>模型就绪:</strong> {{ modelReady ? '是' : '否' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { initLive2DWithModel, switchModel, availableModels } from '@/utils/live2d-multi.js'

const currentModelKey = ref('nahida') // 默认使用Nahida
const currentModelConfig = ref(null)
const status = ref('等待初始化')
const modelReady = ref(false)
const isLoading = ref(false)
const loadingModelName = ref('')

let live2dApp = null
let live2dModel = null

onMounted(() => {
  initModel(currentModelKey.value)
})

const initModel = async (modelKey) => {
  try {
    isLoading.value = true
    loadingModelName.value = availableModels[modelKey]?.name || modelKey
    status.value = `正在初始化 ${loadingModelName.value}...`
    modelReady.value = false
    
    const result = await initLive2DWithModel(modelKey)
    live2dApp = result.app
    live2dModel = result.model
    currentModelConfig.value = result.config
    currentModelKey.value = modelKey
    
    modelReady.value = true
    status.value = `${result.config.name} 加载成功`
  } catch (error) {
    console.error('初始化失败:', error)
    status.value = `初始化失败: ${error.message}`
  } finally {
    isLoading.value = false
  }
}

const switchToModel = async (modelKey) => {
  if (modelKey === currentModelKey.value) return
  
  try {
    isLoading.value = true
    loadingModelName.value = availableModels[modelKey]?.name || modelKey
    status.value = `正在切换到 ${loadingModelName.value}...`
    modelReady.value = false
    
    const result = await switchModel(live2dApp, modelKey)
    live2dApp = result.app
    live2dModel = result.model
    currentModelConfig.value = result.config
    currentModelKey.value = modelKey
    
    modelReady.value = true
    status.value = `已切换到 ${result.config.name}`
  } catch (error) {
    console.error('模型切换失败:', error)
    status.value = `切换失败: ${error.message}`
  } finally {
    isLoading.value = false
  }
}

const playMotion = (motionName) => {
  if (live2dModel && live2dModel.motion) {
    live2dModel.motion(motionName)
    status.value = `播放动作: ${motionName}`
  }
}

const setExpression = (expressionName) => {
  if (live2dModel && live2dModel.expression) {
    live2dModel.expression(expressionName)
    status.value = `设置表情: ${expressionName}`
  }
}
</script>

<style scoped>
.model-switcher-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}

.model-selector {
  margin: 20px 0;
}

.model-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
  margin: 15px 0;
}

.model-btn {
  padding: 12px 24px;
  background: #e9ecef;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.model-btn:hover:not(:disabled) {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.model-btn.active {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

.model-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.canvas-wrapper {
  position: relative;
  display: inline-block;
  margin: 20px 0;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.controls {
  margin: 30px 0;
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.control-group {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  min-width: 200px;
}

.control-group h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.control-btn {
  margin: 5px;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.control-btn:hover {
  background: #0056b3;
}

.expression-btn {
  background: #6f42c1;
}

.expression-btn:hover {
  background: #5a32a3;
}

.status-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
  text-align: left;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.status-item {
  margin: 8px 0;
  font-family: monospace;
  font-size: 14px;
}
</style>
