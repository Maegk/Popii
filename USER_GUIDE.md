# 📘 Creative Fatigue Detection System - User Guide

**For Non-Technical Users**

Welcome! This guide will help you get started with the Creative Fatigue Detection System **without needing any programming knowledge**.

---

## 🎯 What Is This?

The Creative Fatigue Detection System helps you:
- Monitor your ad campaigns automatically
- Detect when your ads are getting "tired" (people are seeing them too much)
- Generate fresh ad variations using AI
- Rotate ads automatically to keep performance high

Think of it as your **24/7 ad performance assistant** that never sleeps!

---

## 📥 Step 1: Download

1. Download the project folder (you should already have this!)
2. Unzip it to a location you can find easily (like your Desktop or Documents folder)

---

## 🐳 Step 2: Install Docker Desktop

**What is Docker?** It's like a magic box that runs the entire application for you - no complicated setup needed!

### For Windows:
1. Go to https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer (double-click the downloaded file)
4. Follow the installation wizard (just click "Next" repeatedly)
5. Restart your computer when prompted

### For Mac:
1. Go to https://www.docker.com/products/docker-desktop
2. Click "Download for Mac" (choose Intel or Apple Silicon based on your Mac)
3. Open the downloaded .dmg file
4. Drag Docker to your Applications folder
5. Open Docker from Applications

### For Linux:
1. Go to https://docs.docker.com/desktop/install/linux-install/
2. Follow instructions for your distribution
3. Start Docker Desktop

