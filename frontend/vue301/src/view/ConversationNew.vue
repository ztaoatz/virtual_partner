<template>
  <div class="conversation-container">
    <!-- 云朵装饰背景 -->
    <div class="cloud-decorations">
      <div class="cloud cloud1">☁</div>
      <div class="cloud cloud2">☁</div>
      <div class="cloud cloud3">☁</div>
      <div class="cloud cloud4">☁</div>
      <div class="cloud cloud5">☁</div>
    </div>    <!-- 虚拟伙伴形象区域 -->
    <div class="virtual-partner-area">
      <div class="partner-avatar" :class="{ 'speaking': isAISpeaking, 'listening': isListening }">
        <div class="live2d-avatar-container">
          <!-- Live2D Nahida 模型 -->
          <Live2DCanvas 
            ref="nahidaRef"
            :width="400"
            :height="500"
            :scale="0.12"
            :modelPath="'/live2d/Nahida_1080/Nahida_1080.model3.json'"
          />
          
          <!-- 说话时的声波效果覆盖层 -->
          <div v-if="isAISpeaking" class="sound-waves-overlay">
            <div class="wave wave1"></div>
            <div class="wave wave2"></div>
            <div class="wave wave3"></div>
          </div>
          
          <!-- 倾听时的呼吸效果覆盖层 -->
          <div v-if="!isAISpeaking && !isListening" class="breathing-glow-overlay"></div>
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
          <span v-if="recognition">正在语音识别...</span>
          <span v-else>正在录制音频...</span>
        </div>
        
        <!-- 处理状态提示 -->
        <div class="processing-hint" v-if="isProcessing">
          <div class="thinking-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span>AI正在思考中...</span>
        </div>
      </div>
    </div>

    <!-- 最小化的设置入口 -->
    <div class="settings-entry" @click="openSettings">
      <svg viewBox="0 0 24 24" width="20" height="20">
        <path d="M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" fill="currentColor"/>
      </svg>
    </div>    <!-- 文本显示切换按钮 -->
    <div class="text-toggle" @click="toggleText">
      <svg viewBox="0 0 24 24" width="18" height="18">
        <path d="M9,22A1,1 0 0,1 8,21V18H4A2,2 0 0,1 2,16V4C2,2.89 2.9,2 4,2H20A2,2 0 0,1 22,4V16A2,2 0 0,1 20,18H13.9L10.2,21.71C10,21.9 9.75,22 9.5,22H9M4,4V16H8.5L12,19.5V16H20V4H4Z" fill="currentColor"/>
      </svg>
    </div>

    <!-- 情绪日记按钮 -->
    <div class="diary-toggle" @click="openDiary" title="情绪日记">
      <svg viewBox="0 0 24 24" width="18" height="18">
        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" fill="currentColor"/>
      </svg>
    </div>

    <!-- 情绪日记模态框 -->
    <div v-if="showDiary" class="diary-modal">
      <div class="diary-content">
        <div class="diary-header">
          <h3>情绪日记</h3>
          <button @click="closeDiary" class="close-btn">&times;</button>
        </div>
        
        <div class="diary-body">
          <!-- 日期选择器 -->
          <div class="date-selector">
            <input 
              type="date" 
              v-model="selectedDate" 
              @change="loadDiaryForDate"
              class="date-input"
            />
          </div>
          
          <!-- 日记内容显示 -->
          <div class="diary-display" v-if="diaryData.content">
            <div class="emotion-summary">
              <h4>今日情绪总结</h4>
              <div class="emotion-tags">
                <span v-for="emotion in diaryData.emotions" :key="emotion" class="emotion-tag">
                  {{ emotion }}
                </span>
              </div>
            </div>
            
            <div class="diary-text">
              <h4>对话日记</h4>
              <p>{{ diaryData.content }}</p>
            </div>
              <div class="conversation-stats">
              <h4>对话统计</h4>
              <div class="stats-grid">
                <div class="stat-item">
                  <span class="stat-label">对话轮数</span>
                  <span class="stat-value">{{ diaryData.messageCount }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">主要话题</span>
                  <span class="stat-value">{{ diaryData.mainTopic }}</span>
                </div>
              </div>
            </div>
            
            <!-- 重新生成按钮 -->
            <div class="diary-actions">
              <button @click="regenerateDiary" class="regenerate-btn" :disabled="isProcessing">
                <svg viewBox="0 0 24 24" width="16" height="16" class="regenerate-icon">
                  <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" fill="currentColor"/>
                </svg>
                重新生成
              </button>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-else class="empty-diary">
            <div class="empty-icon">📝</div>
            <p>该日期暂无情绪日记</p>
            <button @click="generateDiary" class="generate-btn" :disabled="messages.length === 0">
              生成今日日记
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import Live2DCanvas from '@/components/Live2DCanvas.vue'

// Live2D 相关引用
const nahidaRef = ref(null)

// 响应式数据
const isRecording = ref(false)
const isProcessing = ref(false)
const isListening = ref(false)
const isAISpeaking = ref(false)
const isPressed = ref(false)
const showText = ref(true)
const currentEmotion = ref('neutral')
const partnerStatus = ref('准备就绪，随时为您服务')

// 用户和会话管理
const currentUserId = ref('')
const currentSessionId = ref('')
const isLoadingHistory = ref(false)

// 情绪日记相关
const showDiary = ref(false)
const selectedDate = ref(new Date().toISOString().split('T')[0])
const diaryData = reactive({
  content: '',
  emotions: [],
  messageCount: 0,
  mainTopic: ''
})
const diaryDates = reactive(new Set())

// 消息数据
const messages = reactive([])
const recentMessages = computed(() => {
  return messages.slice(-8) // 显示最近8条消息
})

// 录音相关
let mediaRecorder = null
let audioStream = null
let recordingTimeout = null
let recognition = null

// 初始化语音识别
const initSpeechRecognition = () => {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition = new SpeechRecognition()
    
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'zh-CN'
    recognition.maxAlternatives = 1
    
    recognition.onstart = () => {
      console.log('语音识别已启动')
    }
    
    recognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalTranscript += transcript
        } else {
          interimTranscript += transcript
        }
      }
      
      if (finalTranscript) {
        handleSpeechResult(finalTranscript)
      }
    }
    
    recognition.onerror = (event) => {
      console.error('语音识别错误:', event.error)
      if (event.error === 'no-speech') {
        partnerStatus.value = '没有检测到语音，请重试'
      } else if (event.error === 'network') {
        partnerStatus.value = '网络连接问题，请检查网络'
      } else {
        partnerStatus.value = '语音识别失败，请重试'
      }
      resetRecordingState()
    }
    
    recognition.onend = () => {
      console.log('语音识别已结束')
      if (isRecording.value) {
        stopRecording()
      }
    }
  } else {
    console.warn('浏览器不支持语音识别API，将使用MediaRecorder录音')
  }
}

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
    
    // 触发Live2D模型倾听动作
    if (nahidaRef.value) {
      nahidaRef.value.playMotion('TapHead')
      nahidaRef.value.setExpression('Shy')
    }
    
    // 优先使用语音识别API
    if (recognition) {
      recognition.start()
      
      // 设置超时
      recordingTimeout = setTimeout(() => {
        if (isRecording.value) {
          stopRecording()
        }
      }, 30000)
      
    } else {
      // 备选方案：使用MediaRecorder
      audioStream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(audioStream)
      
      const audioChunks = []
      
      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
        await processAudioBlob(audioBlob)
      }
      
      mediaRecorder.start()
      
      recordingTimeout = setTimeout(() => {
        if (isRecording.value) {
          stopRecording()
        }
      }, 30000)
    }
    
  } catch (error) {
    console.error('录音启动失败:', error)
    alert('录音功能启动失败，请检查麦克风权限')
    resetRecordingState()
  }
}

