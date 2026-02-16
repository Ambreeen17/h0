# 🎬 Hackathon Video Production Guide

**For**: Personal AI Employee Hackathon 0
**Project**: AI Employee Vault - Platinum Tier
**Target Duration**: 5-10 minutes (max 15 minutes for most hackathons)
**Date**: 2026-02-16

---

## 🎯 VIDEO STRUCTURE (Recommended: 8-10 minutes)

### Time Breakdown

1. **Introduction** (1 minute) - Hook the judges
2. **System Overview** (1 minute) - High-level architecture
3. **Live Demo** (4-5 minutes) - Show it working
4. **Key Features** (1-2 minutes) - Highlight innovation
5. **GitHub Repository** (1 minute) - Show code quality
6. **Conclusion** (30 seconds) - Final summary

---

## 📹 RECORDING SOFTWARE OPTIONS

### Option 1: Windows Built-in (Recommended for You)
**Xbox Game Bar** (Windows 10/11)
- **How to use**: Press `Win + G`
- **Features**: Screen recording, microphone capture
- **Output**: MP4 video in `Captures/Videos` folder
- **Pros**: Free, installed, good quality
- **Cons**: Basic editing only

**Steps**:
1. Press `Win + G` to open Game Bar
2. Click "Capture" (screen recording)
3. Select window or full screen
4. Click record button (or `Win + Alt + R`)
5. Stop recording when done

### Option 2: OBS Studio (Free, Professional)
- **Download**: https://obsproject.com/
- **Features**: Advanced recording, transitions, multiple sources
- **Pros**: Professional quality, free, watermark-free
- **Cons**: Learning curve

### Option 3: Microsoft PowerPoint (Built-in)
- **Features**: Record slideshow, screen recording
- **Pros**: Already installed, easy to use
- **Cons**: Basic features

---

## 🎬 RECOMMENDED: Xbox Game Bar (Windows)

Since you're on Windows 10, use the built-in Xbox Game Bar:

### Setup (5 minutes)
```bash
1. Open Xbox Game Bar: Win + G
2. Click settings (gear icon)
3. Enable "Capture cursor when recording a game window"
4. Set recording quality to 1080p or higher
5. Set audio to capture system audio + microphone
```

### Recording
```bash
1. Press Win + G to open Game Bar
2. Click "Start recording" (or Win + Alt + R)
3. Do your demo
4. Press Win + Alt + R to stop
5. Video saved to: C:\Users\User\Videos\Captures
```

---

## 📝 VIDEO SCRIPT WITH FILES TO OPEN

### Part 1: INTRODUCTION (1 minute)

**Action**: Face camera or show slides
**Script**:
```
"Hi, I'm submitting AI Employee Vault for Hackathon 0.
This is a Platinum tier autonomous AI employee system
built with Claude Code. Let me show you what it can do."
```

---

### Part 2: SYSTEM OVERVIEW (1 minute)

**File to Open**: `README.md`

**Actions**:
1. Open VS Code or your preferred editor
2. Open `README.md`
3. Scroll through to show key sections

**Script**:
```
"The project is a Digital Full-Time Equivalent AI employee.
It has four tiers: Bronze, Silver, Gold, and Platinum.
I've completed all Platinum tier requirements including
hybrid cloud/local architecture, delegation system,
and production-ready security."
```

**Show**:
- Tier declaration section
- Architecture overview
- Key features list

---

### Part 3: LIVE DEMO (4-5 minutes) ⭐ MOST IMPORTANT

#### 3a. Terminal 1: Health Check (30 seconds)

**Open**: Terminal/Command Prompt

**Commands**:
```bash
cd C:\HACKATHON 0
python skills/health_monitor.py --summary
```

**What to Show**:
- All services showing "healthy"
- Green checkmarks in terminal

**Script**:
```
"First, let me verify the system is healthy.
All services are operational - cloud zone, local zone,
zone synchronization, everything is healthy."
```

#### 3b. Terminal 2: Cloud Zone (45 seconds)

**Open**: New Terminal window

**Commands**:
```bash
python skills/cloud_zone_manager.py --status
```

**What to Show**:
- JSON output with cloud zone status
- Capabilities list
- Drafts created count

**Script**:
```
"The cloud zone operates 24/7 handling drafting,
triage, and analysis. It can process tasks without
needing human intervention."
```

#### 3c. Terminal 3: Local Zone (45 seconds)

**Open**: New Terminal window

**Commands**:
```bash
python skills/local_zone_manager.py --status
```

**What to Show**:
- Local zone status
- Approval capabilities
- Security rules

**Script**:
```
"The local zone handles sensitive operations like
approvals, banking, and credential access.
It enforces human-in-the-loop oversight."
```

