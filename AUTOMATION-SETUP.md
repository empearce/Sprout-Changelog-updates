# 🤖 Automated Changelog Setup Guide

This guide will help you set up automatic changelog updates from Slack at 8 AM and 4 PM EST every day.

## 📋 Prerequisites

- GitHub account
- Slack workspace admin access (or ability to create Slack apps)
- Access to Shopify's Quick deployment
- Google Cloud credentials for Quick

## 🚀 Setup Steps

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it something like `sprout-changelog`
3. Make it **private** (recommended for internal tools)
4. Don't initialize with README (we'll push existing files)

### Step 2: Push Your Changelog to GitHub

```bash
cd "/Users/emilypearce/Desktop/Sprout Changelog"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Sprout Changelog with automation"

# Add your GitHub repo as remote (replace with your repo URL)
git remote add origin https://github.com/YOUR-USERNAME/sprout-changelog.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Name: `Changelog Bot`
4. Pick your Shopify workspace

#### Configure Bot Permissions:

1. Go to **"OAuth & Permissions"** in the sidebar
2. Under **"Scopes"** → **"Bot Token Scopes"**, add these three:
   - `channels:history` - Read messages from public channels
   - `channels:read` - View basic channel info
   - `channels:replies` - Read thread replies (needed for thread context)

3. Scroll up and click **"Install to Workspace"**
4. Authorize the app
5. **Copy the Bot User OAuth Token** (starts with `xoxb-`)
   - Keep this secret! You'll need it in Step 4

#### Add Bot to Your Channel:

1. Go to your Slack channel (#help-sprout-social or wherever)
2. Type `/invite @Changelog Bot`
3. The bot can now read messages from this channel

### Step 4: Configure GitHub Secrets

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**

Click **"New repository secret"** and add:

#### 4.1: SLACK_BOT_TOKEN
- Name: `SLACK_BOT_TOKEN`
- Value: Your bot token from Step 3 (starts with `xoxb-`)

#### 4.2: SLACK_CHANNEL_ID
- Name: `SLACK_CHANNEL_ID`
- Value: `C05J9RTC9K6` (or your channel ID)
  - To find channel ID: Right-click channel → View channel details → Copy ID

#### 4.3: GCP_SA_KEY (for Quick deployment)
- Name: `GCP_SA_KEY`
- Value: Your Google Cloud service account key JSON

**To get GCP credentials:**
```bash
# If you have gcloud CLI configured:
gcloud auth application-default print-access-token

# Or create a service account key:
# 1. Go to Google Cloud Console
# 2. IAM & Admin → Service Accounts
# 3. Create service account or use existing
# 4. Create JSON key
# 5. Paste entire JSON content as secret
```

### Step 5: Test the Automation

#### Manual Test:

1. Go to your GitHub repo
2. Click **Actions** tab
3. Select **"Update Changelog from Slack"** workflow
4. Click **"Run workflow"** → **"Run workflow"**
5. Watch it run!

#### What It Does:

1. ✅ Fetches messages from Slack (last 8 hours)
2. ✅ Looks for messages with "TL;DR:" in them
3. ✅ Extracts TL;DR and Action (if present)
4. ✅ Updates `changelog-data.json`
5. ✅ Commits changes to GitHub
6. ✅ Deploys to Quick automatically

### Step 6: Verify Automatic Schedule

The workflow is configured to run:
- **12:00 AM EST** (midnight, 05:00 UTC)
- **8:00 AM EST** (13:00 UTC)

**Note:** GitHub uses UTC times. The workflow accounts for EST (UTC-5).

If you're in EDT (daylight saving time, UTC-4), you may want to adjust:
```yaml
# In .github/workflows/update-changelog.yml
- cron: '0 4 * * *'   # 12 AM EDT (midnight)
- cron: '0 12 * * *'  # 8 AM EDT
```

## 📝 How to Format Slack Messages

For messages to be automatically picked up, format them like this:

```
TL;DR: Your summary of the update here - what happened, context, etc.

Action: What team members should do or be aware of (optional)
```

**Example:**
```
TL;DR: Fraud Ops now holding high-risk payouts up to full year - discovered via Trust Platform ticket linked from Sprout case.