const stopRecording = () => {
  if (recognition && isRecording.value) {
    recognition.stop()
  }
  
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
  
  // 恢复Live2D模型为默认状态
  if (nahidaRef.value) {
    nahidaRef.value.setExpression('black') // 默认表情
    nahidaRef.value.playMotion('Idle') // 待机动作
  }
  
  // 如果没有使用语音识别API，则进入处理状态
  if (!recognition) {
    isProcessing.value = true
    partnerStatus.value = '正在处理音频...'
  }
}

// 处理语音识别结果
const handleSpeechResult = async (transcript) => {
  console.log('语音识别结果:', transcript)
  
  // 添加用户消息
  const userMessage = {
    id: Date.now(),
    text: transcript,
    isUser: true,
    timestamp: new Date()
  }
  messages.push(userMessage)
  
  // 停止录音并开始处理
  stopRecording()
  isProcessing.value = true
  partnerStatus.value = '正在思考您的问题...'
  
  // 发送到AI模型
  await sendToAIModel(transcript)
}

// 发送到后端API（使用增强的聊天API）
const sendToAIModel = async (userInput) => {
  try {
    // 使用新的增强聊天API
    const response = await axios.post('http://127.0.0.1:8000/enhanced-chat/', {
      "prompt": userInput,
      "system": '你现在是由SocialAI开发的温暖智能助手灵犀，专门为用户提供贴心的对话交流服务。你的任务是以温暖、体贴的方式与用户进行自然对话，帮助用户解决问题，分享情感，提供有价值的建议和陪伴。',
      "user_id": currentUserId.value,
      "session_id": currentSessionId.value
    })
      if (response.data && response.data.result) {
      // 更新会话信息
      currentUserId.value = response.data.user_id
      currentSessionId.value = response.data.session_id
      
      // 保存会话ID到localStorage
      localStorage.setItem('virtual_partner_session_id', response.data.session_id)
      
      // AI回复成功
      isAISpeaking.value = true
      currentEmotion.value = 'happy'
      partnerStatus.value = '正在回复中...'
      
      // 触发Live2D模型说话动作
      if (nahidaRef.value) {
        nahidaRef.value.playMotion('TapBody')
        nahidaRef.value.setExpression('Happy1')
      }
      
      const aiMessage = {
        id: response.data.message_id || Date.now() + 1,
        text: response.data.result,
        isUser: false,
        timestamp: new Date(response.data.timestamp || new Date())
      }
      messages.push(aiMessage)
      
      // 使用语音合成播放AI回复
      speakText(response.data.result)
      
      // 根据回复长度调整AI说话时间
      setTimeout(() => {
        isAISpeaking.value = false
        currentEmotion.value = 'neutral'
        partnerStatus.value = '我在这里，请继续交流'
        isProcessing.value = false
        
        // 恢复Live2D模型为默认状态
        if (nahidaRef.value) {
          nahidaRef.value.setExpression('black') // 默认表情
          nahidaRef.value.playMotion('Idle') // 待机动作
        }
      }, Math.max(3000, response.data.result.length * 100))
      
    } else {
      throw new Error('后端API返回格式错误')
    }
    
  } catch (error) {
    console.error('后端API调用失败:', error)
    
    // 显示错误并提供备用回复
    const errorMessage = {
      id: Date.now() + 1,
      text: '抱歉，我暂时无法连接到AI服务。请稍后重试，或者检查网络连接。',
      isUser: false,
      timestamp: new Date()
    }
    messages.push(errorMessage)
    
    partnerStatus.value = '连接失败，请重试'
    isProcessing.value = false
    isAISpeaking.value = false
    currentEmotion.value = 'neutral'
  }
}

