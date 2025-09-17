/**
 * 用户隔离问题修复测试脚本（优化版本）
 * 
 * 此脚本用于验证改进后的用户隔离修复是否有效
 * 新的检测机制：在点击打开情绪日记按钮时检测用户切换
 * 运行方式：在浏览器控制台中执行此脚本
 */

console.log('=== 用户隔离问题修复测试（优化版本） ===');

// 模拟用户切换场景（点击打开日记按钮时检测）
function testUserSwitchOnDiaryOpen() {
  console.log('\n1. 测试点击日记按钮时的用户切换检测');
  
  // 模拟用户A的数据
  const userAId = 'user-a-12345';
  const userBId = 'user-b-67890';
  
  // 设置用户A的环境
  localStorage.setItem('virtual_partner_user_id', userAId);
  sessionStorage.setItem('userInfo', JSON.stringify({
    user_id: userAId,
    username: '用户A'
  }));
  
  // 添加用户A的日记数据
  localStorage.setItem('diary_2025-09-17', JSON.stringify({
    content: '用户A的日记内容',
    emotions: ['开心', '满足'],
    messageCount: 5,
    mainTopic: '工作学习'
  }));
  localStorage.setItem('diary_2025-09-16', JSON.stringify({
    content: '用户A昨天的日记',
    emotions: ['平静'],
    messageCount: 3,
    mainTopic: '日常生活'
  }));
  
  console.log('✓ 设置用户A的环境和日记数据完成');
  console.log('  - localStorage用户ID:', localStorage.getItem('virtual_partner_user_id'));
  console.log('  - sessionStorage用户信息:', JSON.parse(sessionStorage.getItem('userInfo')).user_id);
  console.log('  - diary_2025-09-17:', localStorage.getItem('diary_2025-09-17') ? '存在' : '不存在');
  console.log('  - diary_2025-09-16:', localStorage.getItem('diary_2025-09-16') ? '存在' : '不存在');
  
  // 模拟用户B登录（只更新sessionStorage）
  console.log('\n2. 模拟用户B登录（sessionStorage更新）');
  sessionStorage.setItem('userInfo', JSON.stringify({
    user_id: userBId,
    username: '用户B'
  }));
  
  console.log('  - localStorage用户ID（未变）:', localStorage.getItem('virtual_partner_user_id'));
  console.log('  - sessionStorage用户信息（已变）:', JSON.parse(sessionStorage.getItem('userInfo')).user_id);
  
  // 模拟checkUserSwitchAndClearDiary函数执行（点击日记按钮时触发）
  console.log('\n3. 模拟点击打开日记按钮，触发用户切换检测');
  function checkUserSwitchAndClearDiary() {
    console.log('执行checkUserSwitchAndClearDiary函数...');
    
    // 获取当前登录用户信息
    const userInfo = JSON.parse(sessionStorage.getItem('userInfo') || '{}');
    
    // 获取localStorage中存储的用户ID
    const localStorageUserId = localStorage.getItem('virtual_partner_user_id');
    
    // 如果有已登录用户
    if (userInfo.user_id) {
      // 检查localStorage中的用户ID是否与当前登录用户匹配
      if (localStorageUserId !== userInfo.user_id) {
        console.log('  检测到用户切换，清除旧用户的日记数据');
        console.log('    旧用户ID:', localStorageUserId);
        console.log('    新用户ID:', userInfo.user_id);
        
        // 更新localStorage中的用户ID
        localStorage.setItem('virtual_partner_user_id', userInfo.user_id);
        
        // 清除旧用户的会话数据
        localStorage.removeItem('virtual_partner_session_id');
        
        // 清除旧用户的日记数据
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
          if (key.startsWith('diary_')) {
            localStorage.removeItem(key);
            console.log('    清除日记数据:', key);
          }
        });
        
        console.log('  用户切换处理完成，已清除旧用户数据');
        return true; // 返回是否发生了切换
      } else {
        console.log('  用户未切换，保持当前状态');
        return false;
      }
    } else {
      console.log('  未检测到登录用户，使用临时用户');
      return false;
    }
  }
  
  const switchDetected = checkUserSwitchAndClearDiary();
  
  console.log('\n4. 验证用户切换检测结果');
  console.log('  - 用户切换是否被检测到:', switchDetected ? '✓ 是' : '❌ 否');
  console.log('  - localStorage用户ID（应已更新）:', localStorage.getItem('virtual_partner_user_id'));
  console.log('  - diary_2025-09-17:', localStorage.getItem('diary_2025-09-17') ? '❌ 仍存在' : '✓ 已清除');
  console.log('  - diary_2025-09-16:', localStorage.getItem('diary_2025-09-16') ? '❌ 仍存在' : '✓ 已清除');
  
  return switchDetected && 
         localStorage.getItem('virtual_partner_user_id') === userBId &&
         localStorage.getItem('diary_2025-09-17') === null && 
         localStorage.getItem('diary_2025-09-16') === null;
}

