# Sprout Changelog

A beautiful, modern changelog website for tracking Sprout updates and improvements.

✨ **Now with automation!** Changelog automatically updates from Slack at 12 AM (midnight) and 8 AM EST. See [AUTOMATION-SETUP.md](AUTOMATION-SETUP.md) for setup instructions.

## 📋 Features

- **Modern Design**: Clean, gradient-based design with smooth animations
- **Search Functionality**: Instantly filter changelog entries
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Categorized Updates**: Clear sections for new features, improvements, and bug fixes
- **Visual Badges**: Color-coded badges for different types of updates

## 🚀 Deployment

This site is configured to deploy with Shopify's Quick CLI.

### Prerequisites

1. Install the Quick CLI:
```bash
npm i -g @shopify/quick
```

2. Authenticate with gcloud (if not already done):
```bash
gcloud auth login
```

### Deploy

To deploy this site:

```bash
quick deploy . sprout-changelog
```

The site will be available at: `https://sprout-changelog.quick.shopify.io`

**Note:** If you encounter a "Failed to sync files to Google Cloud Storage" error, this is a backend permissions issue. You may need to:
- Contact Shopify's Quick CLI support team
- Verify your GCS bucket permissions
- Check with your infrastructure team about Quick deployment access

### Watch Mode

To automatically redeploy on changes:

```bash
quick deploy . sprout-changelog --watch
```

## 📁 Files

- `index.html` - Main changelog page with embedded styles and functionality
- `changelog-data.json` - **Changelog entries data** (edit this file to add new entries!)
- `AGENTS.md` - Quick site configuration file
- `README.md` - This file

## ✏️ Adding New Changelog Entries

**Easy Updates!** Changelog entries are now managed in a separate JSON file:

1. Open `changelog-data.json`
2. Add a new entry at the **top** of the `entries` array:

```json
{
  "month": "november",
  "year": "2025",
  "date": "November 15, 2025",
  "tldr": "Your TL;DR summary here",
  "action": "Action item for the team (optional)",
  "slackUrl": "https://shopify.slack.com/archives/..."
}
```

3. Save the file and deploy!

**Fields:**
- `month`: lowercase month name (november, october, etc.)
- `year`: year as string
- `date`: Full display date
- `tldr`: The main update summary
- `action`: (Optional) Action items for the team - leave as empty string `""` if none
- `slackUrl`: Link to the Slack thread

**💡 Pro Tip:** You can use AI to help format Slack messages into JSON entries! Just paste the Slack message and ask it to format it as a changelog entry.

**📅 New Month?** When starting a new month:
1. Add the month to the month navigation buttons in `index.html` (search for "Jump to Month")
2. Add the month to the `months` and `monthNames` arrays in the JavaScript
3. Make sure entries in the JSON use the correct lowercase month name

## 🎨 Customization

You can customize the appearance by editing `index.html`:

1. **Change Colors**: Modify the CSS variables in the `:root` section
2. **Update Branding**: Change the logo emoji (🍃) and title text in the header
3. **Add New Months**: Update the `months` and `monthNames` arrays in the JavaScript

## 📝 License

© 2025 Sprout. All rights reserved.