// 语音合成播放AI回复
const speakText = (text) => {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'zh-CN'
    utterance.rate = 0.9
    utterance.pitch = 1.1
    utterance.volume = 0.8
    
    utterance.onstart = () => {
      console.log('开始语音播放')
      // 开始嘴部动画
      if (nahidaRef.value) {
        nahidaRef.value.startTalking()
      }
    }
    
    utterance.onend = () => {
      console.log('语音播放结束')
      // 停止嘴部动画
      if (nahidaRef.value) {
        nahidaRef.value.stopTalking()
      }
    }
    
    utterance.onerror = (event) => {
      console.error('语音合成错误:', event.error)
      // 出错时也要停止嘴部动画
      if (nahidaRef.value) {
        nahidaRef.value.stopTalking()
      }
    }
    
    speechSynthesis.speak(utterance)
  }
}

// 备用方案：处理音频文件（当不支持语音识别API时）
const processAudioBlob = async (audioBlob) => {
  try {
    // 这里可以集成其他语音转文字服务，如百度、阿里云等
    // 目前提供一个模拟实现
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    const simulatedTranscript = '这是通过音频文件模拟识别的文字内容'
    await handleSpeechResult(simulatedTranscript)
    
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

// 情绪日记相关方法
const openDiary = () => {
  showDiary.value = true
  loadDiaryForDate()
}

const closeDiary = () => {
  showDiary.value = false
}

const loadDiaryForDate = async () => {
  try {
    // 如果有用户ID，先尝试从后端加载日记
    if (currentUserId.value) {
      try {
        const response = await axios.get('http://127.0.0.1:8000/get-diary/', {
          params: {
            user_id: currentUserId.value,
            date: selectedDate.value
          }
        })
        
        if (response.data && response.data.success) {
          const diary = response.data.diary
          Object.assign(diaryData, {
            content: diary.content,
            emotions: diary.emotions,
            messageCount: diary.message_count,
            mainTopic: diary.main_topic,
            date: diary.date
          })
          
          // 保存到本地存储作为缓存
          localStorage.setItem(`diary_${selectedDate.value}`, JSON.stringify(diaryData))
          diaryDates.add(selectedDate.value)
          return
        }
      } catch (error) {
        console.log('后端没有该日期的日记记录')
      }
    }
    
    // 如果后端没有，尝试从本地存储加载
    const storedDiary = localStorage.getItem(`diary_${selectedDate.value}`)
    if (storedDiary) {
      const parsed = JSON.parse(storedDiary)
      Object.assign(diaryData, parsed)
      return
    }
    
    // 如果都没有，检查该日期是否有聊天记录
    if (currentUserId.value) {
      try {
        const historyResponse = await axios.get('http://127.0.0.1:8000/chat-history/', {
          params: { user_id: currentUserId.value }
        })
        
        if (historyResponse.data?.success && historyResponse.data.messages) {
          const targetDate = selectedDate.value
          const messagesFromDate = historyResponse.data.messages.filter(msg => {
            const msgDate = new Date(msg.timestamp).toISOString().split('T')[0]
            return msgDate === targetDate
          })
          
          if (messagesFromDate.length >= 2) {
            // 有足够的消息记录，提示可以生成日记
            diaryData.content = '该日期有聊天记录，点击"生成今日日记"按钮来创建AI情绪日记'
            diaryData.emotions = []
            diaryData.messageCount = Math.floor(messagesFromDate.length / 2)
            diaryData.mainTopic = '待分析'
            return
          }
        }
      } catch (error) {
        console.log('检查聊天记录失败:', error)
      }
    }
      // 清空数据
    diaryData.content = ''
    diaryData.emotions = []
    diaryData.messageCount = 0
    diaryData.mainTopic = ''
    
  } catch (error) {
    console.error('加载日记失败:', error)
    // 清空数据
    diaryData.content = ''
    diaryData.emotions = []
    diaryData.messageCount = 0
    diaryData.mainTopic = ''
  }
}

const generateDiary = async () => {
  if (!currentUserId.value) {
    alert('请先登录后再生成日记')
    return
  }

  try {
    // 检查是否已有日记
    let forceRegenerate = false
    if (diaryData.content && diaryData.content.length > 50) {
      // 询问是否重新生成
      const userConfirm = confirm('该日期已有情绪日记，是否重新生成？\n重新生成将覆盖现有日记内容。')
      if (!userConfirm) {
        return
      }
      forceRegenerate = true
    }
    
    // 显示加载状态
    const loadingMessage = forceRegenerate ? 
      '正在重新生成情绪日记...' : 
      '正在使用AI分析您的聊天记录，生成情绪日记...'
    partnerStatus.value = loadingMessage
    
    // 调用后端API生成日记
    const response = await axios.post('http://127.0.0.1:8000/generate-diary/', {
      user_id: currentUserId.value,
      date: selectedDate.value,  // 格式: YYYY-MM-DD
      force_regenerate: forceRegenerate
    })

    if (response.data && response.data.success) {
      const diary = response.data.diary
      
      // 更新日记数据
      Object.assign(diaryData, {
        content: diary.content,
        emotions: diary.emotions.map(e => typeof e === 'string' ? e : e.emotion), // 兼容不同格式
        messageCount: diary.message_count,
        mainTopic: diary.main_topic,
        date: diary.date
      })
      
      // 保存到本地存储（可选）
      localStorage.setItem(`diary_${selectedDate.value}`, JSON.stringify(diaryData))
      
      // 添加到日记日期列表
      diaryDates.add(selectedDate.value)

      const successMessage = diary.is_regenerated ? 
        'AI情绪日记重新生成成功！' : 
        'AI情绪日记生成成功！'
      alert(successMessage)
      partnerStatus.value = '日记生成完成！您可以查看今日的情绪分析'
      
    } else {
      throw new Error(response.data?.error || '生成失败')
    }
    
  } catch (error) {
    console.error('生成日记失败:', error)
    
    let errorMessage = '生成日记失败，请重试'
    if (error.response?.status === 400) {
      errorMessage = error.response.data?.error || '该日期没有聊天记录，无法生成日记'
    } else if (error.response?.status === 500) {
      const details = error.response.data?.details
      if (details && details.includes('连接失败')) {
        errorMessage = 'AI模型服务未启动，请确认Ollama服务正在运行'
      } else {
        errorMessage = 'AI模型服务异常，请稍后重试'
      }
    } else if (error.message.includes('Network Error')) {
      errorMessage = '网络连接失败，请检查网络连接'
    }
      alert(errorMessage)
    partnerStatus.value = '日记生成失败，请重试'
  }
}

// 重新生成日记方法
const regenerateDiary = async () => {
  if (!currentUserId.value) {
    alert('请先登录后再重新生成日记')
    return
  }

  // 确认重新生成
  const userConfirm = confirm('确定要重新生成情绪日记吗？\n重新生成将使用最新的聊天记录覆盖现有日记内容。')
  if (!userConfirm) {
    return
  }

  try {
    // 显示加载状态
    partnerStatus.value = '正在重新生成情绪日记...'
    isProcessing.value = true
    
    // 调用后端API强制重新生成日记
    const response = await axios.post('http://127.0.0.1:8000/generate-diary/', {
      user_id: currentUserId.value,
      date: selectedDate.value,
      force_regenerate: true
    })

    if (response.data && response.data.success) {
      const diary = response.data.diary
      
      // 更新日记数据
      Object.assign(diaryData, {
        content: diary.content,
        emotions: diary.emotions.map(e => typeof e === 'string' ? e : e.emotion),
        messageCount: diary.message_count,
        mainTopic: diary.main_topic,
        date: diary.date
      })
      
      // 保存到本地存储
      localStorage.setItem(`diary_${selectedDate.value}`, JSON.stringify(diaryData))
      
      alert('AI情绪日记重新生成成功！')
      partnerStatus.value = '日记重新生成完成！您可以查看更新后的情绪分析'
      
    } else {
      throw new Error(response.data?.error || '重新生成失败')
    }
    
  } catch (error) {
    console.error('重新生成日记失败:', error)
    
    let errorMessage = '重新生成日记失败，请重试'
    if (error.response?.status === 400) {
      errorMessage = error.response.data?.error || '该日期没有聊天记录，无法重新生成日记'
    } else if (error.response?.status === 500) {
      const details = error.response.data?.details
      if (details && details.includes('连接失败')) {
        errorMessage = 'AI模型服务未启动，请确认Ollama服务正在运行'
      } else {
        errorMessage = 'AI模型服务异常，请稍后重试'
      }
    } else if (error.message.includes('Network Error')) {
      errorMessage = '网络连接失败，请检查网络连接'
    }
    
    alert(errorMessage)
    partnerStatus.value = '日记重新生成失败，请重试'
  } finally {
    isProcessing.value = false
  }
}

const extractEmotions = (text) => {
  const emotionMap = {
    '开心': ['开心', '高兴', '快乐', '兴奋', '愉快', '喜悦'],
    '难过': ['难过', '伤心', '悲伤', '沮丧', '失落', '郁闷'],
    '焦虑': ['焦虑', '紧张', '担心', '不安', '忧虑', '压力'],
    '愤怒': ['愤怒', '生气', '烦躁', '恼火', '气愤'],
    '平静': ['平静', '安静', '轻松', '舒适', '宁静'],
    '疲惫': ['累', '疲惫', '疲劳', '困', '乏力']
  }

  const detectedEmotions = []
  for (const [emotion, keywords] of Object.entries(emotionMap)) {
    if (keywords.some(keyword => text.includes(keyword))) {
      detectedEmotions.push(emotion)
    }
  }

  return detectedEmotions.length > 0 ? detectedEmotions : ['平静']
}

const extractMainTopic = (text) => {
  const topics = [
    { name: '工作学习', keywords: ['工作', '学习', '项目', '任务', '考试', '作业', '职场', '同事'] },
    { name: '人际关系', keywords: ['朋友', '家人', '同事', '关系', '交流', '沟通', '聊天'] },
    { name: '健康生活', keywords: ['健康', '运动', '饮食', '睡眠', '休息', '锻炼', '身体'] },
    { name: '情感表达', keywords: ['感受', '情绪', '心情', '想法', '感觉', '体验'] },
    { name: '兴趣爱好', keywords: ['游戏', '电影', '音乐', '阅读', '旅行', '美食', '艺术'] },
    { name: '日常生活', keywords: ['日常', '生活', '今天', '昨天', '计划', '安排'] }
  ]

  let maxScore = 0
  let mainTopic = '日常交流'

  for (const topic of topics) {
    const score = topic.keywords.reduce((acc, keyword) => {
      return acc + (text.split(keyword).length - 1)
    }, 0)
    
    if (score > maxScore) {
      maxScore = score
      mainTopic = topic.name
    }
  }

  return mainTopic
}

const generateDiaryContent = async (messages) => {
  // 简化版本：基于对话内容生成总结
  const userMessages = messages.filter(msg => msg.isUser)
  const aiMessages = messages.filter(msg => !msg.isUser)
  
  if (userMessages.length === 0) {
    return '今天没有进行对话。'
  }

  const topics = userMessages.map(msg => msg.text).join('，')
  const emotions = extractEmotions(topics)
  
  let summary = `今天与AI助手进行了${Math.floor(messages.length / 2)}轮对话。`
  
  if (emotions.length > 0) {
    summary += `主要的情绪状态是${emotions.join('、')}。`
  }
  
  summary += `主要讨论了关于${extractMainTopic(topics)}的话题。`
  
  if (userMessages.length > 3) {
    summary += '对话内容丰富，涵盖了多个方面的交流。'
  } else if (userMessages.length > 1) {
    summary += '进行了有意义的交流互动。'
  } else {
    summary += '虽然对话简短，但也是一次有价值的交流。'
  }

  return summary
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 聊天历史管理方法
const loadChatHistory = async () => {
  try {
    isLoadingHistory.value = true
    partnerStatus.value = '正在加载聊天历史...'
    
    // 构建请求参数，仅传递用户ID，让后端决定加载哪个会话
    const params = {
      user_id: currentUserId.value
    }
    
    // 如果有存储的会话ID，也传递给后端（可选）
    if (currentSessionId.value) {
      params.session_id = currentSessionId.value
    }
    
    const response = await axios.get('http://127.0.0.1:8000/chat-history/', {
      params: params
    })
    
    if (response.data && response.data.success) {
      // 更新用户和会话信息
      currentUserId.value = response.data.user_id
      currentSessionId.value = response.data.session_id
      
      // 保存会话ID到localStorage
      localStorage.setItem('virtual_partner_session_id', response.data.session_id)
      
      // 清空当前消息并加载历史记录
      messages.splice(0, messages.length)
      
      // 如果有历史记录，加载它们
      if (response.data.messages && response.data.messages.length > 0) {
        response.data.messages.forEach(msg => {
          messages.push({
            id: msg.id,
            text: msg.text,
            isUser: msg.isUser,
            timestamp: new Date(msg.timestamp)
          })
        })
        
        // 检查是否是已登录用户
        const userInfo = JSON.parse(sessionStorage.getItem('userInfo') || '{}')
        if (userInfo.user_id && userInfo.user_id === currentUserId.value) {
          partnerStatus.value = `欢迎回来，${userInfo.username || '用户'}！我们继续之前的对话吧`
        } else {
          partnerStatus.value = '欢迎回来！我们继续之前的对话吧'
        }
        
        console.log(`成功加载 ${response.data.messages.length} 条历史消息`)
      } else {
        // 如果没有历史记录，显示欢迎消息
        addWelcomeMessages()
      }
    } else {
      console.log('后端返回无历史记录，显示欢迎消息')
      addWelcomeMessages()
    }
    
  } catch (error) {
    console.error('加载聊天历史失败:', error)
    // 网络错误或其他错误时，仍显示欢迎消息
    addWelcomeMessages()
  } finally {
    isLoadingHistory.value = false
  }
}

const addWelcomeMessages = () => {
  // 检查是否是已登录用户
  const userInfo = JSON.parse(sessionStorage.getItem('userInfo') || '{}')
  let welcomeText = ''
  
  if (userInfo.user_id && userInfo.user_id === currentUserId.value) {
    // 已登录用户的欢迎消息
    welcomeText = `你好${userInfo.username ? '，' + userInfo.username : ''}！我是灵犀，您的AI伙伴。看起来这是我们的第一次对话，点击下方的麦克风按钮开始我们的语音交流吧！`
    partnerStatus.value = `欢迎，${userInfo.username || '用户'}！准备开始我们的对话`
  } else {
    // 访客用户的欢迎消息
    welcomeText = '你好！我是灵犀，您的AI伙伴。点击下方的麦克风按钮开始我们的语音对话吧！'
    partnerStatus.value = '准备就绪，随时为您服务'
  }
  
  // 添加欢迎消息
  messages.push({
    id: 1,
    text: welcomeText,
    isUser: false,
    timestamp: new Date()
  })
  
  // 检查浏览器语音功能支持
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    messages.push({
      id: 2,
      text: '您的浏览器不支持语音识别功能，建议使用Chrome浏览器以获得最佳体验。',
      isUser: false,
      timestamp: new Date()
    })
  }
}

const initializeUserSession = () => {
  // 首先检查是否有已登录用户的信息
  const userInfo = JSON.parse(sessionStorage.getItem('userInfo') || '{}')
  let storedUserId = null
  
  // 优先使用已登录用户的ID
  if (userInfo.user_id) {
    storedUserId = userInfo.user_id
    console.log('使用已登录用户ID:', storedUserId)
    
    // 检查localStorage中的用户ID是否与当前登录用户匹配
    const localStorageUserId = localStorage.getItem('virtual_partner_user_id')
    if (localStorageUserId !== storedUserId) {
      // 如果不匹配，说明用户已切换，清除旧的会话数据
      console.log('检测到用户切换，清除旧会话数据')
      localStorage.setItem('virtual_partner_user_id', storedUserId)
      localStorage.removeItem('virtual_partner_session_id')
    }
  } else {
    // 如果没有登录用户，从localStorage获取或生成临时用户ID
    storedUserId = localStorage.getItem('virtual_partner_user_id')
    console.log('使用临时用户ID:', storedUserId)
  }
  
  // 检查现有用户ID是否是有效的UUID格式
  const isValidUUID = (str) => {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
    return uuidRegex.test(str)
  }
  
  if (!storedUserId || !isValidUUID(storedUserId)) {
    // 生成标准UUID格式的用户ID
    storedUserId = generateUUID()
    localStorage.setItem('virtual_partner_user_id', storedUserId)
    // 清除旧的会话ID，重新开始
    localStorage.removeItem('virtual_partner_session_id')
    console.log('生成新的临时用户ID:', storedUserId)
  }
  
  currentUserId.value = storedUserId
  
  // 获取会话ID，如果用户已切换则为null
  currentSessionId.value = localStorage.getItem('virtual_partner_session_id') || null
  
  console.log('初始化用户会话:', {
    userId: currentUserId.value,
    sessionId: currentSessionId.value
  })
}

// 生成UUID的辅助函数
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c == 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

// 生命周期
onMounted(async () => {
  // 初始化用户会话
  initializeUserSession()
  
  // 初始化语音识别
  initSpeechRecognition()
  
  // 加载聊天历史记录
  await loadChatHistory()
})

onUnmounted(() => {
  // 清理语音识别
  if (recognition) {
    recognition.stop()
    recognition = null
  }
  
  // 清理音频流
  if (audioStream) {
    audioStream.getTracks().forEach(track => track.stop())
  }
  
  // 清理定时器
  if (recordingTimeout) {
    clearTimeout(recordingTimeout)
  }
  
  // 停止语音合成
  if ('speechSynthesis' in window) {
    speechSynthesis.cancel()
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

.live2d-avatar-container {
  position: relative;
  width: 400px;
  height: 500px;
  margin: 0 auto 20px;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 3px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.partner-avatar.speaking .live2d-avatar-container {
  transform: scale(1.02);
  border-color: #d4c5a9;
  box-shadow: 0 25px 70px rgba(212, 197, 169, 0.3);
}

.partner-avatar.listening .live2d-avatar-container {
  border-color: #a8edea;
  box-shadow: 0 25px 70px rgba(168, 237, 234, 0.3);
}

/* 保留原有的avatar-container样式以防需要回退 */
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

/* Live2D 覆盖层效果 */
.sound-waves-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  pointer-events: none;
  z-index: 10;
}

.sound-waves-overlay .wave {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 3px solid #4CAF50;
  border-radius: 50%;
  opacity: 0;
  animation: ripple 2s infinite;
}

.sound-waves-overlay .wave1 { animation-delay: 0s; }
.sound-waves-overlay .wave2 { animation-delay: 0.5s; }
.sound-waves-overlay .wave3 { animation-delay: 1s; }

@keyframes ripple {
  0% {
    width: 20px;
    height: 20px;
    opacity: 1;
  }
  100% {
    width: 150px;
    height: 150px;
    opacity: 0;
  }
}

.breathing-glow-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 20px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: breatheOverlay 4s ease-in-out infinite;
  pointer-events: none;
  z-index: 10;
}

@keyframes breatheOverlay {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.02);
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
  max-height: 45vh; /* 增加到屏幕高度的45% */
  overflow-y: auto;
  z-index: 3;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 滚动条样式优化 */
.conversation-text::-webkit-scrollbar {
  width: 6px;
}

.conversation-text::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.conversation-text::-webkit-scrollbar-thumb {
  background: rgba(212, 197, 169, 0.6);
  border-radius: 10px;
  transition: background 0.3s ease;
}

.conversation-text::-webkit-scrollbar-thumb:hover {
  background: rgba(212, 197, 169, 0.8);
}

.conversation-text.minimized {
  opacity: 0.6;
  transform: translateY(-5px);
  max-height: 25vh; /* 最小化时仍保持较大的区域 */
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 12px; /* 增加消息间距 */
  padding: 5px 0;
}

.message-bubble {
  max-width: 80%; /* 增加消息气泡最大宽度 */
  padding: 14px 18px; /* 增加内边距 */
  border-radius: 18px;
  position: relative;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  animation: messageAppear 0.5s ease-out;
  font-size: 15px; /* 稍微增大字体 */
  line-height: 1.5;
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
  font-size: 15px; /* 增大消息内容字体 */
  line-height: 1.5;
  margin-bottom: 6px; /* 增加间距 */
  word-wrap: break-word;
  word-break: break-word;
}

.message-time {
  font-size: 12px; /* 稍微增大时间字体 */
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
.recording-hint, .processing-hint {
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

.thinking-dots {
  display: flex;
  gap: 3px;
}

.thinking-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #d4c5a9;
  animation: thinkingBounce 1.4s infinite ease-in-out both;
}

.thinking-dots span:nth-child(1) { animation-delay: -0.32s; }
.thinking-dots span:nth-child(2) { animation-delay: -0.16s; }
.thinking-dots span:nth-child(3) { animation-delay: 0s; }

@keyframes thinkingBounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
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
    max-height: 40vh; /* 移动端也增加聊天区域 */
    padding: 12px;
  }
  
  .conversation-text.minimized {
    max-height: 20vh;
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
    max-width: 90%; /* 小屏幕上进一步增加宽度 */
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .conversation-text {
    max-height: 35vh; /* 小屏幕适配 */
    padding: 10px;
  }
  
  .conversation-text.minimized {
    max-height: 18vh;
  }
  
  .settings-entry, .text-toggle {
    width: 35px;
    height: 35px;
  }
    .text-toggle {
    right: 60px;
  }
}

/* 情绪日记样式 */
.diary-toggle {
  position: fixed;
  bottom: 130px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(212, 197, 169, 0.3);
  color: white;
  z-index: 100;
}

.diary-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 197, 169, 0.4);
}

.diary-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.diary-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.diary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid rgba(212, 197, 169, 0.2);
  background: linear-gradient(135deg, rgba(212, 197, 169, 0.1), rgba(184, 160, 130, 0.1));
}

.diary-header h3 {
  margin: 0;
  color: #8b7355;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #8b7355;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(212, 197, 169, 0.2);
}

.diary-body {
  padding: 25px;
  max-height: calc(80vh - 80px);
  overflow-y: auto;
}

.date-selector {
  margin-bottom: 20px;
}

.date-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid rgba(212, 197, 169, 0.3);
  border-radius: 10px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.8);
  color: #8b7355;
  transition: all 0.3s ease;
}