Action: Be aware of extended payout hold policy for high-risk merchants and prepare for increased merchant complaints in Sprout.
```

### Message Filtering Rules

The bot will **ONLY** include messages that:
- ✅ Contain "TL;DR:" or "TLDR:"
- ✅ Contain the word "Sprout" (case-insensitive)

The bot will **IGNORE** messages that:
- ❌ Contain the word "spam"
- ❌ Appear to be help requests (phrases like "help with", "how do I", "need help", etc.)

### Thread Context Intelligence 🧵

The bot is **smart about threads**! It will:
- 📖 Read the ENTIRE thread (all replies)
- 🔍 Look for corrections, final resolutions, or updates
- ⚠️ Detect keywords like "actually", "confirmed", "should not", "incorrect", "final answer"
- ✏️ **Synthesize ONE comprehensive TL;DR** that includes the full conversation
- 📝 Extract Action items from thread if not in main message

**Important:** The bot reads from newest to oldest to find the **final resolution** first, ensuring the most accurate information.

**Example:**
If someone posts:
```
TL;DR: Guidance on filling user profiles in Sprout Social for frequent flyers
Action: Populate user profiles when confident information is accurate
```

And the thread conversation evolves:
```
Reply 1: "Hmm, is this allowed?"
Reply 2: "Checking with Kai..."
Reply 3: "Kai confirmed we should NOT add information to profiles for security reasons"
```

The bot will create:
```
TL;DR: Discussion about filling user profiles in Sprout Social for frequent flyers. 
       UPDATE: Kai confirmed we should NOT add information to Sprout profiles for 
       security reasons, despite potential efficiency gains.

Action: Do NOT populate user profiles in Sprout. This was clarified as a security concern.
```

This ensures the changelog reflects the **accurate final decision**, not just the initial discussion.

The bot will automatically:
- Extract the TL;DR and Action
- Get the date from the message timestamp
- Include important thread context
- Create the Slack link
- Add to your changelog

## 🔧 Customization

### Change Schedule

Edit `.github/workflows/update-changelog.yml`:

```yaml
schedule:
  - cron: '0 5 * * *'   # 12 AM EST (midnight)
  - cron: '0 13 * * *'  # 8 AM EST
```

### Change Lookback Time

Edit `scripts/fetch-slack-updates.py`:

```python
LOOKBACK_HOURS = 8  # Change to whatever you need
```

### Monitor Different Channel

Update the `SLACK_CHANNEL_ID` secret in GitHub with the new channel ID.

## 🐛 Troubleshooting

### Bot not finding messages?

1. Make sure bot is invited to the channel (`/invite @Changelog Bot`)
2. Check bot has correct permissions
3. Verify messages have "TL;DR:" in them

### Workflow not running?

1. Check GitHub Actions tab for errors
2. Verify all secrets are set correctly
3. Try manual run first to test

### Deployment failing?

1. Verify GCP credentials are correct
2. Check you have Quick CLI permissions
3. Test `quick deploy` locally first

### Messages being duplicated?

The script checks for duplicate Slack URLs, so this shouldn't happen. If it does:
1. Check `changelog-data.json` for duplicate entries
2. Review recent workflow runs for errors

## 📊 Monitoring

You can monitor the automation:

1. **GitHub Actions tab** - See all workflow runs
2. **Email notifications** - GitHub will email you on failures
3. **Slack** - Set up GitHub-Slack integration for notifications

## 🎉 You're Done!

Your changelog will now automatically update twice daily! The workflow:
- ✅ Runs at 8 AM and 4 PM EST
- ✅ Fetches new Slack messages
- ✅ Updates the JSON file
- ✅ Commits to GitHub
- ✅ Deploys to Quick
- ✅ All without any manual work!

## 💡 Pro Tips

1. **Test messages** - Post a test message with "TL;DR: Test entry" and run the workflow manually
2. **Review commits** - Check GitHub commits to see what was automatically added
3. **Adjust timing** - Change cron schedule if midnight/8am doesn't work for your team
4. **Add reactions** - Modify script to only process messages with a specific emoji reaction

## 📞 Need Help?

If you run into issues:
1. Check the workflow logs in GitHub Actions
2. Verify all secrets are configured
3. Test the Python script locally first
4. Check Slack bot permissions

---

**Questions?** DM Emily Pearce 💚

