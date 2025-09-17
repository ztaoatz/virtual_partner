/**
 * Nahida TTS 语音服务工具类
 * 用于替换浏览器默认的语音合成，使用Nahida的声音
 */

class NahidaTTSService {
  constructor() {
    this.baseURL = 'http://127.0.0.1:8000'
    this.isPlaying = false
    this.currentAudio = null
    this.onStartCallback = null
    this.onEndCallback = null
    this.onErrorCallback = null
  }  /**
   * 检查TTS服务是否可用
   */
  async checkServiceStatus() {
    try {
      console.log('🔍 检查Nahida TTS服务状态...')
      const response = await fetch(`${this.baseURL}/tts-status/`, { 
        method: 'GET',
        timeout: 3000 
      })
      
      if (!response.ok) {
        console.log('❌ TTS状态检查请求失败:', response.status)
        return false
      }
      
      const data = await response.json()
      const isAvailable = data.status === 'available'
      
      if (isAvailable) {
        console.log('✅ Nahida TTS服务可用:', data.message)
      } else {
        console.log('⚠️ Nahida TTS服务不可用:', data.message)
      }
      
      return isAvailable
    } catch (error) {
      console.log('⚠️ TTS服务状态检查失败，将使用浏览器TTS:', error.message)
      return false
    }
  }

  /**
   * 播放Nahida语音
   * @param {string} text - 要转换为语音的文本
   * @param {Object} options - 可选配置
   * @param {Function} options.onStart - 开始播放回调
   * @param {Function} options.onEnd - 播放结束回调
   * @param {Function} options.onError - 错误回调
   */
  async speak(text, options = {}) {
    // 如果当前正在播放，先停止
    if (this.isPlaying) {
      this.stop()
    }

    try {
      console.log('🎤 开始请求Nahida TTS:', text.substring(0, 50) + '...')

      // 设置回调函数
      this.onStartCallback = options.onStart
      this.onEndCallback = options.onEnd
      this.onErrorCallback = options.onError

      // 发送TTS请求
      const response = await fetch(`${this.baseURL}/nahida-tts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text
        })
      })

      if (!response.ok) {
        throw new Error(`TTS服务错误: ${response.status}`)
      }

      // 获取音频数据
      const audioBlob = await response.blob()
      const audioUrl = URL.createObjectURL(audioBlob)

      // 创建音频对象并播放
      this.currentAudio = new Audio(audioUrl)
      
      // 设置音频事件监听器
      this.currentAudio.onloadstart = () => {
        console.log('🎵 Nahida音频开始加载')
      }

      this.currentAudio.oncanplay = () => {
        console.log('🎵 Nahida音频可以播放')
        this.isPlaying = true
        
        // 触发开始回调
        if (this.onStartCallback) {
          this.onStartCallback()
        }
      }

      this.currentAudio.onended = () => {
        console.log('🎵 Nahida音频播放结束')
        this.isPlaying = false
        
        // 清理资源
        URL.revokeObjectURL(audioUrl)
        this.currentAudio = null
        
        // 触发结束回调
        if (this.onEndCallback) {
          this.onEndCallback()
        }
      }

      this.currentAudio.onerror = (error) => {
        console.error('🎵 Nahida音频播放错误:', error)
        this.isPlaying = false
        
        // 清理资源
        URL.revokeObjectURL(audioUrl)
        this.currentAudio = null
        
        // 触发错误回调
        if (this.onErrorCallback) {
          this.onErrorCallback(error)
        }
      }

      // 开始播放
      await this.currentAudio.play()

    } catch (error) {
      console.error('🚫 Nahida TTS请求失败:', error)
      this.isPlaying = false
      
      // 触发错误回调
      if (this.onErrorCallback) {
        this.onErrorCallback(error)
      }
      
      // 如果TTS服务不可用，抛出错误让调用者处理
      throw error
    }
  }

  /**
   * 停止当前播放的语音
   */
  stop() {
    if (this.currentAudio) {
      this.currentAudio.pause()
      this.currentAudio.currentTime = 0
      this.currentAudio = null
    }
    this.isPlaying = false
    
    console.log('⏹️ 停止Nahida语音播放')
  }

  /**
   * 检查是否正在播放
   */
  get speaking() {
    return this.isPlaying
  }
}

// 创建全局实例
const nahidaTTS = new NahidaTTSService()

export default nahidaTTS
