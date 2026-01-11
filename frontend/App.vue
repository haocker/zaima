
<script>
export default {
  onLaunch() {
    // 应用启动时执行
    console.log('App Launch');
    // 初始化应用，如获取设备ID、检查登录状态等
    this.initApp();
  },
  onShow() {
    // 应用显示时执行
    console.log('App Show');
  },
  onHide() {
    // 应用隐藏时执行
    console.log('App Hide');
  },
  methods: {
    initApp() {
      // 初始化应用逻辑
      // 1. 生成或获取设备ID
      // 2. 检查登录状态
      // 3. 加载配置信息
      this.getDeviceId();
    },
    getDeviceId() {
      // 获取或生成设备ID
      let deviceId = uni.getStorageSync('deviceId');
      if (!deviceId) {
        // 生成设备ID
        deviceId = this.generateDeviceId();
        uni.setStorageSync('deviceId', deviceId);
      }
      console.log('Device ID:', deviceId);
    },
    generateDeviceId() {
      // 生成唯一设备ID
      return 'device_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
  }
};
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 修复 uniapp 页面高度问题 */
page {
  height: 100%;
}

uni-page-wrapper {
  height: 100%;
}

uni-page-body {
  height: 100%;
  overflow: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: #f8f8f8;
  color: #333;
  line-height: 1.6;
}

#app {
  width: 100%;
  overflow-x: hidden;
}

/* 全局按钮样式 */
button {
  border: none;
  outline: none;
  cursor: pointer;
  font-size: 16px;
  padding: 10px 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
}


</style>