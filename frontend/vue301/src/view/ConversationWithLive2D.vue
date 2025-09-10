<template>
  <div class="conversation-container">
    <!-- 云朵装饰背景 -->
    <div class="cloud-decorations">
      <div class="cloud cloud1">☁</div>
      <div class="cloud cloud2">☁</div>
      <div class="cloud cloud3">☁</div>
      <div class="cloud cloud4">☁</div>
      <div class="cloud cloud5">☁</div>
    </div>

    <!-- 虚拟伙伴形象区域 - 使用Live2D -->
    <div class="virtual-partner-area">
      <div class="partner-avatar" :class="{ 'speaking': isAISpeaking, 'listening': isListening }">
        <div class="live2d-container">
          <!-- Live2D模型替换静态图片 -->
          <Live2DCanvas 
            ref="live2dRef"
            :width="300"
            :height="400"
            :scale="0.25"
            :modelPath="'/live2d/Nahida_1080/Nahida_1080.model3.json'"
          />
          
          <!-- 说话时的声波效果覆盖层 -->
          <div v-if="isAISpeaking" class="sound-waves-overlay">
            <div class="wave wave1"></div>
            <div class="wave wave2"></div>
            <div class="wave wave3"></div>
          </div>
        </div>
        
        <!-- 伙伴状态文本 -->
        <div class="partner-status" v-if="partnerStatus">
          {{ partnerStatus }}
        </div>
      </div>
    </div>

    <!-- 对话文本显示区域 -->
    <div class="conversation-text" :class="{ 'minimized': !showText }">
      <transition-group name="message" tag="div" class="messages-container">
        <div 
          v-for="message in recentMessages" 
          :key="message.id"
          class="message-bubble"
          :class="{ 'user': message.isUser, 'ai': !message.isUser }"
        >
          <div class="message-content">{{ message.text }}</div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </transition-group>
    </div>

    <!-- 控制面板 -->
    <div class="control-panel">
      <!-- 语音控制 -->
      <div class="voice-controls">
        <button 
          @click="toggleRecording" 
          :class="{ 'recording': isRecording, 'listening': isListening }"
          class="voice-button"
          :disabled="isAISpeaking"
        >
          <span v-if="!isRecording && !isListening">🎤</span>
          <span v-else-if="isListening">👂</span>
          <span v-else>⏹</span>
        </button>
        
        <!-- 停止AI语音按钮 -->
        <button 
          v-if="isAISpeaking" 
          @click="stopAISpeech"
          class="stop-button"
        >
          ⏹ 停止
        </button>
      </div>

      <!-- Live2D控制 -->
      <div class="live2d-controls">
        <button @click="triggerHappyExpression" class="emotion-btn">😊</button>
        <button @click="triggerSadExpression" class="emotion-btn">😢</button>
        <button @click="triggerSurpriseExpression" class="emotion-btn">😲</button>
        <button @click="triggerRandomMotion" class="motion-btn">动作</button>
      </div>

      <!-- 文本控制 -->
      <div class="text-controls">
        <button @click="toggleText" class="toggle-button">
          {{ showText ? '隐藏文本' : '显示文本' }}
        </button>
        <button @click="clearMessages" class="clear-button">清除记录</button>
      </div>
    </div>

    <!-- 状态指示器 -->
    <div class="status-indicator">
      <div v-if="isRecording" class="status-item recording">🔴 录音中...</div>
      <div v-if="isListening" class="status-item listening">👂 识别中...</div>
      <div v-if="isAISpeaking" class="status-item speaking">🗣 AI回答中...</div>
      <div v-if="isProcessing" class="status-item processing">⚙ 处理中...</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, watch } from 'vue'
import Live2DCanvas from '@/components/Live2DCanvas.vue'

// Live2D相关
const live2dRef = ref(null)

// 状态管理
const isRecording = ref(false)
const isListening = ref(false)
const isAISpeaking = ref(false)
const isProcessing = ref(false)
const showText = ref(true)
const partnerStatus = ref('等待中...')
const currentEmotion = ref('neutral')

// 消息管理
const recentMessages = ref([])
let messageIdCounter = 0

