import * as PIXI from 'pixi.js'
import { Live2DModel, MotionPreloadStrategy } from 'pixi-live2d-display';

// 挂载PIXI到全局
window.PIXI = PIXI;

// 可用的模型列表
export const availableModels = {
  miku: {
    name: 'Miku',
    path: '/live2d/miku/runtime/miku.model3.json',
    scale: 0.25,
    motions: ['Idle', 'TapBody', 'TapHead'],
    expressions: []
  },
  nahida: {
    name: 'Nahida (纳西妲)',
    path: '/live2d/Nahida_1080/Nahida_1080.model3.json',
    scale: 0.15,
    motions: ['Idle', 'TapBody', 'TapHead'],
    expressions: ['Happy1', 'Sad1', 'Angry', 'Shy', 'StarEye', 'Wink']
  },
  mahiro: {
    name: 'Mahiro (真寻)',
    path: '/live2d/Mahiro_GG/Mahiro_V1.model3.json',
    scale: 0.2,
    motions: ['Idle', 'TapBody', 'TapHead'],
    expressions: []
  }
};

export async function initLive2DWithModel(modelKey = 'nahida', canvasId = 'canvas_view') {
  try {
    console.log(`开始初始化Live2D模型: ${modelKey}`);
    
    const modelConfig = availableModels[modelKey];
    if (!modelConfig) {
      throw new Error(`未找到模型配置: ${modelKey}`);
    }
    
    // 创建PIXI应用
    const app = new PIXI.Application({
      view: document.getElementById(canvasId),
      backgroundColor: 0xf0f0f0,
      antialias: true,
      width: 800,
      height: 600,
      autoDensity: true
    });

    console.log('PIXI应用创建成功');

    // 加载模型
    const model = await Live2DModel.from(modelConfig.path, { 
      motionPreload: MotionPreloadStrategy.NONE 
    });
    
    console.log(`${modelConfig.name} 模型加载成功`);

    // 添加模型到舞台
    app.stage.addChild(model);
    
    // 设置模型位置和大小
    model.anchor.set(0.5);
    model.x = app.view.width / 2;
    model.y = app.view.height / 2;
    model.scale.set(modelConfig.scale);

    console.log(`模型 ${modelConfig.name} 配置完成`);

    // 启用交互
    model.interactive = true;
    model.buttonMode = true;

    // 添加点击事件
    model.on('pointerdown', () => {
      console.log(`${modelConfig.name} 被点击`);
      if (model.motion && modelConfig.motions.length > 0) {
        const randomMotion = modelConfig.motions[Math.floor(Math.random() * modelConfig.motions.length)];
        model.motion(randomMotion);
      }
    });

    return { app, model, config: modelConfig };

  } catch (error) {
    console.error('Live2D初始化失败:', error);
    throw error;
  }
}

// 切换模型的函数
export async function switchModel(currentApp, newModelKey, canvasId = 'canvas_view') {
  try {
    // 清理当前应用
    if (currentApp) {
      currentApp.destroy(true);
    }
    
    // 初始化新模型
    return await initLive2DWithModel(newModelKey, canvasId);
  } catch (error) {
    console.error('模型切换失败:', error);
    throw error;
  }
}
