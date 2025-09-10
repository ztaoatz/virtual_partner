<template>
  <div class="page-container">
    <!-- 页面主要内容 -->
    <div class="main-content">
      <h1>这是一个带Live2D的页面</h1>
      <p>Live2D模型会显示在右侧</p>
      
      <div class="content-area">
        <p>您可以在这里放置任何内容...</p>
        <button @click="interactWithModel">与模型互动</button>
      </div>
    </div>
      <!-- Live2D模型区域 -->
    <div class="live2d-area">      <Live2DCanvas 
        ref="live2dRef"
        :width="400"
        :height="600"
        :scale="0.15"
        :modelPath="'/live2d/Nahida_1080/Nahida_1080.model3.json'"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Live2DCanvas from '@/components/Live2DCanvas.vue'

const live2dRef = ref(null)

// 与模型互动
const interactWithModel = () => {
  if (live2dRef.value) {
    // 随机播放动作
    const motions = ['Idle', 'TapBody', 'TapHead']
    const randomMotion = motions[Math.floor(Math.random() * motions.length)]
    live2dRef.value.playMotion(randomMotion)
    
    console.log(`播放动作: ${randomMotion}`)
  }
}
</script>

<style scoped>
.page-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-content {
  flex: 1;
  padding: 40px;
  color: white;
}

.main-content h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

.content-area {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  margin-top: 30px;
}

.content-area button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

.content-area button:hover {
  background: #45a049;
}

.live2d-area {
  width: 400px;
  height: 600px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