// 语音识别和合成
let recognition = null
let speechSynthesis = window.speechSynthesis

// 初始化
onMounted(() => {
  initSpeechRecognition()
})

// 清理资源
onBeforeUnmount(() => {
  if (recognition) {
    recognition.stop()
  }
  if (speechSynthesis) {
    speechSynthesis.cancel()
  }
})

// 初始化语音识别
const initSpeechRecognition = () => {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition = new SpeechRecognition()
    
    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = 'zh-CN'
    
    recognition.onstart = () => {
      isListening.value = true
      partnerStatus.value = '正在倾听...'
    }
    
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      addMessage(transcript, true)
      processUserInput(transcript)
    }
    
    recognition.onerror = (event) => {
      console.error('语音识别错误:', event.error)
      isListening.value = false
      isRecording.value = false
      partnerStatus.value = '识别失败，请重试'
    }
    
    recognition.onend = () => {
      isListening.value = false
      isRecording.value = false
    }
  }
}

// 切换录音状态
const toggleRecording = () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

// 开始录音
const startRecording = () => {
  if (recognition && !isRecording.value && !isAISpeaking.value) {
    try {
      recognition.start()
      isRecording.value = true
      partnerStatus.value = '开始录音...'
      
      // 触发Live2D倾听动作
      if (live2dRef.value) {
        live2dRef.value.playMotion('TapHead')
      }
    } catch (error) {
      console.error('录音启动失败:', error)
      partnerStatus.value = '录音启动失败'
    }
  }
}

// 停止录音
const stopRecording = () => {
  if (recognition && isRecording.value) {
    recognition.stop()
    isRecording.value = false
    partnerStatus.value = '处理中...'
  }
}

// 处理用户输入
const processUserInput = async (text) => {
  isProcessing.value = true
  partnerStatus.value = '思考中...'
  
  try {
    // 这里应该调用您的AI API
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const aiResponse = `我理解您说的"${text}"，这是一个模拟回复。`
    addMessage(aiResponse, false)
    speakText(aiResponse)
    
    // 触发Live2D开心表情
    triggerHappyExpression()
    
  } catch (error) {
    console.error('处理失败:', error)
    const errorMessage = '抱歉，我现在无法回答您的问题。'
    addMessage(errorMessage, false)
    speakText(errorMessage)
  } finally {
    isProcessing.value = false
  }
}

// 添加消息
const addMessage = (text, isUser) => {
  const message = {
    id: ++messageIdCounter,
    text,
    isUser,
    timestamp: new Date()
  }
  
  recentMessages.value.push(message)
  
  // 只保留最近10条消息
  if (recentMessages.value.length > 10) {
    recentMessages.value.shift()
  }
}

// 语音合成
const speakText = (text) => {
  if (speechSynthesis) {
    speechSynthesis.cancel() // 停止之前的语音
    
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'zh-CN'
    utterance.rate = 0.9
    utterance.pitch = 1.1
    
    utterance.onstart = () => {
      isAISpeaking.value = true
      partnerStatus.value = '正在回答...'
      
      // 触发Live2D说话动作
      if (live2dRef.value) {
        live2dRef.value.playMotion('TapBody')
      }
    }
    
    utterance.onend = () => {
      isAISpeaking.value = false
      partnerStatus.value = '等待中...'
    }
    
    utterance.onerror = () => {
      isAISpeaking.value = false
      partnerStatus.value = '语音播放失败'
    }
    
    speechSynthesis.speak(utterance)
  }
}

// 停止AI语音
const stopAISpeech = () => {
  if (speechSynthesis) {
    speechSynthesis.cancel()
    isAISpeaking.value = false
    partnerStatus.value = '等待中...'
  }
}

// Live2D表情控制
const triggerHappyExpression = () => {
  if (live2dRef.value) {
    live2dRef.value.setExpression('Happy1')
    currentEmotion.value = 'happy'
  }
}

const triggerSadExpression = () => {
  if (live2dRef.value) {
    live2dRef.value.setExpression('Sad1')
    currentEmotion.value = 'sad'
  }
}

const triggerSurpriseExpression = () => {
  if (live2dRef.value) {
    live2dRef.value.setExpression('StarEye')
    currentEmotion.value = 'surprise'
  }
}

