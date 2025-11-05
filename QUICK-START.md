# 🚀 Quick Start Guide

## Setup Checklist

### ☐ 1. Create GitHub Repo
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/sprout-changelog.git
git push -u origin main
```

### ☐ 2. Create Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create new app → "Changelog Bot"
3. Add scopes: `channels:history`, `channels:read`, `channels:replies`
4. Install to workspace
5. Copy Bot OAuth Token (xoxb-...)
6. Invite bot to channel: `/invite @Changelog Bot`

### ☐ 3. Add GitHub Secrets
Go to repo Settings → Secrets → Actions:

- `SLACK_BOT_TOKEN`: Your xoxb- token
- `SLACK_CHANNEL_ID`: `C05J9RTC9K6`
- `GCP_SA_KEY`: Your Google Cloud service account JSON

### ☐ 4. Test It!
1. Go to Actions tab in GitHub
2. Run "Update Changelog from Slack" manually
3. Check if it works!

## ✅ Done!

Your changelog will now auto-update at:
- 🌙 12:00 AM EST (midnight)
- 🌅 8:00 AM EST

## 📝 Message Format

Post in Slack like this:
```
TL;DR: Your update summary here about Sprout

Action: What to do about it
```

**Important:** Messages MUST contain "Sprout" to be included.
Messages with "spam" or help requests are automatically ignored.

## 📖 Full Documentation

See [AUTOMATION-SETUP.md](AUTOMATION-SETUP.md) for detailed instructions.

