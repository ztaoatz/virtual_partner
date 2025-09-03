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

    <!-- 虚拟伙伴形象区域 -->
    <div class="virtual-partner-area">
      <div class="partner-avatar" :class="{ 'speaking': isAISpeaking, 'listening': isListening }">
        <div class="avatar-container">
          <img src="@/assets/linxi.png" alt="灵犀" class="avatar-image" />
          <div class="expression-overlay" :class="currentEmotion"></div>
          
          <!-- 说话时的声波效果 -->
          <div v-if="isAISpeaking" class="sound-waves">
            <div class="wave wave1"></div>
            <div class="wave wave2"></div>
            <div class="wave wave3"></div>
          </div>
          
          <!-- 倾听时的呼吸效果 -->
          <div v-if="!isAISpeaking && !isListening" class="breathing-glow"></div>
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

    <!-- 交互控制区域 -->
    <div class="interaction-area">
      <!-- 主要麦克风按钮 -->
      <div class="mic-container">
        <button 
          @click="toggleRecording"
          @mousedown="startPress"
          @mouseup="endPress"
          @mouseleave="endPress"
          :class="{ 
            'recording': isRecording, 
            'processing': isProcessing,
            'pressed': isPressed 
          }"
          class="mic-button"
          :disabled="isProcessing"
        >
          <!-- 麦克风图标 -->
          <div class="mic-icon" v-if="!isRecording && !isProcessing">
            <svg viewBox="0 0 24 24" width="32" height="32">
              <path d="M12 2C13.1 2 14 2.9 14 4V11C14 12.1 13.1 13 12 13S10 12.1 10 11V4C10 2.9 10.9 2 12 2M19 11C19 14.53 16.39 17.44 13 17.93V21H11V17.93C7.61 17.44 5 14.53 5 11H7C7 13.76 9.24 16 12 16S17 13.76 17 11H19Z" fill="currentColor"/>
            </svg>
          </div>
          
          <!-- 录音时的声波动画 -->
          <div class="recording-animation" v-if="isRecording">
            <div class="recording-wave recording-wave1"></div>
            <div class="recording-wave recording-wave2"></div>
            <div class="recording-wave recording-wave3"></div>
            <div class="recording-wave recording-wave4"></div>
          </div>
          
          <!-- 处理中的加载动画 -->
          <div class="processing-spinner" v-if="isProcessing">
            <div class="spinner-ring"></div>
          </div>
        </button>
        
        <!-- 录音状态提示 -->
        <div class="recording-hint" v-if="isRecording">
          <div class="pulse-dot"></div>
          <span>正在倾听...</span>
        </div>
      </div>
    </div>

    <!-- 最小化的设置入口 -->
    <div class="settings-entry" @click="openSettings">
      <svg viewBox="0 0 24 24" width="20" height="20">
        <path d="M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" fill="currentColor"/>
      </svg>
    </div>

    <!-- 文本显示切换按钮 -->
    <div class="text-toggle" @click="toggleText">
      <svg viewBox="0 0 24 24" width="18" height="18">
        <path d="M9,22A1,1 0 0,1 8,21V18H4A2,2 0 0,1 2,16V4C2,2.89 2.9,2 4,2H20A2,2 0 0,1 22,4V16A2,2 0 0,1 20,18H13.9L10.2,21.71C10,21.9 9.75,22 9.5,22H9M4,4V16H8.5L12,19.5V16H20V4H4Z" fill="currentColor"/>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

// 响应式数据
const isRecording = ref(false)
const isProcessing = ref(false)
const isListening = ref(false)
const isAISpeaking = ref(false)
const isPressed = ref(false)
const showText = ref(true)
const currentEmotion = ref('neutral')
const partnerStatus = ref('准备就绪，随时为您服务')

// 消息数据
const messages = reactive([])
const recentMessages = computed(() => {
  return messages.slice(-4) // 只显示最近4条消息
})

// 录音相关
let mediaRecorder = null
let audioStream = null
let recordingTimeout = null

// 方法
const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

const startRecording = async () => {
  try {
    isRecording.value = true
    isListening.value = true
    partnerStatus.value = '我在认真倾听...'
    
    // 获取音频流
    audioStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(audioStream)
    
    const audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }
    
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
      await processAudio(audioBlob)
    }
    
    mediaRecorder.start()
    
    // 30秒后自动停止录音
    recordingTimeout = setTimeout(() => {
      if (isRecording.value) {
        stopRecording()
      }
    }, 30000)
    
  } catch (error) {
    console.error('录音启动失败:', error)
    alert('麦克风访问失败，请检查权限设置')
    resetRecordingState()
  }
}