.date-input:focus {
  outline: none;
  border-color: #d4c5a9;
  box-shadow: 0 0 10px rgba(212, 197, 169, 0.2);
}

.diary-display {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.emotion-summary h4,
.diary-text h4,
.conversation-stats h4 {
  margin: 0 0 12px 0;
  color: #8b7355;
  font-size: 16px;
  font-weight: 600;
}

.emotion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.emotion-tag {
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
  color: white;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 500;
}

.diary-text p {
  margin: 0;
  line-height: 1.6;
  color: #666;
  background: rgba(255, 255, 255, 0.6);
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #d4c5a9;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.stat-item {
  background: rgba(255, 255, 255, 0.6);
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  border: 1px solid rgba(212, 197, 169, 0.2);
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #8b7355;
}

.empty-diary {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.empty-diary p {
  margin: 0 0 20px 0;
  font-size: 14px;
}

.generate-btn {
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(212, 197, 169, 0.3);
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 197, 169, 0.4);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 重新生成按钮样式 */
.diary-actions {
  margin-top: 25px;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(212, 197, 169, 0.2);
}

.regenerate-btn {
  background: linear-gradient(135deg, #e8a87c, #d4956d);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(232, 168, 124, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  letter-spacing: 0.5px;
}

.regenerate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(232, 168, 124, 0.4);
  background: linear-gradient(135deg, #d4956d, #c4885c);
}

.regenerate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.regenerate-icon {
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.regenerate-btn:hover:not(:disabled) .regenerate-icon {
  transform: rotate(360deg);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .diary-toggle {
    bottom: 120px;
    right: 15px;
    width: 35px;
    height: 35px;
  }
  
  .diary-content {
    width: 95%;
    max-height: 85vh;
  }
  
  .diary-header {
    padding: 15px 20px;
  }
  
  .diary-body {
    padding: 20px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}
</style>
