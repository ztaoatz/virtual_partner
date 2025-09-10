<template>
  <div class="live2d-demo">
    <h1>Live2D 模型演示</h1>
    
    <!-- Live2D组件 -->
    <div class="model-container">
      <Live2DCanvas 
        ref="live2dRef"
        :modelPath="currentModel"
        :scale="0.4"
        :width="800"
        :height="600"
      />
    </div>
    
    <!-- 控制面板 -->
    <div class="control-panel">
      <div class="control-group">
        <h3>模型选择</h3>
        <select v-model="currentModel" @change="switchModel">
          <option value="/live2d/Nahida_1080/Nahida_1080.model3.json">Nahida</option>
          <option value="/live2d/miku/runtime/miku.model3.json">Miku</option>
          <option value="/live2d/Mahiro_GG/runtime/Mahiro_GG.model3.json">Mahiro</option>
        </select>
      </div>
      
      <div class="control-group">
        <h3>动作控制</h3>
        <button @click="playMotion('Idle')">播放待机动作</button>
        <button @click="playMotion('TapBody')">点击身体</button>
        <button @click="playMotion('TapHead')">点击头部</button>
      </div>
      
      <div class="control-group">
        <h3>表情控制</h3>
        <button @click="setExpression('Happy1')">开心</button>
        <button @click="setExpression('Sad1')">难过</button>
        <button @click="setExpression('Angry')">生气</button>
        <button @click="setExpression('Shy')">害羞</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Live2DCanvas from '@/components/Live2DCanvas.vue'

const live2dRef = ref(null)
const currentModel = ref('/live2d/Nahida_1080/Nahida_1080.model3.json')

// 播放动作
const playMotion = (motionName) => {
  if (live2dRef.value) {
    live2dRef.value.playMotion(motionName)
    console.log(`播放动作: ${motionName}`)
  }
}

// 设置表情
const setExpression = (expressionName) => {
  if (live2dRef.value) {
    live2dRef.value.setExpression(expressionName)
    console.log(`设置表情: ${expressionName}`)
  }
}

// 切换模型
const switchModel = () => {
  console.log(`切换模型到: ${currentModel.value}`)
  // 注意：切换模型需要重新初始化组件
  // 这里可以通过key来强制重新渲染组件
}
</script>

<style scoped>
.live2d-demo {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.model-container {
  width: 800px;
  height: 600px;
  margin: 20px auto;
  border: 2px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
  background: linear-gradient(45deg, #f0f8ff, #e6f3ff);
}

.control-panel {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 20px;
}

.control-group {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  min-width: 200px;
}

.control-group h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.control-group button,
.control-group select {
  margin: 5px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
}

.control-group button:hover {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.control-group select {
  width: 100%;
  margin-bottom: 10px;
}
</style>
