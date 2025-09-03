// 语音转文字功能测试脚本
// 可以在浏览器控制台中运行此脚本来测试语音识别

class SpeechRecognitionTest {
    constructor() {
        this.recognition = null;
        this.isRecording = false;
        this.init();
    }
    
    init() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'zh-CN';
            this.recognition.maxAlternatives = 1;
            
            this.setupEventListeners();
            console.log('✅ 语音识别初始化成功');
        } else {
            console.error('❌ 浏览器不支持语音识别功能');
        }
    }
    
    setupEventListeners() {
        this.recognition.onstart = () => {
            console.log('🎤 语音识别已启动');
            this.isRecording = true;
        };
        
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            if (interimTranscript) {
                console.log('🔄 识别中:', interimTranscript);
            }
            
            if (finalTranscript) {
                console.log('✅ 最终结果:', finalTranscript);
                this.handleResult(finalTranscript);
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('❌ 语音识别错误:', event.error);
            this.isRecording = false;
        };
        
        this.recognition.onend = () => {
            console.log('⏹️ 语音识别已结束');
            this.isRecording = false;
        };
    }
    
    start() {
        if (this.recognition && !this.isRecording) {
            this.recognition.start();
        }
    }
    
    stop() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
        }
    }
    
    handleResult(transcript) {
        console.log('🚀 准备发送到AI模型:', transcript);
        // 这里可以调用AI模型API
        this.sendToAI(transcript);
    }
    
    async sendToAI(message) {
        try {
            console.log('📤 发送给AI:', message);
            
            // 模拟API调用
            const response = await fetch('http://localhost:25674/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: 'test_user'
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('📥 AI回复:', data);
                
                // 可选：使用语音合成播放回复
                if (data.response) {
                    this.speak(data.response);
                }
            } else {
                console.error('❌ AI API调用失败:', response.status);
            }
        } catch (error) {
            console.error('❌ 网络错误:', error);
            console.log('💡 提示：请确保AI模型服务运行在 http://localhost:25674');
        }
    }
    
    speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'zh-CN';
            utterance.rate = 0.9;
            utterance.pitch = 1.1;
            utterance.volume = 0.8;
            
            utterance.onstart = () => console.log('🔊 开始播放语音');
            utterance.onend = () => console.log('🔇 语音播放结束');
            
            speechSynthesis.speak(utterance);
        }
    }
}

// 使用说明
console.log(`
🎤 语音转文字功能测试
====================

使用方法：
1. const speechTest = new SpeechRecognitionTest();
2. speechTest.start(); // 开始录音
3. 说话...
4. speechTest.stop(); // 停止录音

或者一键测试：
startSpeechTest();

注意事项：
- 需要Chrome等支持Web Speech API的浏览器
- 首次使用需要授权麦克风权限
- 确保AI模型服务运行在 http://localhost:25674
`);

// 一键测试函数
function startSpeechTest() {
    const test = new SpeechRecognitionTest();
    
    if (test.recognition) {
        console.log('🚀 开始语音测试...');
        test.start();
        
        // 10秒后自动停止
        setTimeout(() => {
            test.stop();
            console.log('⏱️ 测试结束（10秒超时）');
        }, 10000);
    }
}

// 检查浏览器兼容性
function checkBrowserCompatibility() {
    console.log('🔍 浏览器兼容性检查:');
    console.log('语音识别:', 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window ? '✅ 支持' : '❌ 不支持');
    console.log('语音合成:', 'speechSynthesis' in window ? '✅ 支持' : '❌ 不支持');
    console.log('媒体录制:', 'mediaDevices' in navigator ? '✅ 支持' : '❌ 不支持');
}

// 立即执行兼容性检查
checkBrowserCompatibility();
