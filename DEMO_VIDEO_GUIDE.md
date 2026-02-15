# Demo Video Production Guide

**Purpose**: Guide for creating a professional demo video of the Platinum tier AI Employee
**Target Duration**: 20 minutes
**Audience**: Hackathon judges

---

## Quick Start (3 Options)

### Option 1: Automated Script Recording ⭐ RECOMMENDED

**Windows**: Run `record_demo.bat`
**Linux/Mac**: Run `bash record_demo.ps1` (requires PowerShell)

This script:
- Automates all demo steps
- Adds narration prompts
- Controls timing
- Provides visual cues

**Steps**:
1. Open terminal in project directory
2. Start screen recording (Windows Game Bar: Win+G, or OBS Studio)
3. Run the script: `record_demo.bat` (Windows) or `bash record_demo.ps1` (Mac/Linux)
4. Follow on-screen prompts
5. Stop recording when demo completes

### Option 2: Live Presentation During Judging

Skip the video and present live:
1. Practice the demo flow (follow PLATINUM_DEMO.md)
2. Prepare speaking points (use VIDEO_SCRIPT.md)
3. Present live during judging session
4. Be ready for technical issues (have backup plan)

### Option 3: Screen Recording + Voiceover

Record screen first, then add narration:
1. Run `record_demo.bat` (silently, without speaking)
2. Record the screen output
3. Use VIDEO_SCRIPT.md as narration guide
4. Record voiceover separately
5. Edit together in video editing software

---

## Recommended Recording Tools

### Windows

1. **Windows Game Bar** (Built-in, Free)
   - Press Win+G to open
   - Record screen or window
   - Good for quick recordings

2. **OBS Studio** (Free, Open Source)
   - https://obsproject.com/
   - Professional quality
   - More control over settings
   - Can add overlays and transitions

3. **Microsoft Stream** (Free with Microsoft account)
   - Built into Windows 10/11
   - Screen recording with webcam
   - Good for presenter-in-corner style

### Mac

1. **QuickTime Player** (Built-in, Free)
   - File → New Screen Recording
   - Simple and effective

2. **OBS Studio** (Free, Open Source)
   - Same as Windows version
   - Recommended for professional results

### Linux

1. **SimpleScreenRecorder** (Free)
   - `sudo apt install simplescreenrecorder`
   - Easy to use

2. **OBS Studio** (Free, Open Source)
   - Available on all platforms
   - Consistent experience

---

## Pre-Recording Checklist

### 1. System Preparation

- [ ] Close unnecessary applications (reduce distractions)
- [ ] Disable notifications (Windows Focus Assist, Do Not Disturb)
- [ ] Set display resolution to 1920x1080 (Full HD)
- [ ] Use a large terminal font (14-16pt) for readability
- [ ] Clear desktop icons (reduce visual clutter)
- [ ] Test screen recording software (do a test recording)

### 2. Terminal Setup

- [ ] Set terminal to full screen or large window
- [ ] Choose color scheme with good contrast
- [ ] Enable line numbers (if available)
- [ ] Set scroll buffer to maximum
- [ ] Test all commands beforehand

### 3. Demo Environment

- [ ] Verify all zone structures exist
- [ ] Test all Platinum tier skills
- [ ] Clear old test data (optional, for clean demo)
- [ ] Have backup commands ready (in case something fails)

### 4. Script Preparation

- [ ] Read VIDEO_SCRIPT.md completely
- [ ] Practice speaking each section
- [ ] Time your practice run (aim for ~20 minutes)
- [ ] Mark difficult sections for extra practice

---

## Recording Process

### Step 1: Initial Setup (5 minutes)

1. **Open terminal** in the project directory
2. **Set window size** to fill most of the screen
3. **Start screen recording software**
4. **Do a 10-second test recording** and check:
   - Audio is clear
   - Terminal text is readable
   - No background distractions
   - Recording frame rate is smooth

### Step 2: Start Recording

1. **Clear terminal** (`cls` or `clear`)
2. **Start screen recording**
3. **Wait 3 seconds** (gives editing room for post-production)
4. **Start demo script**: `record_demo.bat` (Windows) or `bash record_demo.ps1` (Mac/Linux)

### Step 3: Follow the Script

The automated script will guide you through:

**Part 1: Introduction** (2 minutes)
- Project overview
- Tier progression
- Platinum tier features

**Part 2: Setup Verification** (2 minutes)
- Zone structure verification
- Directory listings
- Status checks

**Part 3: Work-Zone Architecture** (3 minutes)
- Cloud zone capabilities
- Local zone capabilities
- Delegation architecture

**Part 4: Cloud Zone Operations** (4 minutes)
- Email task creation
- Task triage
- Draft creation

**Part 5: Secure Zone Sync** (4 minutes)
- Task syncing
- Secret filtering demonstration

**Part 6: Local Zone Approval** (5 minutes)
- Task processing
- Approval workflow
- Action execution

**Part 7: Delegation Architecture** (2 minutes)
- Claim-by-move
- Single-writer dashboard

**Part 8: Health Monitoring** (2 minutes)
- Health checks
- Monitoring cycle
- Alerts

**Part 9: Summary** (2 minutes)
- Complete flow summary
- Final status check

**Total: ~26 minutes** (some sections run faster)

### Step 4: Stop Recording

1. **Wait for demo completion message**
2. **Stop screen recording**
3. **Save recording** as `platinum_demo_raw.mp4`
4. **Verify file size** (should be several hundred MB)