#### 3d. Live Task Creation (1 minute)

**Open**: File Explorer → Navigate to `test_watches` folder

**Actions**:
1. Create a simple text file in `test_watches/`
2. Save it as `demo_task.md`
3. Show it appear in the folder

**Script**:
```
"Let me demonstrate the perception layer.
I'll create a task file in the test watches folder.
The file system watcher would detect this automatically
and create a task in the vault."
```

#### 3e. Run Test Suite (1 minute)

**Open**: Terminal

**Commands**:
```bash
python tests/test_suite.py --all
```

**What to Show**:
- Tests running live
- "Test Summary: 20/20 passed"
- All green [PASS] messages

**Script**:
```
"I've created a comprehensive test suite with 20 tests
covering all components. Let me run it now.
All 20 tests pass - this validates cloud zone operations,
local zone approvals, zone synchronization, health monitoring,
and the complete end-to-end workflow."
```

#### 3f. Zone Synchronization Demo (30 seconds)

**Open**: Terminal

**Commands**:
```bash
python skills/zone_sync_manager.py --status
```

**Script**:
```
"The zone sync manager handles delegation between zones
using claim-by-move architecture. It enforces markdown-only
sync and filters secrets for security."
```

---

### Part 4: KEY FEATURES (1-2 minutes)

#### 4a. Documentation (30 seconds)

**File**: Open `docs/ARCHITECTURE_DIAGRAMS.md`

**Actions**:
1. Scroll through to show Mermaid diagrams
2. Stop at key diagrams (system overview, zone architecture)

**Script**:
```
"I've created comprehensive documentation including
15 architecture diagrams showing the complete system design,
security boundaries, and data flow."
```

#### 4b. API Documentation (30 seconds)

**File**: Open `docs/API_DOCUMENTATION.md`

**Actions**:
1. Show the table of contents
2. Scroll to show API reference sections

**Script**:
```
"Complete API documentation for all 15 skills with
function signatures, parameters, and usage examples."
```

#### 4c. Enhanced Features (30 seconds)

**Files**: Show enhanced features

**Actions**:
1. Open `skills/task_prioritizer.py`
2. Open `skills/analytics_dashboard.py`
3. Open `skills/backup_manager.py`

**Script**:
```
"I've also added enhanced features including
intelligent task prioritization, analytics dashboard,
and automated backup management."
```

---

### Part 5: GITHUB REPOSITORY (1 minute)

#### 5a. Open Repository in Browser

**URL**: https://github.com/Ambreeen17/h0

**Actions**:
1. Navigate to repository
2. Show the README
3. Scroll to see project structure

**Script**:
```
"The complete source code is available on GitHub.
You can see the comprehensive README and project structure."
```

#### 5b. Show Code Quality (30 seconds)