**Important:** After installing, make sure Docker Desktop is running (you'll see a whale icon in your system tray/menu bar).

---

## 🚀 Step 3: Start the Application

Now for the easy part!

### Method 1: Double-Click (Easiest!)

**Windows Users:**
- Find the file called `start.bat`
- Double-click it
- A black window will appear - don't close it!
- Wait 30-60 seconds
- Your browser will open automatically

**Mac/Linux Users:**
- Find the file called `start.sh`
- Right-click it and select "Open" (first time only)
- If prompted, click "Open" to confirm
- Terminal will open - don't close it!
- Wait 30-60 seconds
- Your browser will open automatically

### Method 2: Use the Launcher Page

- Double-click `LAUNCH.html`
- It opens in your browser with easy-to-follow instructions
- Click the "Open Application" button once the system is running

---

## 🎨 Step 4: Using the Application

Once your browser opens, you'll see a beautiful dashboard!

### Dashboard (Home Page)

**What you'll see:**
- 📊 **Metric Cards** at the top showing:
  - Active Ad Sets (how many campaigns you're monitoring)
  - Active Creatives (how many ads are running)
  - Average CTR (click-through rate)
  - High Fatigue Alerts (ads that need attention)

- 📈 **Charts** showing:
  - Performance trends over time
  - Fatigue distribution (how many ads are low, moderate, high, or critical fatigue)
  - Recent rotations (when ads were automatically changed)

### Ad Sets Page

**What it does:**
- Shows all your advertising campaigns
- Color-coded fatigue scores:
  - 🟢 Green = Low fatigue (all good!)
  - 🟡 Yellow = Moderate fatigue (watch it)
  - 🟠 Orange = High fatigue (should refresh soon)
  - 🔴 Red = Critical fatigue (refresh immediately!)

**How to use:**
- Click "+ New Ad Set" to add a campaign
- Click the Play/Pause buttons to start/stop monitoring
- Click Settings to configure each ad set

### Creatives Page

**What it does:**
- Shows all your ad creatives (the actual ads)
- Displays performance metrics for each
- Lets you generate AI variations

**How to generate new ads:**
1. Click "Generate Variations" button
2. Select the original ad you want to vary
3. Choose variation types:
   - **Hook**: Different headlines
   - **Angle**: Different value propositions
   - **Copy**: Different body text
   - **Format**: Different ad types
4. Choose how many variations (1-10)
5. Click "Generate"
6. Wait 30-60 seconds - AI creates fresh versions!

### Fatigue Monitor

**What it does:**
- Real-time fatigue detection
- Shows which ads need attention
- Provides recommendations

**How to read it:**
- Look at the colored cards at top
- Scroll down to see individual ad sets
- Click "Rotate Creative" button for any ad showing "Action Required"

### Settings Page

**What to configure:**
- **Fatigue Thresholds**: When should we alert you?
  - Frequency: How many times someone sees an ad
  - CTR Drop: When click rate drops by X%
  - CPA Increase: When cost per acquisition rises by X%

- **Auto-Rotation**: Should we automatically rotate ads?
  - Toggle on/off
  - Set cooldown period (wait time between rotations)

- **API Keys**: Connect to your ad platforms
  - Meta (Facebook/Instagram)
  - Anthropic or OpenAI (for AI generation)

---

## 🌙 Dark Mode

Love dark mode? Click the moon/sun icon in the sidebar to toggle!

---

## 📱 Mobile Friendly

The entire interface works on your phone or tablet - check on the go!

---

## 🛑 Step 5: Stopping the Application

### Windows:
- Double-click `stop.bat`
OR
- Close the black window that appeared when you started

### Mac/Linux:
- Double-click `stop.sh`
OR
- Press `Ctrl+C` in the terminal window
OR
- Close the terminal window

---

## ❓ Common Questions

### Q: The application won't start!
**A:** Make sure Docker Desktop is running. Look for the whale icon in your system tray/menu bar.

### Q: My browser didn't open automatically
**A:** Manually go to http://localhost:3000

### Q: I see an error message
**A:**
1. Make sure Docker Desktop is running
2. Wait a full 60 seconds for everything to start
3. Try restarting Docker Desktop
4. Run the stop script, then start again

### Q: How do I connect my Facebook ads?
**A:**
1. Go to Settings page
2. Enter your Meta Access Token
3. Enter your Ad Account ID
4. Click Save

### Q: The AI generation isn't working
**A:** You need to add an API key in Settings:
- Get an Anthropic API key from https://console.anthropic.com/
OR
- Get an OpenAI API key from https://platform.openai.com/

### Q: Is my data safe?
**A:** Yes! Everything runs on YOUR computer. No data is sent anywhere except to the AI APIs for generation (if you use that feature).

### Q: Can I run this 24/7?
**A:** Yes! Just leave the application running. Docker will keep everything working smoothly.

### Q: How do I update the application?
**A:**
1. Stop the application
2. Download the new version
3. Replace the old files
4. Start again!

---

## 💡 Tips for Best Results

1. **Check Daily**: Look at the dashboard each day to spot trends
2. **Act on High Fatigue**: When you see orange or red warnings, generate new creatives
3. **Use Auto-Rotation**: Enable it in Settings for hands-free management
4. **Try Different Variations**: Generate multiple types (hook, angle, copy) to see what works
5. **Monitor Performance**: Compare CTR and CPA before and after rotations

---

## 🎓 Understanding the Metrics

### CTR (Click-Through Rate)
- **What it is**: Percentage of people who click your ad
- **Good range**: 2-5% (depends on industry)
- **If it's dropping**: Time to refresh!

### CPA (Cost Per Acquisition)
- **What it is**: How much you pay to get a customer
- **What to watch**: If it's increasing, you're paying more
- **If it's rising**: Your ad is fatigued

### Frequency
- **What it is**: Average times each person sees your ad
- **Sweet spot**: 3-5 times
- **Too high**: Above 6-7 = fatigue risk

### Fatigue Score
- **What it is**: Our AI's prediction of how tired your ad is
- **Scale**: 0-100%
- **0-30%**: Low (good!)
- **30-60%**: Moderate (watch it)
- **60-80%**: High (refresh soon)
- **80-100%**: Critical (refresh NOW!)

---

## 🎉 You're All Set!

You now have a powerful ad monitoring system running!

**Next Steps:**
1. Add your first ad set
2. Connect your ad accounts (Settings → API Configuration)
3. Let it monitor for a few days
4. Generate your first AI variation
5. Watch your performance improve!

**Need More Help?**
- Check the dashboard tooltips (hover over elements)
- View the API documentation at http://localhost:8000/docs
- Read the technical README.md for advanced features

---

## 🚀 Happy Advertising!

Remember: The best ads are fresh ads. Let this system help you stay ahead of fatigue!

---

*Last Updated: 2025*
*Version: 1.0.0*
