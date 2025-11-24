# 📥 Download and Install

## Quick Start for Non-Technical Users

### ✅ What You Need
- A computer (Windows, Mac, or Linux)
- Internet connection
- 10 GB free disk space
- That's it!

---

## 📦 Step 1: Download

### Option A: Download from GitHub
1. Click the green "Code" button at the top of this page
2. Click "Download ZIP"
3. Save the file to your Desktop or Downloads folder
4. Right-click the ZIP file and choose "Extract All"

### Option B: Clone with Git (if you know Git)
```bash
git clone <repository-url>
cd Popii
```

---

## 🐳 Step 2: Install Docker Desktop

**This is the ONLY thing you need to install!**

### Windows:
1. Go to: https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Double-click the installer
4. Follow the wizard (keep clicking "Next")
5. Restart your computer

### Mac:
1. Go to: https://www.docker.com/products/docker-desktop
2. Download for your Mac type:
   - Apple Silicon (M1/M2/M3) OR
   - Intel Chip
3. Drag Docker to Applications folder
4. Open Docker from Applications

### Linux:
Follow instructions at: https://docs.docker.com/desktop/install/linux-install/

---

## 🚀 Step 3: Start the Application

### The EASIEST Way:

1. **Open the project folder** (where you extracted the files)

2. **Double-click one file:**
   - **Windows**: Double-click `start.bat`
   - **Mac/Linux**: Double-click `start.sh`

3. **Wait 30-60 seconds**
   - A window will appear (don't close it!)
   - You'll see text scrolling (that's normal!)

4. **Browser opens automatically!**
   - The application will open at http://localhost:3000
   - If it doesn't, manually open that link

### Alternative: Use the Launcher

1. Double-click `LAUNCH.html`
2. Follow the on-screen instructions
3. Click "Open Application"

---

## 🎨 Step 4: Start Using It!

You'll see a beautiful dashboard with:
- 📊 Real-time metrics
- 📈 Performance charts
- ✨ AI creative generation
- ⚠️ Fatigue alerts

**First time?** Check out `USER_GUIDE.md` for a complete walkthrough!

---

## 🛑 How to Stop

### Windows:
- Double-click `stop.bat`
OR
- Close the black window

### Mac/Linux:
- Double-click `stop.sh`
OR
- Close the terminal window

---

## ❓ Troubleshooting

### "It won't start!"
**Solution:**
1. Make sure Docker Desktop is running (look for whale icon in taskbar/menu)
2. Wait a full 60 seconds
3. Try running stop script, then start script again

### "Port already in use"
**Solution:**
Something else is using the same port. Either:
- Stop other applications using ports 3000 or 8000
- Or modify `docker-compose.yml` to use different ports

### "Docker is not installed"
**Solution:**
- Install Docker Desktop (see Step 2 above)
- Restart your computer after installing

### "Permission denied" (Mac/Linux)
**Solution:**
Run this in terminal:
```bash
chmod +x start.sh stop.sh
```

---

## 🎯 What's Included?

```
📁 Popii/
├── 📄 LAUNCH.html          ← Open this in browser for guided start
├── 📄 start.bat            ← Windows: Double-click to start
├── 📄 start.sh             ← Mac/Linux: Double-click to start
├── 📄 stop.bat             ← Windows: Stop the application
├── 📄 stop.sh              ← Mac/Linux: Stop the application
├── 📄 USER_GUIDE.md        ← Complete user guide (READ THIS!)
├── 📄 README.md            ← Technical documentation
├── 📄 QUICKSTART.md        ← Quick technical setup
└── 📄 docker-compose.yml   ← Docker configuration (don't touch!)
```

---

## 🔗 Quick Links

Once running, access:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Monitoring**: http://localhost:5555 (Celery Flower)
- **Metrics**: http://localhost:9090 (Prometheus)

---

## 💡 Pro Tips

1. **Keep Docker Running**: Don't quit Docker Desktop while using the app
2. **Bookmark localhost:3000**: For easy access
3. **Read the User Guide**: `USER_GUIDE.md` has everything explained in plain English
4. **Dark Mode Available**: Toggle in the sidebar!
5. **Mobile Friendly**: Works on phone/tablet too

---

## 🎓 Learning Path

**Complete Beginner?**
1. Read this file (you're doing it! ✅)
2. Install Docker Desktop
3. Double-click `start.bat` or `start.sh`
4. Open `USER_GUIDE.md` once app is running

**Slightly Technical?**
1. Read `QUICKSTART.md`
2. Read `README.md` for architecture details
3. Check out `examples/` folder for code samples

**Developer?**
1. Read `README.md`
2. Read `CONTRIBUTING.md`
3. Check `frontend/README.md` for frontend details
4. Explore the codebase!

---

## 🆘 Need Help?

1. **First**: Read `USER_GUIDE.md` - answers 90% of questions!
2. **Second**: Check this troubleshooting section
3. **Third**: Open an issue on GitHub (if using GitHub)
4. **Fourth**: Check Docker Desktop logs for errors

---

## 🎉 Ready?

You're just **3 clicks** away from a powerful ad monitoring system:

1. ✅ Download files
2. ✅ Install Docker Desktop
3. ✅ Double-click `start.bat` or `start.sh`

**That's it!** No terminal commands, no coding, no complexity.

---

## ⚡ Super Quick Version

```
1. Download & extract
2. Install Docker Desktop
3. Double-click start.bat (Windows) or start.sh (Mac/Linux)
4. Wait 60 seconds
5. Browser opens automatically
6. Start using!
```

---

**Made with ❤️ for non-technical users**

*No command line required. No coding needed. Just double-click and go!*