**GitHub Sections to Show**:
1. **Code Tab**: Click to show file structure
2. **skills/** folder: Show the agent skills
3. **watchers/** folder: Show perception layer
4. **tests/** folder: Show test coverage
5. **docs/** folder: Show documentation

**Script**:
```
"The code is well-organized with separate folders for
skills, watchers, tests, and documentation.
All components follow the Agent Skills pattern."
```

#### 5c. Show Commits (30 seconds)

**GitHub Actions**:
1. Click "commits" (show recent commits)
2. Show the detailed commit messages

**Script**:
```
"The git history shows professional commit practices
with clear descriptions and co-authorship attribution."
```

---

### Part 6: CONCLUSION (30 seconds)

**Action**: Face camera or show final slide

**Script**:
```
"To summarize, AI Employee Vault is a production-ready
Digital FTE system with:

✅ Complete Platinum tier implementation
✅ Hybrid cloud/local architecture
✅ Secure delegation system
✅ Human-in-the-loop oversight
✅ Comprehensive testing (20/20 tests passing)
✅ Professional documentation

It demonstrates how AI agents can operate as
structured autonomous employees, not just chatbots.

Thank you for watching!"
```

---

## 📋 FILES TO HAVE OPEN DURING VIDEO

### Before Recording (Prep These)

1. **VS Code** with these files open in tabs:
   - `README.md` (first tab)
   - `PLATINUM_DEMO.md` (second tab)
   - `docs/ARCHITECTURE_DIAGRAMS.md` (third tab)
   - `skills/cloud_zone_manager.py` (fourth tab)
   - `skills/health_monitor.py` (fifth tab)

2. **Browser** open to:
   - https://github.com/Ambreeen17/h0

3. **File Explorer** open to:
   - `C:\HACKATHON 0\AI_Employee_Vault`
   - `C:\HACKATHON 0\AI_Employee_Vault_Cloud`
   - `C:\HACKATHON 0\test_watches`

4. **3 Terminal Windows** arranged:
   - Terminal 1: For health checks
   - Terminal 2: For cloud/local zone status
   - Terminal 3: For running tests

### During Recording (Switch Between These)

**Switch to VS Code** to show:
- Architecture diagrams
- API documentation
- Code structure

**Switch to Browser** to show:
- GitHub repository
- Commit history
- File structure

**Switch to Terminal** to show:
- Live commands
- Test execution
- System status

---

## 🎬 RECORDING CHECKLIST

### Before Recording (15 minutes)

- [ ] Review script 2-3 times
- [ ] Open all files in VS Code tabs
- [ ] Open GitHub repository in browser
- [ ] Open 3 terminal windows
- [ ] Navigate to project directory in all terminals
- [ ] Test recording (record 30 seconds, play back)
- [ ] Close unnecessary applications
- [ ] Clear desktop clutter
- [ ] Disable notifications (Focus Assist)

### During Recording

- [ ] Speak clearly and confidently
- [ ] Point to relevant parts of screen
- [ ] Don't rush - let viewers see the output
- [ ] Switch windows smoothly
- [ ] Explain what you're doing
- [ ] Keep energy high

---

## 💡 TIPS FOR A GREAT VIDEO

### Do's ✅

- ✅ **Start with a hook** - what makes this special?
- ✅ **Show, don't just tell** - demonstrate live
- ✅ **Use your voice** - be enthusiastic
- ✅ **Keep it moving** - change views every 30-60 seconds
- ✅ **Highlight innovation** - Platinum tier features
- ✅ **Show tests passing** - validates quality
- ✅ **Show code quality** - clean architecture
- ✅ **Mention "built with Claude Code"** - shows tool usage

### Don'ts ❌

- ❌ Don't read directly from slides
- ❌ Don't go too fast (let viewers see output)
- ❌ Don't have dead air (keep talking)
- ❌ Don't make excuses (own your work)
- ❌ Don't show sensitive data (use .env.example)
- ❌ Don't skip the test run (shows quality)
- ❌ Don't ramble (stay on script)

---

## 🎬 ADVANCED: Multi-Source Recording (Optional)

If you want professional-looking video with multiple sources:

### Use OBS Studio Setup

**Sources to Add**:
1. **Display Capture**: Your main screen
2. **Window Capture**: VS Code (for code)
3. **Window Capture**: Terminal (for commands)
4. **Browser Source**: GitHub (for repo)
5. **Microphone/Aux**: Your voice

**Scene Transitions**:
- Scene 1: Introduction (Display + Webcam)
- Scene 2: Demo (Display + Terminal)
- Scene 3: Code (Display + VS Code)
- Scene 4: GitHub (Display + Browser)
- Scene 5: Conclusion (Display + Webcam)

---

## 📊 TIMING RECOMMENDATIONS

### For 5-Minute Video (Short & Punchy)
- Intro: 30 seconds
- System Overview: 30 seconds
- Live Demo: 2.5 minutes
- GitHub: 30 seconds
- Conclusion: 30 seconds

### For 10-Minute Video (Recommended)
- Intro: 1 minute
- System Overview: 1 minute
- Live Demo: 5 minutes
- GitHub: 2 minutes
- Conclusion: 30 seconds

### For 15-Minute Video (Detailed)
- Intro: 1 minute
- System Overview: 2 minutes
- Live Demo: 8 minutes
- GitHub: 3 minutes
- Conclusion: 1 minute

---

## 🎯 WHAT JUDGES WANT TO SEE

### Must Show (Priority Order)

1. ✅ **It Works** - Live demo of functionality
2. ✅ **Complete Implementation** - All tiers done
3. ✅ **Innovation** - What makes this special
4. ✅ **Code Quality** - Well-organized, tested
5. ✅ **Documentation** - Professional, comprehensive
6. ✅ **Architecture** - Thoughtful design

### Nice to Show

- Test results (all passing)
- Architecture diagrams
- API documentation
- GitHub commit history
- Enhanced features

---

## 🎬 POST-PROCESSING (Optional)

### Basic Editing (Windows Photos)

1. Open Xbox Game Bar capture in Photos app
2. Trim start/end
3. Add simple transitions
4. Export as MP4

### Advanced Editing (DaVinci Resolve - Free)

1. Import video
2. Cut sections
3. Add text overlays
4. Add transitions
5. Export to YouTube/MP4

---

## 📤 UPLOAD DESTINATIONS

### Check Hackathon Requirements

Common platforms:
- **YouTube** (unlisted or public)
- **Vimeo** (password protected)
- **Google Drive** (shareable link)
- **Direct upload** to hackathon platform

**Naming Convention**:
```
AI_Employee_Vault_Hackathon0_Submission_YourName.mp4
```

---

## 🎬 QUICK START RECORDING GUIDE

### Step-by-Step (Fast Track)

**Step 1: Setup (5 minutes)**
```bash
1. Open VS Code with key files
2. Open GitHub in browser
3. Open 3 terminal windows
4. Navigate to project: cd C:\HACKATHON 0
```

**Step 2: Practice Run (5 minutes)**
```bash
1. Run through the script once
2. Time each section
3. Practice smooth transitions
```

**Step 3: Record (10 minutes)**
```bash
1. Press Win + G (Xbox Game Bar)
2. Click "Start recording"
3. Follow the script
4. Press Win + Alt + R to stop
```

**Step 4: Review (5 minutes)**
```bash
1. Watch the recording
2. Check audio is clear
3. Check screen is visible
4. Note any improvements
```

**Step 5: Final Take (10 minutes)**
```bash
1. Record again with improvements
2. Watch to confirm
3. Ready to upload!
```

---

## 🎯 FINAL CHECKLIST

Before uploading, verify:

- [ ] Audio is clear
- [ ] Screen is visible (not blurry)
- [ ] Script is followed
- [ ] All key features shown
- [ ] Tests running successfully
- [ ] GitHub repository shown
- [ ] Under time limit (check hackathon rules)
- [ ] Video format correct (MP4 recommended)
- [ ] File size appropriate (check limits)

---

## 💬 SAMPLE SCRIPT TO READ

### Introduction (20 seconds)
```
"Hi judges, I'm presenting AI Employee Vault for Hackathon 0.
This is a Platinum tier autonomous AI employee system
built with Claude Code. Let me show you what it can do."
```

### Demo Lead-in (10 seconds)
```
"Now let me show you the system in action.
I'll start with a health check to verify everything is operational."
```

### GitHub Lead-in (10 seconds)
```
"The complete source code and documentation are on GitHub.
Let me show you the repository."
```

### Conclusion (20 seconds)
```
"To summarize, AI Employee Vault demonstrates a production-ready
Digital FTE with hybrid cloud/local architecture, secure delegation,
and human-in-the-loop oversight. Thank you for watching!"
```

---

## 📹 RECORDING TIPS

### Camera Position
- Keep camera at eye level
- Good lighting on your face
- Plain background (less distraction)

### Audio
- Quiet room
- Speak clearly and at moderate pace
- Use microphone if available (better quality)

### Screen
- Use 1080p or higher resolution
- Close unnecessary apps
- Use dark mode for coding (easier to see)

### Environment
- Quiet space (no background noise)
- Stable internet (if recording online)
- Do Not Disturb mode on

---

## 🚀 QUICK START RECORDING

### Option 1: Single Take (Fastest)

1. Open all files in VS Code
2. Open GitHub in browser
3. Open terminal
4. Press `Win + G` then click "Start recording"
5. Follow this order:
   - Show README (30s)
   - Run health check (30s)
   - Run tests (1 min)
   - Show architecture diagrams (30s)
   - Show GitHub (1 min)
   - Conclusion (30s)
6. Press `Win + Alt + R` to stop

**Total time**: 4 minutes

### Option 2: Multi-Take (Best Quality)

1. Record intro separately
2. Record demo separately
3. Record GitHub separately
4. Edit together in post-production

**Total time**: 15-20 minutes

---

## 📋 FILES REFERENCE CARD

Keep this handy while recording:

### Must Show Files
```
✅ README.md (overview)
✅ PLATINUM_DEMO.md (demo script)
✅ docs/ARCHITECTURE_DIAGRAMS.md (diagrams)
✅ docs/API_DOCUMENTATION.md (API reference)
✅ tests/test_suite.py (test suite)
✅ skills/health_monitor.py (health monitoring)
✅ skills/cloud_zone_manager.py (cloud zone)
✅ skills/local_zone_manager.py (local zone)
```

### Must Show URLs
```
✅ https://github.com/Ambreeen17/h0
✅ Click "Code" tab (show structure)
✅ Click "commits" (show history)
```

### Must Run Commands
```
✅ python skills/health_monitor.py --summary
✅ python tests/test_suite.py --all
✅ python skills/cloud_zone_manager.py --status
✅ python skills/local_zone_manager.py --status
```

---

## ✅ FINAL TIP

**Practice makes perfect!**

Record yourself once, watch it, note improvements, then record again.

The second take will be much better!

---

**Good luck with your video!** 🎬💎

**Your AI Employee Vault is amazing - let the judges see it!**