const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop()
  }
  
  if (audioStream) {
    audioStream.getTracks().forEach(track => track.stop())
  }
  
  if (recordingTimeout) {
    clearTimeout(recordingTimeout)
  }
  
  isRecording.value = false
  isListening.value = false
  isProcessing.value = true
  partnerStatus.value = '正在思考...'
}

const processAudio = async (audioBlob) => {
  try {
    // 模拟语音识别和AI处理
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      text: '这是一条模拟的用户语音转文字内容',
      isUser: true,
      timestamp: new Date()
    }
    messages.push(userMessage)
    
    // 模拟AI回复
    setTimeout(async () => {
      isAISpeaking.value = true
      currentEmotion.value = 'happy'
      partnerStatus.value = '正在回复中...'
      
      const aiMessage = {
        id: Date.now() + 1,
        text: '我理解您的想法，让我为您提供一些建议...',
        isUser: false,
        timestamp: new Date()
      }
      messages.push(aiMessage)
      
      // 模拟AI说话时间
      setTimeout(() => {
        isAISpeaking.value = false
        currentEmotion.value = 'neutral'
        partnerStatus.value = '我在这里，请继续交流'
        isProcessing.value = false
      }, 3000)
      
    }, 500)
    
  } catch (error) {
    console.error('音频处理失败:', error)
    alert('语音处理失败，请重试')
    resetRecordingState()
  }
}

const resetRecordingState = () => {
  isRecording.value = false
  isListening.value = false
  isProcessing.value = false
  isAISpeaking.value = false
  partnerStatus.value = '准备就绪，随时为您服务'
}

const startPress = () => {
  isPressed.value = true
}

const endPress = () => {
  isPressed.value = false
}

const toggleText = () => {
  showText.value = !showText.value
}

const openSettings = () => {
  // 跳转到设置页面或打开设置模态框
  console.log('打开设置')
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 生命周期
onMounted(() => {
  // 初始化欢迎消息
  messages.push({
    id: 1,
    text: '你好！我是灵犀，您的AI伙伴。点击下方的麦克风按钮开始我们的对话吧！',
    isUser: false,
    timestamp: new Date()
  })
})

onUnmounted(() => {
  if (audioStream) {
    audioStream.getTracks().forEach(track => track.stop())
  }
  if (recordingTimeout) {
    clearTimeout(recordingTimeout)
  }
})
</script>

<style scoped>
.conversation-container {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    #fef7f0 0%,    /* 温暖的米色 */
    #fdf2e6 25%,   /* 奶油色 */
    #f8f4f0 50%,   /* 浅米色 */
    #e8f4fd 75%,   /* 淡天空蓝 */
    #d4e7f4 100%   /* 柔和蓝色 */
  );
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 云朵装饰 */
.cloud-decorations {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.cloud {
  position: absolute;
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.4);
  animation: cloudFloat 12s ease-in-out infinite;
}

.cloud1 {
  top: 10%;
  left: 5%;
  animation-delay: 0s;
}

.cloud2 {
  top: 20%;
  right: 10%;
  animation-delay: 3s;
  font-size: 1.5rem;
}

.cloud3 {
  bottom: 25%;
  left: 8%;
  animation-delay: 6s;
  font-size: 1.8rem;
}

.cloud4 {
  bottom: 15%;
  right: 5%;
  animation-delay: 9s;
  font-size: 1.6rem;
}

.cloud5 {
  top: 50%;
  left: 15%;
  animation-delay: 12s;
  font-size: 1.3rem;
}

@keyframes cloudFloat {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-15px) translateX(10px);
    opacity: 0.6;
  }
}

/* 虚拟伙伴区域 */
.virtual-partner-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  position: relative;
  z-index: 2;
}

.partner-avatar {
  text-align: center;
  transition: transform 0.3s ease;
}

.avatar-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.partner-avatar.speaking .avatar-image {
  transform: scale(1.05);
  border-color: #d4c5a9;
  box-shadow: 0 25px 70px rgba(212, 197, 169, 0.3);
}

.partner-avatar.listening .avatar-image {
  border-color: #a8edea;
  box-shadow: 0 25px 70px rgba(168, 237, 234, 0.3);
}

.expression-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  transition: background-color 0.5s ease;
  pointer-events: none;
}

.expression-overlay.happy {
  background: radial-gradient(circle, rgba(255, 223, 186, 0.3) 0%, transparent 70%);
}

.expression-overlay.thinking {
  background: radial-gradient(circle, rgba(168, 237, 234, 0.3) 0%, transparent 70%);
}

/* 声波效果 */
.sound-waves {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 250px;
  height: 250px;
}

.wave {
  position: absolute;
  border: 2px solid #d4c5a9;
  border-radius: 50%;
  opacity: 0;
  animation: soundWave 2s infinite;
}

.wave1 {
  width: 100%;
  height: 100%;
  animation-delay: 0s;
}

