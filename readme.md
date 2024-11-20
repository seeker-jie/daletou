# 大乐透开奖 Telegram 通知

通过 Telegram 机器人自动发送大乐透开奖信息。

## 设置步骤

1. 创建 Telegram 机器人
   - 在 Telegram 中找到 @BotFather
   - 发送 `/newbot` 命令创建新机器人
   - 保存获得的 bot token

2. 获取 Chat ID
   - 将机器人加入群组或直接与机器人对话
   - 访问 `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - 从返回的 JSON 中找到 chat_id

3. Fork 这个仓库

4. 设置 GitHub Secrets
   - 在仓库的 Settings -> Secrets 中添加：
     - TELEGRAM_BOT_TOKEN：你的 bot token
     - TELEGRAM_CHAT_ID：你的 chat id

5. 启用 GitHub Actions

## 功能特点

- 自动获取最新开奖结果
- 包含完整开奖信息（号码、奖池、销量等）
- 美化的消息格式
- 支持手动触发

## 通知时间

每周二、四、日早上 10:00 （北京时间）自动运行