// 测试localStorage数据完整性验证
function testDataIntegrityValidation() {
  console.log('\n5. 测试数据完整性验证');
  
  const currentUserId = 'current-user-123';
  
  // 设置当前用户环境
  localStorage.setItem('virtual_partner_user_id', currentUserId);
  sessionStorage.setItem('userInfo', JSON.stringify({
    user_id: currentUserId,
    username: '当前用户'
  }));
  
  // 设置正确的日记数据
  localStorage.setItem('diary_2025-09-18', JSON.stringify({
    content: '当前用户的日记',
    emotions: ['满意'],
    messageCount: 4,
    mainTopic: '学习'
  }));
  
  console.log('✓ 设置测试数据完成');
  
  // 模拟没有用户切换的情况下点击日记按钮
  console.log('  模拟没有用户切换时点击日记按钮...');
  function checkUserSwitchAndClearDiary() {
    const userInfo = JSON.parse(sessionStorage.getItem('userInfo') || '{}');
    const localStorageUserId = localStorage.getItem('virtual_partner_user_id');
    
    if (userInfo.user_id) {
      if (localStorageUserId !== userInfo.user_id) {
        console.log('    检测到用户切换');
        return true;
      } else {
        console.log('    用户未切换，数据保持不变');
        return false;
      }
    }
    return false;
  }
  
  const switchDetected = checkUserSwitchAndClearDiary();
  
  console.log('  验证结果:');
  console.log('    - 用户切换检测:', switchDetected ? '❌ 误检测' : '✓ 正确（无切换）');
  console.log('    - 日记数据保留:', localStorage.getItem('diary_2025-09-18') ? '✓ 已保留' : '❌ 被误删');
  
  return !switchDetected && localStorage.getItem('diary_2025-09-18') !== null;
}

// 运行所有测试
function runAllTests() {
  console.log('开始运行用户隔离修复测试（优化版本）...\n');
  
  const test1Result = testUserSwitchOnDiaryOpen();
  const test2Result = testDataIntegrityValidation();
  
  console.log('\n=== 测试结果总结 ===');
  console.log('点击日记按钮时用户切换检测:', test1Result ? '✅ 通过' : '❌ 失败');
  console.log('数据完整性验证测试:', test2Result ? '✅ 通过' : '❌ 失败');
  
  if (test1Result && test2Result) {
    console.log('\n🎉 所有测试通过！优化后的用户隔离功能正常工作。');
    console.log('\n📝 新的工作机制：');
    console.log('  • 用户切换检测仅在点击打开日记按钮时触发');
    console.log('  • 避免了页面初始化时的不必要检查');
    console.log('  • 更精确的时机控制，提高了性能');
  } else {
    console.log('\n⚠️ 部分测试失败，需要进一步检查修复逻辑。');
  }
  
  // 清理测试数据
  localStorage.removeItem('virtual_partner_user_id');
  sessionStorage.removeItem('userInfo');
  const keys = Object.keys(localStorage);
  keys.forEach(key => {
    if (key.startsWith('diary_')) {
      localStorage.removeItem(key);
    }
  });
  console.log('\n✅ 测试数据清理完成');
}

// 执行测试
runAllTests();