---

## Post-Production

### Option A: Minimal Editing (Quick)

If you're short on time:

1. **Trim beginning** (remove preparation)
2. **Trim end** (remove stopping recorder)
3. **Add title card** at beginning:
   - "Personal AI Employee - Platinum Tier Demo"
   - "Hackathon 0"
   - "Duration: ~20 minutes"
4. **Export** as MP4 (H.264, 1080p, 30fps)

### Option B: Professional Editing (Polished)

For best results:

1. **Add section titles** for each of the 9 parts
2. **Highlight key outputs** with zoom or highlights:
   - Cloud zone status
   - Triage result
   - Approval request
   - Secret blocking
3. **Add text overlays** for:
   - Commands being run
   - Key results
   - Important metrics
4. **Smooth transitions** between sections
5. **Add progress indicator** (Part X of 9)
6. **Include background music** (optional, subtle):
   - Use copyright-free music
   - Keep volume low
   - Fade out during technical demos
7. **Add closed captions** for accessibility
8. **Export** as high-quality MP4

---

## Audio Guidelines

### Voiceover Tips

1. **Microphone**:
   - Use a quality USB microphone
   - Position 6-8 inches from mouth
   - Use pop filter (or speak past the mic)

2. **Environment**:
   - Record in quiet room
   - Close windows and doors
   - Turn off fans and AC
   - Use soft furnishings to reduce echo

3. **Speaking**:
   - Speak clearly and at moderate pace
   - Maintain consistent volume
   - Emphasize key terms
   - Pause between sections
   - Sound natural, not robotic

4. **Script**:
   - Use VIDEO_SCRIPT.md as your guide
   - Practice each section before recording
   - Mark your script with breathing pauses
   - Don't be afraid to re-record sections

### Adding Voiceover (Post-Recording)

If you record screen first:

1. **Watch the raw video** and note timestamps
2. **Record narration** section by section
3. **Import both files** into video editor
4. **Sync narration** with screen actions
5. **Trim and adjust** for perfect timing
6. **Add background music** (optional, very subtle)

---

## Export Settings

### Recommended Export Settings

**Format**: MP4
**Codec**: H.264
**Resolution**: 1920x1080 (Full HD)
**Frame Rate**: 30 fps
**Bitrate**: 8-12 Mbps (1080p)
**Audio**: AAC, 192 kbps, 48 kHz

### Platform-Specific Settings

**YouTube**:
- Resolution: 1920x1080
- Codec: H.264
- Bitrate: 8 Mbps
- Format: MP4

**Vimeo**:
- Resolution: 1920x1080
- Codec: H.264
- Bitrate: 10 Mbps
- Format: MP4

**Hackathon Submission**:
- Follow contest rules
- Usually: MP4, <500MB, <20 minutes

---

## Troubleshooting

### Issue: Terminal text is too small

**Solution**:
- Windows Terminal: Settings → Appearance → Font Size (14-16)
- Git Bash: Right-click → Options → Text → Size (14-16)
- Mac Terminal: Terminal → Preferences → Text → Font (14-16)

### Issue: Commands run too fast

**Solution**:
- Add `timeout /t X` (Windows) or `sleep X` (Linux/Mac) after commands
- Practice your typing speed
- Edit recording to slow down sections

### Issue: Demo fails during recording

**Solution**:
- Don't panic! Troubleshooting is part of the demo
- Explain what went wrong
- Show how you fix it
- If unrecoverable, re-record that section
- Edit multiple takes together in post-production

### Issue: Audio quality is poor

**Solution**:
- Use better microphone
- Record in quieter room
- Use noise reduction in post-production
- Re-record voiceover separately

### Issue: Recording file is too large

**Solution**:
- Reduce bitrate in export settings
- Lower resolution to 1280x720 (720p)
- Use more compression (larger file, but acceptable quality)

---

## Final Checklist

### Before Submission

- [ ] Video plays correctly on multiple devices
- [ ] Audio is clear and understandable
- [ ] All 9 parts of demo are included
- [ ] Key features are demonstrated (zones, sync, approval, health)
- [ ] Duration is under 20 minutes (or contest limit)
- [ ] File size meets submission requirements
- [ ] Video is exported in correct format
- [ ] Closed captions are available (if required)
- [ ] Video is uploaded or prepared for submission
- [ ] Backup copy is saved locally

---

## Alternative: Live Demo Tips

If presenting live instead of video:

1. **Practice extensively** - know the flow by heart
2. **Have backup commands** - in case something fails
3. **Prepare a slideshow** - with screenshots as backup
4. **Test the environment** - where you'll present
5. **Have a timer** - keep track of time
6. **Be ready for questions** - judges will ask
7. **Stay calm** - if something breaks, explain and move on

---

## Resources

- **Demo Script**: `VIDEO_SCRIPT.md` - Complete narration with timestamps
- **Demo Guide**: `PLATINUM_DEMO.md` - Technical demo walkthrough
- **Recording Script**: `record_demo.bat` (Windows) or `record_demo.ps1` (Mac/Linux)
- **Verification**: `PLATINUM_TIER_VERIFICATION.md` - Feature checklist

---

## Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Review PLATINUM_DEMO.md for technical details
3. Test commands individually before recording
4. Consider Option 2 (live presentation) if recording is problematic
5. Focus on clear communication over perfect production

Remember: **Content is more important than production quality**.
A clear, well-explained demo beats a polished but confusing one.

Good luck with your demo! 🎬✨