.wave2 {
  width: 120%;
  height: 120%;
  top: -10%;
  left: -10%;
  animation-delay: 0.5s;
}

.wave3 {
  width: 140%;
  height: 140%;
  top: -20%;
  left: -20%;
  animation-delay: 1s;
}

@keyframes soundWave {
  0% {
    opacity: 1;
    transform: scale(0.8);
  }
  100% {
    opacity: 0;
    transform: scale(1.3);
  }
}

/* 呼吸效果 */
.breathing-glow {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  animation: breathe 4s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.05);
  }
}

.partner-status {
  color: #8b6f47;
  font-size: 1rem;
  font-weight: 400;
  opacity: 0.8;
  min-height: 24px;
  transition: all 0.3s ease;
}

/* 对话文本区域 */
.conversation-text {
  position: fixed;
  top: 20px;
  left: 20px;
  right: 20px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 3;
  transition: all 0.3s ease;
}

.conversation-text.minimized {
  opacity: 0.3;
  transform: translateY(-10px);
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  animation: messageAppear 0.5s ease-out;
}

.message-bubble.user {
  align-self: flex-end;
  background: rgba(212, 197, 169, 0.8);
  color: white;
  margin-left: auto;
}

.message-bubble.ai {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.9);
  color: #8b6f47;
}

.message-content {
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 4px;
}

.message-time {
  font-size: 11px;
  opacity: 0.6;
  text-align: right;
}

.message-bubble.ai .message-time {
  text-align: left;
}

@keyframes messageAppear {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-enter-active, .message-leave-active {
  transition: all 0.5s ease;
}

.message-enter-from, .message-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 交互区域 */
.interaction-area {
  position: fixed;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 4;
}

.mic-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.mic-button {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(212, 197, 169, 0.4);
  position: relative;
  overflow: hidden;
}

.mic-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(212, 197, 169, 0.5);
}

.mic-button.pressed {
  transform: translateY(-1px) scale(0.95);
}

.mic-button.recording {
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  animation: recordingPulse 1.5s infinite;
}

.mic-button.processing {
  background: linear-gradient(135deg, #a8edea, #fed6e3);
}

.mic-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

@keyframes recordingPulse {
  0%, 100% {
    box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
  }
  50% {
    box-shadow: 0 15px 40px rgba(255, 107, 107, 0.7);
  }
}

.mic-icon svg {
  transition: transform 0.3s ease;
}

.mic-button:hover .mic-icon svg {
  transform: scale(1.1);
}

/* 录音动画 */
.recording-animation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
}

.recording-wave {
  width: 3px;
  height: 20px;
  background: white;
  border-radius: 2px;
  animation: recordingWave 1s infinite ease-in-out;
}

.recording-wave1 { animation-delay: 0s; }
.recording-wave2 { animation-delay: 0.1s; }
.recording-wave3 { animation-delay: 0.2s; }
.recording-wave4 { animation-delay: 0.3s; }

@keyframes recordingWave {
  0%, 40%, 100% {
    transform: scaleY(0.4);
  }
  20% {
    transform: scaleY(1);
  }
}

/* 处理中动画 */
.processing-spinner {
  width: 32px;
  height: 32px;
}

.spinner-ring {
  width: 100%;
  height: 100%;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 录音提示 */
.recording-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #8b6f47;
  font-size: 14px;
  font-weight: 500;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff6b6b;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
}

/* 最小化控制按钮 */
.settings-entry, .text-toggle {
  position: fixed;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #8b6f47;
  z-index: 5;
}

.settings-entry {
  top: 20px;
  right: 20px;
}

.text-toggle {
  top: 20px;
  right: 70px;
}

.settings-entry:hover, .text-toggle:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .avatar-container {
    width: 150px;
    height: 150px;
  }
  
  .mic-button {
    width: 70px;
    height: 70px;
  }
  
  .mic-icon svg {
    width: 28px;
    height: 28px;
  }
  
  .conversation-text {
    top: 80px;
    left: 15px;
    right: 15px;
    max-height: 150px;
  }
  
  .cloud {
    font-size: 1.5rem;
  }
  
  .cloud2, .cloud4, .cloud5 {
    font-size: 1.2rem;
  }
  
  .cloud3 {
    font-size: 1.4rem;
  }
}

@media (max-width: 480px) {
  .avatar-container {
    width: 120px;
    height: 120px;
  }
  
  .mic-button {
    width: 60px;
    height: 60px;
  }
  
  .mic-icon svg {
    width: 24px;
    height: 24px;
  }
  
  .message-bubble {
    max-width: 85%;
    padding: 10px 14px;
    font-size: 13px;
  }
  
  .settings-entry, .text-toggle {
    width: 35px;
    height: 35px;
  }
  
  .text-toggle {
    right: 60px;
  }
}
</style>