const triggerRandomMotion = () => {
  if (live2dRef.value) {
    const motions = ['Idle', 'TapBody', 'TapHead']
    const randomMotion = motions[Math.floor(Math.random() * motions.length)]
    live2dRef.value.playMotion(randomMotion)
  }
}

// 工具函数
const toggleText = () => {
  showText.value = !showText.value
}

const clearMessages = () => {
  recentMessages.value = []
}

const formatTime = (timestamp) => {
  return timestamp.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}
</script>

<style scoped>
.conversation-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 云朵装饰 */
.cloud-decorations {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.cloud {
  position: absolute;
  color: rgba(255, 255, 255, 0.3);
  font-size: 2em;
  animation: float 6s ease-in-out infinite;
}

.cloud1 { top: 10%; left: 10%; animation-delay: 0s; }
.cloud2 { top: 20%; right: 15%; animation-delay: 2s; }
.cloud3 { top: 60%; left: 5%; animation-delay: 4s; }
.cloud4 { top: 70%; right: 20%; animation-delay: 1s; }
.cloud5 { top: 40%; left: 80%; animation-delay: 3s; }

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* 虚拟伙伴区域 */
.virtual-partner-area {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.partner-avatar {
  position: relative;
  transition: transform 0.3s ease;
}

.partner-avatar.speaking {
  transform: scale(1.05);
}

.partner-avatar.listening {
  transform: scale(1.02);
}

.live2d-container {
  position: relative;
  width: 300px;
  height: 400px;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

/* 声波效果覆盖层 */
.sound-waves-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.wave {
  position: absolute;
  border: 2px solid #4CAF50;
  border-radius: 50%;
  opacity: 0;
  animation: ripple 2s infinite;
}

.wave1 { animation-delay: 0s; }
.wave2 { animation-delay: 0.5s; }
.wave3 { animation-delay: 1s; }

@keyframes ripple {
  0% {
    width: 10px;
    height: 10px;
    opacity: 1;
  }
  100% {
    width: 100px;
    height: 100px;
    opacity: 0;
  }
}

.partner-status {
  text-align: center;
  margin-top: 15px;
  color: white;
  font-size: 16px;
  background: rgba(0, 0, 0, 0.3);
  padding: 8px 16px;
  border-radius: 15px;
  backdrop-filter: blur(5px);
}

/* 对话文本区域 */
.conversation-text {
  position: fixed;
  bottom: 120px;
  left: 20px;
  right: 20px;
  max-height: 200px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  z-index: 3;
}

.conversation-text.minimized {
  transform: translateY(100%);
}

.messages-container {
  max-height: 150px;
  overflow-y: auto;
}

.message-bubble {
  margin: 8px 0;
  padding: 10px 15px;
  border-radius: 15px;
  max-width: 80%;
  word-wrap: break-word;
}

.message-bubble.user {
  background: #007bff;
  color: white;
  margin-left: auto;
  text-align: right;
}

.message-bubble.ai {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  margin-right: auto;
}

.message-content {
  font-size: 14px;
  line-height: 1.4;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 4px;
}

/* 控制面板 */
.control-panel {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 25px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 4;
}

.voice-controls, .live2d-controls, .text-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.voice-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: #4CAF50;
  color: white;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.voice-button:hover {
  transform: scale(1.1);
}

.voice-button.recording {
  background: #f44336;
  animation: pulse 1s infinite;
}

.voice-button.listening {
  background: #ff9800;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.emotion-btn, .motion-btn, .toggle-button, .clear-button, .stop-button {
  padding: 8px 12px;
  border: none;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  transition: background 0.3s ease;
}

.emotion-btn:hover, .motion-btn:hover, .toggle-button:hover, .clear-button:hover, .stop-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.stop-button {
  background: #f44336;
}

/* 状态指示器 */
.status-indicator {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 5;
}

.status-item {
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 12px;
  border-radius: 15px;
  margin: 5px 0;
  font-size: 14px;
}

/* 消息动画 */
.message-enter-active, .message-leave-active {
  transition: all 0.3s ease;
}

.message-enter-from, .message-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
